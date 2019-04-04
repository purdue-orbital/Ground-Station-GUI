#! /usr/bin/python3.6
import matplotlib.pyplot as plt
import queue
import random
import time


class AccelerometerGyroGraphs:
    # def open_graphs(self):
    #     self.update_balloon_acc(-8,-9,-10)
    #     self.update_balloon_gyro(-3,-4,-5)
    #     self.update_rocket_acc(3,4,5)
    #     self.update_rocket_gyro(8,9,10)

    def update_balloon_acc(self, x_queue, y_queue, z_queue):
        self.ax_ba.cla()
        self.ax_ba.set_ylabel("Acceleration (m/s^2)")
        self.ax_ba.set_title("Balloon")
        # self.balloon_acc_xQ.get()
        # self.balloon_acc_xQ.put(x)
        # self.balloon_acc_yQ.get()
        # self.balloon_acc_yQ.put(y)
        # self.balloon_acc_zQ.get()
        # self.balloon_acc_zQ.put(z)
        self.ax_ba.plot(list(x_queue.queue), 'xkcd:yellow')
        self.ax_ba.plot(list(y_queue.queue), 'xkcd:cyan')
        self.ax_ba.plot(list(z_queue.queue), 'xkcd:fuchsia')
        plt.pause(0.001)

    def update_balloon_gyro(self, x_queue, y_queue, z_queue):
        self.ax_bg.cla()
        self.ax_bg.set_ylabel("Gyro (degrees/s)")
        # self.balloon_gyro_xQ.get()
        # self.balloon_gyro_xQ.put(x)
        # self.balloon_gyro_yQ.get()
        # self.balloon_gyro_yQ.put(y)
        # self.balloon_gyro_zQ.get()
        # self.balloon_gyro_zQ.put(z)
        self.ax_bg.plot(list(x_queue.queue), 'xkcd:yellow')
        self.ax_bg.plot(list(y_queue.queue), 'xkcd:cyan')
        self.ax_bg.plot(list(z_queue.queue), 'xkcd:fuchsia')
        plt.pause(0.001)

    def update_rocket_acc(self, x_queue, y_queue, z_queue):
        self.ax_ra.cla()
        self.ax_ra.set_xlabel("Time (s)")
        self.ax_ra.set_title("Rocket")
        # self.rocket_acc_xQ.get()
        # self.rocket_acc_xQ.put(x)
        # self.rocket_acc_yQ.get()
        # self.rocket_acc_yQ.put(y)
        # self.rocket_acc_zQ.get()
        # self.rocket_acc_zQ.put(z)
        self.ax_ra.plot(list(x_queue.queue), 'xkcd:yellow')
        self.ax_ra.plot(list(y_queue.queue), 'xkcd:cyan')
        self.ax_ra.plot(list(z_queue.queue), 'xkcd:fuchsia')
        plt.pause(0.001)

    def update_rocket_gyro(self, x_queue, y_queue, z_queue):
        self.ax_rg.cla()
        self.ax_rg.set_xlabel("Time (s)")
        # self.rocket_gyro_xQ.get()
        # self.rocket_gyro_xQ.put(x)
        # self.rocket_gyro_yQ.get()
        # self.rocket_gyro_yQ.put(y)
        # self.rocket_gyro_zQ.get()
        # self.rocket_gyro_zQ.put(z)
        self.ax_rg.plot(list(x_queue.queue), 'xkcd:yellow')
        self.ax_rg.plot(list(y_queue.queue), 'xkcd:cyan')
        self.ax_rg.plot(list(z_queue.queue), 'xkcd:fuchsia')
        plt.pause(0.001)

    def __init__(self):
        # DARK THEME!!!!!
        plt.style.use('dark_background')

        # Graph 6 plots in a 2x3 fashion
        self.fig, [[self.ax_ba, self.ax_ra], [self.ax_bg, self.ax_rg]] = plt.subplots(nrows=2, ncols=2, sharex=True,
                                                                                      sharey=True)

        # Crappy code so it can close properly
        # self.fig.canvas.mpl_connect('close_event', handle_close)
        # shouldClose = False

        # Adjust the space so there is more space  
        plt.tight_layout()
        plt.subplots_adjust(wspace=0, hspace=0)

        # Start in interactive mode so that the graph starts in a non blocking thread
        plt.ion()

        # Fill the queue with 0s so that we can graph something if the user opens the graph early

        # Setup titles, axis labels, and plot the initial 0s
        # self.ax_ba.plot(list(self.balloon_acc_xQ.queue))
        # self.ax_ba.plot(list(self.balloon_acc_yQ.queue))
        # self.ax_ba.plot(list(self.balloon_acc_zQ.queue))
        self.ax_ba.set_ylabel("Acceleration (m/s^2)")
        self.ax_ba.set_title("Balloon")

        # self.ax_bg.plot(list(self.balloon_gyro_xQ.queue))
        # self.ax_bg.plot(list(self.balloon_gyro_yQ.queue))
        # self.ax_bg.plot(list(self.balloon_gyro_zQ.queue))
        self.ax_bg.set_ylabel("Gyro (degrees/s)")

        self.ax_ra.set_xlabel("Time (s)")
        self.ax_ra.set_title("Rocket")
        # self.ax_ra.plot(list(self.rocket_acc_xQ.queue))
        # self.ax_ra.plot(list(self.rocket_acc_yQ.queue))
        # self.ax_ra.plot(list(self.rocket_acc_zQ.queue))

        self.ax_rg.set_xlabel("Time (s)")
        # self.ax_rg.plot(list(self.rocket_gyro_xQ.queue))
        # self.ax_rg.plot(list(self.rocket_gyro_yQ.queue))
        # self.ax_rg.plot(list(self.rocket_gyro_zQ.queue))

        # # Run the loop so the graph gets updated every second
        # while True:
        #     # Random data for now
        #     x = random.randint(-50,50)
        #     y = random.randint(-50,50)
        #     z = random.randint(-50,50)
        #     # Call methods for each graph to update x,y,z
        #     update_balloon_acc(x, y, z)
        #     update_baboon_gyro(x, y, z)
        #     update_rocket_acc(x, y, z)
        #     update_rocket_gyro(x, y, z)
        #     # Sleep for a second, will probably be replaced with a callback or something
        #     # ! Do not get rid of the pause, it messes it up for some reason
        #     plt.pause(0.001)
        #     time.sleep(1)
