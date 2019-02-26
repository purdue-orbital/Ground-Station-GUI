import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import RPi.GPIO as GPIO

from Timer import *
from DataWindow import DataWindow

from GraphNotebook import GraphNotebook

import threading
import random
import queue
import json


class ThreadedClient:
    def __init__(self, master):

        self.master = master
        # self.master.iconify for the memes
        root.protocol("WM_DELETE_WINDOW", self.end_application)

        # Queue to buffer incoming data
        self.queue = queue.Queue()

        # Window to display all data
        self.gui = DataWindow(master, self.queue)

        # Create thread to spoof data in queue
        self.running = 1
        self.thread1 = threading.Thread(target=self.test_queue)
        self.thread1.start()

        # Create testing variables
        self.testing = 0

        # Add event to detect GPIO pin 11
        GPIO.add_event_detect(11, GPIO.RISING, callback=self.launch())

        # Process data in queue
        self.update()

    def update(self):
        self.gui.process_incoming()
        if not self.running or not self.gui.running:
            if self.end_application():
                import sys
                sys.exit(1)
        self.master.after(200, self.update)

    def set_testing(self, isTesting):
        self.testing = isTesting
        self.gui.set_testing(isTesting)

    def insert_data(self, data):
        self.queue.put(data)

    def handle_radio(self):
        print("test")

    def error(self, message):
        messagebox.showinfo("Error", message)

    def test_queue(self):
        while self.running:
            time.sleep(1)

            preload = ('{"temperature":' + str(rand.random())[0:5] + ',' +
                       '"pressure":' + str(rand.random())[0:5] + ',' +
                       '"humidity":' + str(rand.random())[0:5] + ',' +
                       '"altitude":' + str(rand.random())[0:5] + ',' +
                       '"direction":' + str(rand.random())[0:5] + ',' +
                       '"acceleration":' + str(rand.random())[0:5] + ',' +
                       '"velocity":' + str(rand.random())[0:5] + ',' +
                       '"user_angle":' + str(rand.random())[0:5] + ' }')

            # print(preload)

            data_json = json.loads(preload)
            self.queue.put(data_json)

    def launch(self):
        print("Lauching")
        # TODO send launch

    def end_application(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.running = 0
            self.gui.close()
            GPIO.cleanup()
            root.destroy()
            return 1

        else:
            self.gui.running = 1
            return 0


rand = random.Random()
root = tk.Tk()

client = ThreadedClient(root)
root.mainloop()
