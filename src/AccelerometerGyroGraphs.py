import matplotlib.pyplot as plt
import matplotlib.animation as animation
import queue
import time

def update_baloon_acc(x, y, z):
    return 0

def update_baloon_gyro(x, y, z):
    return 0

def update_rocket_acc(x, y, z):
    return 0

def update_rocket_gyro(x, y, z):
    return 0

def update_strato_acc(x, y, z):
    return 0

def update_strato_gyro(x, y, z):
    return 0


# DARK THEME!!!!!
plt.style.use('dark_background')

# Graph 6 plots in a 2x3 fashion
fig, axs = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True)

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
strato_acc_xQ = queue.Queue()
strato_acc_yQ = queue.Queue()
strato_acc_zQ = queue.Queue()
strato_gyro_xQ = queue.Queue()
strato_gyro_yQ = queue.Queue()
strato_gyro_zQ = queue.Queue()

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
    strato_acc_xQ.put(0)
    strato_acc_yQ.put(0)
    strato_acc_zQ.put(0)
    strato_gyro_xQ.put(0)
    strato_gyro_yQ.put(0)
    strato_gyro_zQ.put(0)

#Setup titles, axis labels, and plot the initial 0s
baloon_acc_graph = plt.sca(axs[0,0])
plt.plot(list(baloon_acc_xQ.queue))
plt.plot(list(baloon_acc_yQ.queue))
plt.plot(list(baloon_acc_zQ.queue))
plt.ylabel("Acceleration (m/s^2)")
plt.title("Balloon")

baloon_gyro_graph = plt.sca(axs[1,0])
plt.plot(list(baloon_gyro_xQ.queue))
plt.plot(list(baloon_gyro_yQ.queue))
plt.plot(list(baloon_gyro_zQ.queue))
plt.ylabel("Gyro (degrees/s)")

rocket_acc_graph = plt.sca(axs[0,1])
plt.title("Rocket")
plt.plot(list(rocket_acc_xQ.queue))
plt.plot(list(rocket_acc_yQ.queue))
plt.plot(list(rocket_acc_zQ.queue))

rocket_gyro_graph = plt.sca(axs[1,1])
plt.xlabel("Time (s)")
plt.plot(list(rocket_gyro_xQ.queue))
plt.plot(list(rocket_gyro_yQ.queue))
plt.plot(list(rocket_gyro_zQ.queue))

stato_acc_graph = plt.sca(axs[0,2])
plt.title("Stratologger")
plt.plot(list(strato_acc_xQ.queue))
plt.plot(list(strato_acc_yQ.queue))
plt.plot(list(strato_acc_zQ.queue))

plt.sca(axs[1,2])
plt.plot(list(strato_gyro_xQ.queue))
plt.plot(list(strato_gyro_yQ.queue))
plt.plot(list(strato_gyro_zQ.queue))

# Run the loop so the graph gets updated every second
while True:
    plt.pause(0.001)
    time.sleep(1)