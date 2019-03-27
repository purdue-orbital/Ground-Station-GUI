from ThreadedWindow import ThreadedClient
import math

from Mode import Mode


class Incoming:
    __instance = None

    def get_instance():
        if Incoming.__instance == None:
            Incoming()
        return Incoming.__instance

    def __init__(self):
        if Incoming.__instance != None:
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
