from digi.xbee.devices import XBeeDevice, XBee64BitAddress, RemoteXBeeDevice, XBeeException

# Local port number:
# - For linux, it will be '/dev/ttyS#'
# - For windows, it will be 'COM#'
#
# where # is the port number.
LOCAL_PORT = "/dev/ttyS10"

# Baud rate of the local device
BAUD_RATE = 9600

DATA_TO_SEND = "Hello XBee!"

# Remote node MAC address in hexidecimal format
REMOTE_NODE_ADDRESS = "0013A2004148887C"


class Module:
    def __init__(self):
        self.device = XBeeDevice(LOCAL_PORT, BAUD_RATE)
        self.remote_device = None

        try:
            remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(REMOTE_NODE_ADDRESS))
            if remote_device is None:
                print("Could not find the remote device")
        except XBeeException:
            print("Exception has occurred")

    def send(self, data):

        try:
            self.device.open()
            print("Sending data to %s >> %s..." % (self.remote_device.get_64bit_addr(), DATA_TO_SEND))

            self.device.send_data_async(self.remote_device, data)

            print("Success")
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()

    def poll(self):
        try:
            self.device.open()

            def data_receive_callback(msg):
                print("From %s >> %s" % (msg.remote_device.get_64bit_addr(),
                                         msg.data.decode()))

            self.device.add_data_received_callback(data_receive_callback)

            print("Waiting for data...\n")
            input()
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()


def main():
    device = XBeeDevice(LOCAL_PORT, BAUD_RATE)

    try:
        device.open()

        # Obtain the remote XBee device from the XBee network.
        # xbee_network = device.get_network()
        # remote_device = xbee_network.discover_device(REMOTE_NODE_ID)

        # Instantiate remote device
        remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(REMOTE_NODE_ADDRESS))

        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        print("Sending data to %s >> %s..." % (remote_device.get_64bit_addr(), DATA_TO_SEND))

        device.send_data_async(remote_device, DATA_TO_SEND)

        print("Success")

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    pass
