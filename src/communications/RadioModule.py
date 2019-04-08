import logging
import sys
import traceback
import json

from digi.xbee.devices import XBeeDevice, XBee64BitAddress, RemoteXBeeDevice, XBeeException

# Local port number:
# - For linux, it will be '/dev/ttyS#'
# - For windows, it will be 'COM#'
#
# where # is the port number.
LOCAL_PORT = "/dev/ttyS10"

# Baud rate of the local device
BAUD_RATE = 9600

# Remote node MAC address in hexadecimal format
REMOTE_NODE_ADDRESS = "0013A2004148887C"


class Module:
    __instance = None

    def get_instance(self):
        if Module.__instance is None:
            print(Module.__instance)
            Module()
        return Module.__instance

    def __init__(self):
        if Module.__instance is not None:
            print(Module.__instance)
            raise Exception("Constructor should not be called")
        else:
            Module.__instance = ModuleSingleton()


class ModuleSingleton:
    def __init__(self):

        try:
            self.device = XBeeDevice(LOCAL_PORT, BAUD_RATE)
            self.device.set_sync_ops_timeout(10)
            self.device.open()
        except Exception as e:
            print("Local Device Failure")
            print(e)

        def data_receive_callback(msg):
            data = msg.data.decode("utf8")

            json_data = json.loads(data)

            print(json_data)

            self.queue.put(json_data)

        try:
            self.device.add_data_received_callback(data_receive_callback)
        except Exception as e:
            print("Callback Failure")
            print(e)
            self.reset_radio()

        self.remote_device = None
        self.queue = None

        try:
            self.remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(REMOTE_NODE_ADDRESS))
            print(self.remote_device)
            if self.remote_device is None:
                print("Could not find the remote device")
        except XBeeException:
            print("Exception has occurred")

    def send(self, data):
        try:
            self.device.send_data(self.remote_device, data)
        except XBeeException as e:
            print(repr(e))
            traceback.print_exc()
            print("Sending Error")
            self.reset_radio()

        print("Sent")

    def bind_queue(self, queue):
        self.queue = queue

    def reset_radio(self):
        print("Resetting Radio Connection")
        self.device.reset()

    def close(self):
        try:
            self.device.close()
        except Exception as e:
            print(e)
