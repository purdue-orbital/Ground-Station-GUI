from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

local_xbee = XBeeDevice("/dev/ttyS13", 9600)

local_xbee.open()

remote_xbee = RemoteXBeeDevice(local_xbee, XBee64BitAddress.from_hex_string("0013A20040F6E10C"))


local_xbee.send_data(remote_xbee, "Hello World!")


local_xbee.close()



