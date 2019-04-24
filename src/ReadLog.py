import os
import json
from pprint import pprint
import subprocess


class ReadLog:

    def __init__(self):
        self.status = 0

    def getIndex(self, line):
        i = 0
        for c in line:
            if c == '=':
                i += 1
                break
            i += 1
        return i + 1

    def tail(self, f, n):
        assert n >= 0
        pos, lines = n + 1, []
        while len(lines) <= n:
            try:
                f.seek(-pos, 2)

            except IOError:
                f.seek(0)
                break
            finally:
                lines = list(f)
            pos *= 2
        return lines[-n:]

    def readLog(self):
        with open("./logs/status.log", 'r') as f:
            lines = self.tail(f, 11)
        for line in lines:
            if "temperature" in line:
                i = self.getIndex(line)
                print("temperature: " + line[i:-1])
            elif "pressure" in line:
                i = self.getIndex(line)
                print("pressure: " + line[i:-1])
            elif "humidity" in line:
                i = self.getIndex(line)
                print("humidity: " + line[i:-1])
            elif "altitude" in line:
                i = self.getIndex(line)
                print("altitude: " + line[i:-1])
            elif "direction" in line:
                i = self.getIndex(line)
                print("direction: " + line[i:-1])
            elif "acceleration" in line:
                i = self.getIndex(line)
                print("acceleration: " + line[i:-1])
            elif "velocity" in line:
                i = self.getIndex(line)
                print("velocity: " + line[i:-1])

