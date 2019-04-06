import json
import time
import traceback
import sys

from digi.xbee.devices import XBeeDevice, XBee64BitAddress, RemoteXBeeDevice, XBeeException

# Local port number:
# - For linux, it will be '/dev/ttyS#'
# - For windows, it will be 'COM#'
#
# where # is the port number.
LOCAL_PORT = "/dev/ttyS13"

# Baud rate of the local device
BAUD_RATE = 9600


# Remote node MAC address in hexadecimal format
REMOTE_NODE_ADDRESS = '0013A20040F6E10C'

class RadioTest:
    def __init__(self):
        self.device = XBeeDevice(LOCAL_PORT, BAUD_RATE)
        self.device.set_sync_ops_timeout(10)
        self.device.open()
        self.remote_device = None
        self.queue = None

        try:
            self.remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(REMOTE_NODE_ADDRESS))
            if self.remote_device is None:
                print("Could not find the remote device")

            print(self.remote_device)
        except XBeeException:
            print("Exception has occurred")

    def spam(self):
        for i in range(100):
            if i % 2 == 0:
                origin = "balloon"
            else:
                origin = "rocket"


            data = '{\"origin\":\"' + origin + '\",\"alt\":' + str(i) + ',\"GPS\":{\"long\":10,\"lat\":10},\"gyro\":{\"x\":10,\"y\":10,\"z\":' + str(i) + '},\"mag\": '+ str(i) + ',\"temp\": '+ str(i) +',\"acc\":{\"x\":10,\"y\":10,\"z\":10}}'

            print(data)

            try:
                self.device.send_data(self.remote_device, data)
                print("Success")
            except Exception as e:
                traceback.print_exc()
                self.device.reset()
                self.device.close()
                self.device.open()
                print(e)

            time.sleep(2)

        self.close()
        sys.exit(1)


    def close(self):
        try:
            self.device.close()
        except Exception as e:
            print(e)


mod = RadioTest()
mod.spam()
