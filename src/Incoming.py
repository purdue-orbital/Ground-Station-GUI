from ThreadedWindow import ThreadedClient
import math

from Mode import Mode


def find_cardinal_direction(x, y):
    return math.atan2(y, x)


class Incoming:
    __instance = None

    def get_instance(self):
        if Incoming.__instance is None:
            Incoming()
        return Incoming.__instance

    def __init__(self):
        if Incoming.__instance is not None:
            raise Exception("Constructor should not be called")
        else:
            Incoming.__instance = IncomingSingleton()


class IncomingSingleton:
    def __init__(self):
        self.queue = None

    def parse_data(self, data):
        if self.queue is None:
            print("Queue not bound")
            return -1

        self.queue.put(data)
