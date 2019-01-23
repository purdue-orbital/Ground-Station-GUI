import time
from tkinter import *


from Timer import *
from MainWindow import *

import threading
import random
import queue
import json


class ThreadedClient:
    def __init__(self, master):

        self.master = master
        # self.master.iconify for the memes
        root.protocol("WM_DELETE_WINDOW", self.endApplication)

        self.queue = queue.Queue()

        self.gui = DataWindow(master, self.queue)

        self.running = 1
        self.thread1 = threading.Thread(target=self.checkQueue)
        self.thread1.start()

        self.update()

    def update(self):
        self.gui.processIncoming()
        if not self.running:
            import sys
            sys.exit(1)
        self.master.after(200, self.update)

    def checkQueue(self):
        while self.running:
            time.sleep(1)

            preload = ( '{ "temperature":' + str(rand.random())[0:5] + ','
                             '"pressure":' + str(rand.random())[0:5] + ','
                             '"humidity":' + str(rand.random())[0:5] + ','
                             '"altitude":' + str(rand.random())[0:5] + ','
                             '"direction":' + str(rand.random())[0:5] + ','
                             '"acceleration":' + str(rand.random())[0:5] + ','
                             '"velocity":' + str(rand.random())[0:5] + ','
                             '"user_angle":' + str(rand.random())[0:5] + ' }' )

            print(preload)

            dataJson = json.loads(preload)
            self.queue.put(dataJson)

    def endApplication(self):
        self.running = 0


rand = random.Random()
root = Tk()

client = ThreadedClient(root)
root.mainloop()
