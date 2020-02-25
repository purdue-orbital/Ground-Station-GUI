#! /usr/bin/python3.6
import json

from Mode import Mode
from communications.RadioModule import Module


class Comm:
    __instance = None

    def get_instance(self):
        if Comm.__instance is None:
            Comm()
        return Comm.__instance

    def __init__(self):
        if Comm.__instance is not None:
            raise Exception("Constructor should not be called")
        else:
            Comm.__instance = CommSingleton()


class CommSingleton:
    def __init__(self):

        self.packets_sent = 0
        self.packets_received = 0

        try:
            self.__mode = Mode.STANDBY
            self.__radio = Module.get_instance(self)
        except Exception as e:
            print("Module Err")
            print(e)

    def standby(self):
        self.__mode = Mode.STANDBY

    def testing(self):
        self.__mode = Mode.TESTING

    def flight(self):
        self.__mode = Mode.FLIGHT

    def set_mode(self, m):
        if m == Mode.STANDBY:
            self.standby()
        elif m == Mode.TESTING:
            self.testing()
        elif m == Mode.FLIGHT:
            self.flight()
        else:
            print("INVALID MODE DETECTED. REVERTING TO TESTING MODE.")
            self.testing()

    def get_mode(self):
        return self.__mode

    def get_packets_sent(self):
        return self.packets_sent

    def get_packets_received(self):
        return self.packets_received

    def reset_counters(self):
        self.packets_sent = 0
        self.packets_received = 0

    def send(self, command):
        self.packets_sent += 1
        print("Sending...")

        if self.__mode == Mode.STANDBY:
            # discard command
            print("\nStandby, command discarded.\n")

        command_json = {}
        if self.__mode == Mode.TESTING:
            command_json["mode"] = "testing"
            command_json["command"] = command

        if self.__mode == Mode.FLIGHT:
            command_json["mode"] = "flight"
            command_json["command"] = command

        try:
            if not len(command_json) == 0:
                print(command_json)

                sent = self.__radio.send(json.dumps(command_json))
                self.packets_received += 1 
                return sent
        except Exception as e:
            print("Sending Err")
            print(e)
            return 0
