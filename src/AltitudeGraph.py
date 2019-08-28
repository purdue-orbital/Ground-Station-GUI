#! /usr/bin/python3.6
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import queue

class AltitudeGraph:
    def __init__(self):
        # DARK THEME!!!!!
        plt.style.use('dark_background')
        # Crappy code so it can close properly
        self.fig2, self.axs = plt.subplots()
        # Adjust the space so there is more space  
        plt.tight_layout()
        plt.subplots_adjust(wspace=0, hspace=0)

        # Start in interactive mode so that the graph starts in a non blocking thread
        # TODO Init should not open, rather initialize variables
        # plt.ion()

        self.axs.set_xlabel("Time (s)")
        self.axs.set_ylabel("Altitude (m)")
        self.axs.set_title("Altitude vs Time")

        # # Run the loop so the graph gets updated every second
        # while True:
        #     # Random data for now
        #     r = random.randint(-50,50)
        #     # Call methods for each graph to update x,y,z
        #     self.update_altitude(r)
        #     # Sleep for a second, will probably be replaced with a callback or something
        #     # ! Do not get rid of the pause, it messes it up for some reason
        #     time.sleep(1)

    def update_altitude(self, alt_queue):
        plt.pause(0.001)
        self.axs.cla()
        self.axs.set_xlabel("Time (s)")
        self.axs.set_ylabel("Altitude (m)")
        self.axs.set_title("Altitude vs Time")
        # FIXME You pass in an int, not an object with a queue attribute......
        # self.axs.plot(list(alt_queue.queue), 'xkcd:cyan')
