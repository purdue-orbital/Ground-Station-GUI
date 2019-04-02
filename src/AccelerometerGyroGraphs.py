#! /usr/bin/python3.6
import matplotlib.pyplot as plt
import queue
import random
import time

def update_baloon_acc(x, y, z):
    plt.sca(axs[0,0])
    plt.cla()
    plt.ylabel("Acceleration (m/s^2)")
    plt.title("Balloon")
    baloon_acc_xQ.get()
    baloon_acc_xQ.put(x)
    baloon_acc_yQ.get()
    baloon_acc_yQ.put(y)
    baloon_acc_zQ.get()
    baloon_acc_zQ.put(z)
    plt.plot(list(baloon_acc_xQ.queue), 'xkcd:yellow')
    plt.plot(list(baloon_acc_yQ.queue), 'xkcd:cyan')
    plt.plot(list(baloon_acc_zQ.queue), 'xkcd:fuchsia')

def update_baloon_gyro(x, y, z):
    plt.sca(axs[1,0])
    plt.cla()
    plt.ylabel("Gyro (degrees/s)")
    baloon_gyro_xQ.get()
    baloon_gyro_xQ.put(x)
    baloon_gyro_yQ.get()
    baloon_gyro_yQ.put(y)
    baloon_gyro_zQ.get()
    baloon_gyro_zQ.put(z)
    plt.plot(list(baloon_gyro_xQ.queue), 'xkcd:yellow')
    plt.plot(list(baloon_gyro_yQ.queue), 'xkcd:cyan')
    plt.plot(list(baloon_gyro_zQ.queue), 'xkcd:fuchsia')

def update_rocket_acc(x, y, z):
    plt.sca(axs[0,1])
    plt.cla()
    plt.xlabel("Time (s)")
    plt.title("Rocket")
    rocket_acc_xQ.get()
    rocket_acc_xQ.put(x)
    rocket_acc_yQ.get()
    rocket_acc_yQ.put(y)
    rocket_acc_zQ.get()
    rocket_acc_zQ.put(z)
    plt.plot(list(rocket_acc_xQ.queue), 'xkcd:yellow')
    plt.plot(list(rocket_acc_yQ.queue), 'xkcd:cyan')
    plt.plot(list(rocket_acc_zQ.queue), 'xkcd:fuchsia')

def update_rocket_gyro(x, y, z):
    plt.sca(axs[1,1])
    plt.cla()
    plt.xlabel("Time (s)")
    rocket_gyro_xQ.get()
    rocket_gyro_xQ.put(x)
    rocket_gyro_yQ.get()
    rocket_gyro_yQ.put(y)
    rocket_gyro_zQ.get()
    rocket_gyro_zQ.put(z)
    plt.plot(list(rocket_gyro_xQ.queue), 'xkcd:yellow')
    plt.plot(list(rocket_gyro_yQ.queue), 'xkcd:cyan')
    plt.plot(list(rocket_gyro_zQ.queue), 'xkcd:fuchsia')

def handle_close(event):
    global shouldClose
    shouldClose = True    


# DARK THEME!!!!!
plt.style.use('dark_background')

# Graph 6 plots in a 2x3 fashion
fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)

# Crappy code so it can close properly
fig.canvas.mpl_connect('close_event', handle_close)
shouldClose = False


# Adjust the space so there is more space  
plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Start in interactive mode so that the graph starts in a non blocking thread
plt.ion()

# Create several queue that holds the number for each line in every graph
baloon_acc_xQ = queue.Queue()
baloon_acc_yQ = queue.Queue()
baloon_acc_zQ = queue.Queue()
baloon_gyro_xQ = queue.Queue()
baloon_gyro_yQ = queue.Queue()
baloon_gyro_zQ = queue.Queue()
rocket_acc_xQ = queue.Queue()
rocket_acc_yQ = queue.Queue()
rocket_acc_zQ = queue.Queue()
rocket_gyro_xQ = queue.Queue()
rocket_gyro_yQ = queue.Queue()
rocket_gyro_zQ = queue.Queue()

# Fill the queue with 0s so that we can graph something if the user opens the graph early
amount_of_point_to_graph = 20
for i in range(0, amount_of_point_to_graph):
    baloon_acc_xQ.put(0)
    baloon_acc_yQ.put(0)
    baloon_acc_zQ.put(0)
    baloon_gyro_xQ.put(0)
    baloon_gyro_yQ.put(0)
    baloon_gyro_zQ.put(0)
    rocket_acc_xQ.put(0)
    rocket_acc_yQ.put(0)
    rocket_acc_zQ.put(0)
    rocket_gyro_xQ.put(0)
    rocket_gyro_yQ.put(0)
    rocket_gyro_zQ.put(0)

#Setup titles, axis labels, and plot the initial 0s
plt.sca(axs[0,0])
plt.plot(list(baloon_acc_xQ.queue))
plt.plot(list(baloon_acc_yQ.queue))
plt.plot(list(baloon_acc_zQ.queue))
plt.ylabel("Acceleration (m/s^2)")
plt.title("Balloon")

plt.sca(axs[1,0])
plt.plot(list(baloon_gyro_xQ.queue))
plt.plot(list(baloon_gyro_yQ.queue))
plt.plot(list(baloon_gyro_zQ.queue))
plt.ylabel("Gyro (degrees/s)")

plt.sca(axs[0,1])
plt.xlabel("Time (s)")
plt.title("Rocket")
plt.plot(list(rocket_acc_xQ.queue))
plt.plot(list(rocket_acc_yQ.queue))
plt.plot(list(rocket_acc_zQ.queue))

plt.sca(axs[1,1])
plt.xlabel("Time (s)")
plt.plot(list(rocket_gyro_xQ.queue))
plt.plot(list(rocket_gyro_yQ.queue))
plt.plot(list(rocket_gyro_zQ.queue))

# Run the loop so the graph gets updated every second
while True:
    # Random data for now
    x = random.randint(-50,50)
    y = random.randint(-50,50)
    z = random.randint(-50,50)
    # Call methods for each graph to update x,y,z
    update_baloon_acc(x, y, z)
    update_baloon_gyro(x, y, z)
    update_rocket_acc(x, y, z)
    update_rocket_gyro(x, y, z)
    # Sleep for a second, will probably be replaced with a callback or something
    # ! Do not get rid of the pause, it messes it up for some reason
    plt.pause(0.001)
    time.sleep(1)