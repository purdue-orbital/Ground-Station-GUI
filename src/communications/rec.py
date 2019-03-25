from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

# Instantiate an XBee device object.
device = XBeeDevice("/dev/ttyS13", 9600)

device.open()
addr = device.get_64bit_addr()
print(addr)



# Instantiate a remote XBee device object.
remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string("0013A20040F6E10C"))

# Read data sent by the remote device.
xbee_message = device.read_data(remote_device)
