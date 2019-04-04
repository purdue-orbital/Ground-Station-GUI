import os
import json
from pprint import pprint
import subprocess

def getIndex(line):
    i = 0
    for c in line:
        if c == '=':
            i += 1
            break
        i += 1
    return i+1

def readLog():
    with open("./logs/status.log", 'r') as f:
        lines = tail(f, 11)
    # pprint(lines)
    for line in lines:
        if "temperature" in line:
            i = getIndex(line)
            print("temperature: " + line[i:-1])
        elif "pressure" in line:
            i = getIndex(line)
            print("pressure: " + line[i:-1])
        elif "humidity" in line:
            i = getIndex(line)
            print("humidity: " + line[i:-1])
        elif "altitude" in line:
            i = getIndex(line)
            print("altitude: " + line[i:-1])
        elif "direction" in line:
            i = getIndex(line)
            print("direction: " + line[i:-1])
        elif "acceleration" in line:
            i = getIndex(line)
            print("acceleration: " + line[i:-1])
        elif "velocity" in line:
            i = getIndex(line)
            print("velocity: " + line[i:-1])

def tail(f, n):
    assert n >= 0
    pos, lines = n+1, []
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


def main():
    readLog()


if __name__ == '__main__':
    main()

#TODO: Write Tail function to get most recent log
#TODO: Check that the log is the same as the json file passed to it

