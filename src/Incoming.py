from ThreadedWindow import ThreadedClient
import math


class Incoming:
    def __init__(self, client):
        self.client = client

    def parse_data(self, data):
        self.client.insert_data(data)

    def find_cardinal_direction(self, x, y):
        return math.atan2(y, x)
