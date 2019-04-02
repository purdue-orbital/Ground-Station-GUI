#! /usr/bin/python3.6
import matplotlib.pyplot as plt
import queue
import random
import time

class AccelerometerGyroGraphs:
    def open_graphs(self):
        self.update_baloon_acc(0,0,0)
        self.update_baloon_gyro(0,0,0)
        self.update_rocket_acc(0,0,0)
        self.update_rocket_gyro(0,0,0)

    def update_baloon_acc(self, x, y, z):
        plt.sca(self.axs[0,0])
        plt.cla()
        plt.ylabel("Acceleration (m/s^2)")
        plt.title("Balloon")
        self.baloon_acc_xQ.get()
        self.baloon_acc_xQ.put(x)
        self.baloon_acc_yQ.get()
        self.baloon_acc_yQ.put(y)
        self.baloon_acc_zQ.get()
        self.baloon_acc_zQ.put(z)
        plt.plot(list(self.baloon_acc_xQ.queue), 'xkcd:yellow')
        plt.plot(list(self.baloon_acc_yQ.queue), 'xkcd:cyan')
        plt.plot(list(self.baloon_acc_zQ.queue), 'xkcd:fuchsia')
        plt.pause(0.001)

    def update_baloon_gyro(self, x, y, z):
        plt.sca(self.axs[1,0])
        plt.cla()
        plt.ylabel("Gyro (degrees/s)")
        self.baloon_gyro_xQ.get()
        self.baloon_gyro_xQ.put(x)
        self.baloon_gyro_yQ.get()
        self.baloon_gyro_yQ.put(y)
        self.baloon_gyro_zQ.get()
        self.baloon_gyro_zQ.put(z)
        plt.plot(list(self.baloon_gyro_xQ.queue), 'xkcd:yellow')
        plt.plot(list(self.baloon_gyro_yQ.queue), 'xkcd:cyan')
        plt.plot(list(self.baloon_gyro_zQ.queue), 'xkcd:fuchsia')
        plt.pause(0.001)

    def update_rocket_acc(self, x, y, z):
        plt.sca(self.axs[0,1])
        plt.cla()
        plt.xlabel("Time (s)")
        plt.title("Rocket")
        self.rocket_acc_xQ.get()
        self.rocket_acc_xQ.put(x)
        self.rocket_acc_yQ.get()
        self.rocket_acc_yQ.put(y)
        self.rocket_acc_zQ.get()
        self.rocket_acc_zQ.put(z)
        plt.plot(list(self.rocket_acc_xQ.queue), 'xkcd:yellow')
        plt.plot(list(self.rocket_acc_yQ.queue), 'xkcd:cyan')
        plt.plot(list(self.rocket_acc_zQ.queue), 'xkcd:fuchsia')
        plt.pause(0.001)

    def update_rocket_gyro(self, x, y, z):
        plt.sca(self.axs[1,1])
        plt.cla()
        plt.xlabel("Time (s)")
        self.rocket_gyro_xQ.get()
        self.rocket_gyro_xQ.put(x)
        self.rocket_gyro_yQ.get()
        self.rocket_gyro_yQ.put(y)
        self.rocket_gyro_zQ.get()
        self.rocket_gyro_zQ.put(z)
        plt.plot(list(self.rocket_gyro_xQ.queue), 'xkcd:yellow')
        plt.plot(list(self.rocket_gyro_yQ.queue), 'xkcd:cyan')
        plt.plot(list(self.rocket_gyro_zQ.queue), 'xkcd:fuchsia')
        plt.pause(0.001)

    def __init__(self):
        # DARK THEME!!!!!
        plt.style.use('dark_background')

        # Graph 6 plots in a 2x3 fashion
        self.fig, self.axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)

        # Crappy code so it can close properly
        # fig.canvas.mpl_connect('close_event', handle_close)
        # shouldClose = False

        # Adjust the space so there is more space  
        plt.tight_layout()
        plt.subplots_adjust(wspace=0, hspace=0)

        # Start in interactive mode so that the graph starts in a non blocking thread
        plt.ion()

        # Create several queue that holds the number for each line in every graph
        self.baloon_acc_xQ = queue.Queue()
        self.baloon_acc_yQ = queue.Queue()
        self.baloon_acc_zQ = queue.Queue()
        self.baloon_gyro_xQ = queue.Queue()
        self.baloon_gyro_yQ = queue.Queue()
        self.baloon_gyro_zQ = queue.Queue()
        self.rocket_acc_xQ = queue.Queue()
        self.rocket_acc_yQ = queue.Queue()
        self.rocket_acc_zQ = queue.Queue()
        self.rocket_gyro_xQ = queue.Queue()
        self.rocket_gyro_yQ = queue.Queue()
        self.rocket_gyro_zQ = queue.Queue()

        # Fill the queue with 0s so that we can graph something if the user opens the graph early
        amount_of_point_to_graph = 20
        for i in range(0, amount_of_point_to_graph):
            self.baloon_acc_xQ.put(0)
            self.baloon_acc_yQ.put(0)
            self.baloon_acc_zQ.put(0)
            self.baloon_gyro_xQ.put(0)
            self.baloon_gyro_yQ.put(0)
            self.baloon_gyro_zQ.put(0)
            self.rocket_acc_xQ.put(0)
            self.rocket_acc_yQ.put(0)
            self.rocket_acc_zQ.put(0)
            self.rocket_gyro_xQ.put(0)
            self.rocket_gyro_yQ.put(0)
            self.rocket_gyro_zQ.put(0)

        #Setup titles, axis labels, and plot the initial 0s
        plt.sca(self.axs[0,0])
        plt.plot(list(self.baloon_acc_xQ.queue))
        plt.plot(list(self.baloon_acc_yQ.queue))
        plt.plot(list(self.baloon_acc_zQ.queue))
        plt.ylabel("Acceleration (m/s^2)")
        plt.title("Balloon")

        plt.sca(self.axs[1,0])
        plt.plot(list(self.baloon_gyro_xQ.queue))
        plt.plot(list(self.baloon_gyro_yQ.queue))
        plt.plot(list(self.baloon_gyro_zQ.queue))
        plt.ylabel("Gyro (degrees/s)")

        plt.sca(self.axs[0,1])
        plt.xlabel("Time (s)")
        plt.title("Rocket")
        plt.plot(list(self.rocket_acc_xQ.queue))
        plt.plot(list(self.rocket_acc_yQ.queue))
        plt.plot(list(self.rocket_acc_zQ.queue))

        plt.sca(self.axs[1,1])
        plt.xlabel("Time (s)")
        plt.plot(list(self.rocket_gyro_xQ.queue))
        plt.plot(list(self.rocket_gyro_yQ.queue))
        plt.plot(list(self.rocket_gyro_zQ.queue))

        # # Run the loop so the graph gets updated every second
        # while True:
        #     # Random data for now
        #     x = random.randint(-50,50)
        #     y = random.randint(-50,50)
        #     z = random.randint(-50,50)
        #     # Call methods for each graph to update x,y,z
        #     update_baloon_acc(x, y, z)
        #     update_baloon_gyro(x, y, z)
        #     update_rocket_acc(x, y, z)
        #     update_rocket_gyro(x, y, z)
        #     # Sleep for a second, will probably be replaced with a callback or something
        #     # ! Do not get rid of the pause, it messes it up for some reason
        #     plt.pause(0.001)
        #     time.sleep(1)