import logging
import sys
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


class Module:
    __instance = None

    def get_instance(self):
        if Module.__instance is None:
            Module()
        return Module.__instance

    def __init__(self):
        if Module.__instance is not None:
            raise Exception("Constructor should not be called")
        else:
            Module.__instance = ModuleSingleton()


class ModuleSingleton:
    def __init__(self):
        self.device = XBeeDevice(LOCAL_PORT, BAUD_RATE)
        self.remote_device = None
        self.queue = None

        try:
            self.remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(REMOTE_NODE_ADDRESS))
            if self.remote_device is None:
                print("Could not find the remote device")
        except XBeeException:
            print("Exception has occurred")

    def send(self, data):
        print("Testing data: " + data)
        try:
            self.device.open()
            print("Sending data to %s >> %s..." % (self.remote_device.get_64bit_addr(), DATA_TO_SEND))

            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="[root] %(levelname)s - %(message)s")

            logger = logging.getLogger(self.device.get_node_id())

            self.device.send_data(self.remote_device, data)

            print("Success")

        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()

    def bind_queue(self, queue):
        self.queue = queue

    def receive(self):
        try:
            self.device.open()

            def data_receive_callback(msg):
                address = xbee_message.remote_device.get_64bit_addr()
                data = xbee_message.data.decode("utf8")

                json_data = json.load(data)

                self.queue.put(json_data)

            self.device.add_data_received_callback(data_receive_callback)

            print("Waiting for data...\n")
            input()
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
