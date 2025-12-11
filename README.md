# reinkpy-fix
Free and open waste ink counter resetter for some (EPSON) printers.
# reinkpy-fix (Epson Printer Waste Counter Reset)

A working fork of the `reinkpy` project by Daniel Gerber 'https://codeberg.org/atufi/reinkpy' with critical fixes implemented for resetting the Epson EcoTank waste ink counter.

**Status:** Confirmed working for Epson L3060 Series and similar.

---

### Problem Solved:

The original `reinkpy` library fails when attempting to execute the waste counter reset (`driver.reset_waste()`) via LAN/SNMP. This is because:

1.  The `reinkpy/snmp.py` file **lacked the necessary SNMP SET command** logic for writing data.
2.  The library failed to correctly pass the necessary proprietary **write community string** (`EPCF_PASS`) from the user script to the SNMP connection.

**This repository fixes both issues.**

### 🛠️ How to Use (LAN Fix)

1.  **Clone this Repository:**
    ```bash
    git clone https://github.com/LeFZdev/reinkpy-fix
    cd reinkpy-fix
    ```
2.  **Setup Virtual Environment** (If needed):
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```
    
3.  **Run the Reset Script:**
    Modify the provided `main.py` to use the correct printer IP and the necessary.

    
5.  **Execute:**
    ```bash
    python main.py
    ```
    
---

### Notable Contributions (My Fixes)

The following changes were implemented to enable LAN write functionality:

* **`reinkpy/snmp.py`**: Added the missing `_set_cmd` method utilizing `pysnmp.hlapi.setCmd` to enable SNMP SET (write) operations.
* **`reinkpy/__init__.py`**: Patched `NetworkDevice` to accept and pass the `write_user` argument from the calling script to the `SNMPLink` constructor.
* Fixed syntax erros in **`reinkpy/__init__.py`**, and **`reinkpy/snmp.py`**, As well as changing file nominations of **`reinkpy/usbtest.py`** and **`reinkpy/netscan.py`** to prevent circular imports
***
**Fixed by Ziad EL Fazazi**
