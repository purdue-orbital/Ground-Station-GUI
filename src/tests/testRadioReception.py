import json

from digi.xbee.devices import XBeeDevice, XBee64BitAddress, RemoteXBeeDevice, XBeeException

# Local port number:
# - For linux, it will be '/dev/ttyS#'
# - For windows, it will be 'COM#'
#
# where # is the port number.
LOCAL_PORT = "/dev/ttyS7"

# Baud rate of the local device
BAUD_RATE = 9600

DATA_TO_SEND = "Hello XBee!"

# Remote node MAC address in hexadecimal format
REMOTE_NODE_ADDRESS = "0013A2004148887C"

class RadioTest:
    def __init__(self):
        self.device = XBeeDevice(LOCAL_PORT, BAUD_RATE)
        self.device.open()
        self.remote_device = None
        self.queue = None

        try:
            self.remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(REMOTE_NODE_ADDRESS))
            if self.remote_device is None:
                print("Could not find the remote device")
        except XBeeException:
            print("Exception has occurred")

    def spam(self):
        for i in range(100):
            data = '{\"origin\":\"balloon\",\"alt\":' + i + ',\"GPS\":{\"long\":10,\"lat\":10},\"gyro\":{\"x\":10,\"y\":10,\"z\":10},\"mag\":10,\"temp\":10,\"acc\":{\"x\":10,\"y\":10,\"z\":10}}'

            print(data)

            try:
                self.device.send_data(self.remote_device, data)
            except Exception as e:
                print(e)

            sleep(1)

    def close(self):
        try:
            self.device.close()
        except Exception as e:
            print(e)


mod = RadioTest()
mod.spam()
