# SPDX-License-Identifier: AGPL-3.0-or-later
__all__ = (
    'SNMPLink',
)

from pysnmp.hlapi import *
import contextlib, functools
import logging
_log = logging.getLogger(__name__)
del logging


class SNMPLink:

    OID_PRINTER = '1.3.6.1.2.1.43'
    OID_ENTERPRISE = '1.3.6.1.4.1'
    OID_ppmPrinterIEEE1284DeviceId = OID_ENTERPRISE + '.2699.1.2.1.2.1.1.3.1'

    def __init__(self, ip, port=161, version='1', read_user='public', write_user='private'):
        self.ip = ip
        self.port = port
        assert version in ('1', '2c', '3')
        self.version = version
        self.read_user = read_user       # Used for GET (Reading)
        self.write_user = write_user     # Used for SET (Writing)
        # ... (rest of the function)

    def _get_cmd(self, oid):
        if self.version == '1':
            auth = CommunityData(self.read_user, mpModel=0)
        elif self.version == '2c':
            auth = CommunityData(self.read_user, mpModel=1)
        else:
            auth = UsmUserData(self.read_user)
        engine = SnmpEngine()
        # TMPFIX: ensure running loop
        import asyncio
        try: asyncio.get_running_loop()
        except RuntimeError: asyncio.set_event_loop(asyncio.new_event_loop())
        return getCmd(
            engine,
            auth,
            UdpTransportTarget((self.ip, self.port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid), None),
            lookupMib=True
        )
    
    def _set_cmd(self, oid_value_pair):
        """Executes an SNMP SET command to write data to the device."""
        
        # Use the WRITE user for SET commands
        if self.version == '1':
            auth = CommunityData(self.write_user, mpModel=0)
        elif self.version == '2c':
            auth = CommunityData(self.write_user, mpModel=1)
        else:
            auth = UsmUserData(self.write_user)
            
        engine = SnmpEngine()
        
        # TMPFIX: ensure running loop (keeping the original fix)
        import asyncio
        try: asyncio.get_running_loop()
        except RuntimeError: asyncio.set_event_loop(asyncio.new_event_loop())
        
        # FIX: Use setCmd for writing data
        return setCmd( 
            engine,
            auth,
            UdpTransportTarget((self.ip, self.port)),
            ContextData(),
            *oid_value_pair, # Expects a list of ObjectType(OID, Value)
            lookupMib=True
        )
    
    def get(self, oid):
        oid = getattr(self, f'OID_{oid}', oid)
        eInd, eStat, eIdx, varBinds = self._get_cmd(oid) #_iget.send((oid, None))
        if eInd:
            _log.warn(eInd)
        elif eStat:
            _log.warn('%s at %s', eStat.prettyPrint(),
                      varBinds[int(eIdx) - 1][0] if eIdx else '?')
        else:
            _log.debug('\n'.join((v.prettyPrint() for v in varBinds)))
            return varBinds

    @functools.cached_property
    def info(self) -> dict:
        try:
            r = self.get('ppmPrinterIEEE1284DeviceId')[0][1].asOctets().decode('ascii')
            from . import _parse_ieee1284_id
            return _parse_ieee1284_id(r)
        except:
            _log.exception('Reading IEEE 1284 device id failed.')
            return {}
