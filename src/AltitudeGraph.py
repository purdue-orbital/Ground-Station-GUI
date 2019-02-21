import matplotlib.pyplot as plt
import queue
import random
import time
import sys

def update_altitude(h):
    plt.cla()
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.title("Altitude vs Time")
    alititudeQ.get()
    alititudeQ.put(h)
    fig = plt.plot(list(alititudeQ.queue), 'xkcd:cyan')

def handle_close(event):
    global shouldClose
    shouldClose = True

# DARK THEME!!!!!
plt.style.use('dark_background')

# Crappy code so it can close properly
fig = plt.figure()
fig.canvas.mpl_connect('close_event', handle_close)
shouldClose = False

# Adjust the space so there is more space  
plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

# Start in interactive mode so that the graph starts in a non blocking thread
plt.ion()

alititudeQ = queue.Queue()

# Fill the queue with 0s so that we can graph something if the user opens the graph early
amount_of_point_to_graph = 20
for i in range(0, amount_of_point_to_graph):
    alititudeQ.put(0)

plt.xlabel("Time (s)")
plt.ylabel("Altitude (m)")
plt.title("Altitude vs Time")


# Run the loop so the graph gets updated every second
while not shouldClose:
    # Random data for now
    r = random.randint(-50,50)
    # Call methods for each graph to update x,y,z
    update_altitude(r)
    # Sleep for a second, will probably be replaced with a callback or something
    # ! Do not get rid of the pause, it messes it up for some reason
    plt.pause(0.001)
    time.sleep(1)