import reinkpy
#Bombastic SIDEYE SIDEYE
# python main.py
# run this code to 

for p in reinkpy.Device.find():
    print(p.info)

# Or get a specific device
# p = reinkpy.Device.from_file('/dev/usb/lp0')
# For USB connection usb connection
# p = reinkpy.Device.from_usb(manufacturer='EPSON')

# For LAN connection
printer = reinkpy.Device.from_ip('X.X.X.X') # Consider putting your ip address there


driver = printer.epson # Epson driver
if not driver.spec.model: # Either model is unknown or autoconfiguration failed
    # Some printers just don't advertise their model name cleanly, e.g.
	driver.configure("L3060") # Here i used the name of my Epson printer "L3060 Series", so consider putting your printer model there"

driver.reset_waste()

# driver.reset_waste() to reset the waste counter
# driver.write_eeprom((address, value), …) to print eeprom values


# ~Fazazi