import time
import tkinter as tk
from tkinter import messagebox
import RPi.GPIO as GPIO


from Timer import *
from MainWindow import DataWindow

import threading
import random
import queue
import json


class ThreadedClient:
    def __init__(self, master):

        self.master = master
        # self.master.iconify for the memes
        root.protocol("WM_DELETE_WINDOW", self.end_application)

        self.queue = queue.Queue()

        self.gui = DataWindow(master, self.queue)

        self.running = 1
        self.thread1 = threading.Thread(target=self.check_queue)
        self.thread1.start()

        self.update()

    def update(self):
        self.gui.process_incoming()
        if not self.running:
            import sys
            sys.exit(1)
        self.master.after(200, self.update)

    def check_queue(self):
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

    def end_application(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.running = 0
            GPIO.cleanup()
            root.destroy()


rand = random.Random()
root = tk.Tk()

client = ThreadedClient(root)
root.mainloop()
