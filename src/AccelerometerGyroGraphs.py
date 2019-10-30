#! /usr/bin/python3.6
import matplotlib.pyplot as plt
import queue
import random
import time


class AccelerometerGyroGraphs:

    def __init__(self):
        # DARK THEME!!!!!
        plt.style.use('dark_background')

        # Graph 2 plots in a 2x1 fashion
        self.fig = plt.figure()
        self.ax_ba = self.fig.add_subplot(211)
        self.ax_bg = self.fig.add_subplot(212)

        # Adjust the space so there is more space
        plt.tight_layout()
        plt.subplots_adjust(wspace=0, hspace=0)

        # Start in interactive mode so that the graph starts in a non blocking thread
        plt.ion()

        # Fill the queue with 0s so that we can graph something if the user opens the graph early

        # Setup titles, axis labels, and plot the initial 0s
        self.ax_ba.set_ylabel("Acceleration (m/s^2)")
        self.ax_ba.set_title("Balloon")

        self.ax_bg.set_ylabel("Gyro (degrees/s)")

    def update_balloon_acc(self, x_queue, y_queue, z_queue):
        self.ax_ba.cla()
        self.ax_ba.set_ylabel("Acceleration (m/s^2)")
        self.ax_ba.set_title("Balloon")

        self.ax_ba.plot(list(x_queue.queue), 'xkcd:yellow')
        self.ax_ba.plot(list(y_queue.queue), 'xkcd:cyan')
        self.ax_ba.plot(list(z_queue.queue), 'xkcd:fuchsia')
        plt.pause(0.001)

    def update_balloon_gyro(self, x_queue, y_queue, z_queue):
        self.ax_bg.cla()
        self.ax_bg.set_ylabel("Gyro (degrees/s)")

        self.ax_bg.plot(list(x_queue.queue), 'xkcd:yellow')
        self.ax_bg.plot(list(y_queue.queue), 'xkcd:cyan')
        self.ax_bg.plot(list(z_queue.queue), 'xkcd:fuchsia')
        plt.pause(0.001)
