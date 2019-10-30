import traceback
import json
import serial

from digi.xbee.devices import XBeeDevice, XBee64BitAddress, RemoteXBeeDevice, XBeeException
from util.exception import RadioSerialConnectionException, RadioObjectException

# Local port number:
# - For linux (including ubuntu for windows), it will be '/dev/ttyS#'
# - For pure windows (cmd, PowerShell, Pycharm, etc), it will be 'COM#'
#
# where # is the port number.
LOCAL_PORT = "/dev/ttyS16"

# Baud rate of the local device
BAUD_RATE = 9600

# Remote node MAC address in hexadecimal format. This can be found on the radio chip itself, listed as the
# hardware address.
REMOTE_NODE_ADDRESS = "0013A2004187A0B0"

OK = "\u001b[32m"
WARN = "\u001b[33m"
ERR = "\u001b[31m"
NORM = "\u001b[0m"


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
        except serial.SerialException:
            # raise RadioSerialConnectionException
            pass

        def data_receive_callback(msg):
            data = msg.data.decode("utf8")
            json_data = json.loads(data)
            print(OK + "Received:")
            print(json_data)
            self.queue.put(json_data)

        try:
            self.device.add_data_received_callback(data_receive_callback)
        except AttributeError:
            raise RadioObjectException
            pass
            # self.reset_radio()
        except Exception as e:
            print(e)

        self.remote_device = None
        self.queue = None

        try:
            self.remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(REMOTE_NODE_ADDRESS))
            print("Remote Device Address: " + str(self.remote_device))
            if self.remote_device is None:
                print(ERR + "Could not find the remote device" + NORM)
        except XBeeException:
            print(ERR + "Remote Device Instantiation Error" + NORM)

    def send(self, data):
        try:
            self.device.send_data_broadcast(data)
            print(OK + "Sent" + NORM)
        except XBeeException as e:
            print(ERR + "Sending Error" + NORM)
            print(repr(e))
            traceback.print_exc()
            self.reset_radio()

    def bind_queue(self, queue):
        self.queue = queue

    def reset_radio(self):
        print(WARN + "Resetting Radio Connection" + NORM)
        self.device.reset()

    def close(self):
        try:
            self.device.close()
        except Exception as e:
            print(ERR + "Closing Error" + NORM)
            print(e)
