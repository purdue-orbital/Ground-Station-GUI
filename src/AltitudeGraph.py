#! /usr/bin/python3.6
import tkinter as tk
import matplotlib.pyplot as plt2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import queue

class AltitudeGraph:
    def update_altitude(self, h):
        plt2.pause(0.001)
        plt2.cla()
        plt2.xlabel("Time (s)")
        plt2.ylabel("Altitude (m)")
        plt2.title("Altitude vs Time")
        self.alititudeQ.get()
        self.alititudeQ.put(h)
        self.fig = plt2.plot(list(self.alititudeQ.queue), 'xkcd:cyan')

    def open_graph(self):
        plt2.pause(0.001)
        plt2.cla()
        plt2.xlabel("Time (s)")
        plt2.ylabel("Altitude (m)")
        plt2.title("Altitude vs Time")
        self.fig = plt2.plot(list(self.alititudeQ.queue), 'xkcd:cyan')

    def __init__(self):
        # DARK THEME!!!!!
        plt2.style.use('dark_background')
        # Crappy code so it can close properly
        self.fig = plt2.figure()
        # Adjust the space so there is more space  
        plt2.tight_layout()
        plt2.subplots_adjust(wspace=0, hspace=0)

        # Start in interactive mode so that the graph starts in a non blocking thread
        plt2.ion()

        self.alititudeQ = queue.Queue()

        # Fill the queue with 0s so that we can graph something if the user opens the graph early
        self.amount_of_point_to_graph = 20
        for i in range(0, self.amount_of_point_to_graph):
            self.alititudeQ.put(0)

        plt2.xlabel("Time (s)")
        plt2.ylabel("Altitude (m)")
        plt2.title("Altitude vs Time")

        # # Run the loop so the graph gets updated every second
        # while True:
        #     # Random data for now
        #     r = random.randint(-50,50)
        #     # Call methods for each graph to update x,y,z
        #     self.update_altitude(r)
        #     # Sleep for a second, will probably be replaced with a callback or something
        #     # ! Do not get rid of the pause, it messes it up for some reason
        #     time.sleep(1)
