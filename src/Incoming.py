from ThreadedWindow import ThreadedClient


class Incoming:
    def __init__(self, client):
        self.client = client

    def parse_data(self, data):
        self.client.insert_data(data)
