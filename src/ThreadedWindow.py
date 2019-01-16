import time
from tkinter import *


from Timer import *
from MainWindow import *

import threading
import random
import queue
import json

# class GuiPart:
#     def __init__(self, master, queue, endCommand):
#         self.queue = queue
#         # Set up the GUI
#         console = ttk.Button(master, text='Done', command=endCommand)
#         console.pack(  )
#         # Add more GUI stuff here depending on your specific needs


class ThreadedClient:
    def __init__(self, master):

        self.master = master

        self.queue = queue.Queue()

        self.gui = MyWindow(master, self.queue)

        self.running = 1
        self.thread1 = threading.Thread(target=self.checkQueue)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.update()

    def update(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(200, self.update)

    def checkQueue(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.
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
