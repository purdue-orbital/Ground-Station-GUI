import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import RPi.GPIO as GPIO

from Timer import *
from DataWindow import DataWindow

# from GraphNotebook import GraphNotebook
from Mode import Mode
from communications.RadioModule import Module
from CommunicationDriver import Comm

import threading
import random
import queue
import json

OK = "\u001b[32m"
WARN = "\u001b[33m"
ERR = "\u001b[31m"
NORM = "\u001b[0m"

"""
ROCKET GUI Version 0.3-alpha
Author: Matt Drozt, Ken Sodetz, Jay Rixie, Emanuel Pituch, Connor Todd
Since: 10/31/2018
Created for Purdue Orbital Ground Stations Sub-Team
Parses and displays data from the a Raspberry Pi 3 to verbosely
display and graph all pertinent data from the launch structure.
"""


class ThreadedClient:
    def __init__(self, master):
        """
        Init method
        :param master: Master window
        """
        self.master = master
        # self.master.iconify for the memes
        root.protocol("WM_DELETE_WINDOW", self.end_application)

        # Queue to buffer incoming data
        self.queue = queue.Queue()

        # Create Module class and bind queue
        # TODO Exception handling
        self.radio = Module.get_instance(self)

        self.radio.bind_queue(self.queue)

        # Window to display all data
        self.gui = DataWindow(master, self.queue)

        self.running = 1

        # Create thread to spoof data in queue
        self.thread1 = threading.Thread(target=self.test_queue)
        self.thread1.start()
        
        # Process data in queue
        self.update()

    def update(self):
        # Loop function and handle data from interrupts
        try:
            self.gui.process_incoming()
            # Call again
            self.master.after(200, self.update)
        except Exception as e:
            print("Process Incoming Error")
            print(e)

    def error(self, message):
        messagebox.showinfo("Error", message)

    def test_queue(self):
        i = 0
        end = 0
        while self.running:
            time.sleep(1)
            if self.gui.is_test_mode():
                end = 1
                origin = "balloon"

                preload = (
                        '{ "origin" : "' + origin + '",' +
                        '"GPS": {' +
                        '"long": ' + str(rand.random())[0:5] + ',' +
                        '"alt": ' + str(rand.random())[0:5] + ',' +
                        '"lat": ' + str(rand.random())[0:5] +
                        '},' +
                        '"gyro": {' +
                        '"x": ' + str(rand.random())[0:5] + ',' +
                        '"y": ' + str(rand.random())[0:5] + ',' +
                        '"z": ' + str(rand.random())[0:5] +
                        '},' +
                        '"temp": ' + str(rand.random())[0:5] + ',' +
                        '"acc": {' +
                        '"x": ' + str(rand.random())[0:5] + ',' +
                        '"y": ' + str(rand.random())[0:5] + ',' +
                        '"z": ' + str(rand.random())[0:5] +
                        '}' +
                        '}'
                )

                preload2 = (
                        '{ "origin" : "status",' +
                        '"QDM" : 1,' +
                        '"Ignition" : 1,' +
                        '"Stabilization" : 1,' +
                        '"PlatRadio" : 1' +
                        '}'
                )

                data_json = json.loads(preload)
                data_json2 = json.loads(preload2)
                self.queue.put(data_json)
                self.queue.put(data_json2)

    def end_application(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.radio.close()
            self.running = 0
            if self.gui.shutdown_timer is not None:
                self.gui.shutdown_timer.stop()
            self.gui.close()
            GPIO.cleanup()
            root.destroy()

            return 0

        else:
            return 1


rand = random.Random()
root = tk.Tk()

client = ThreadedClient(root)
root.mainloop()
