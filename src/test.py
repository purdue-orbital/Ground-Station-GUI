# THIS SHOULD ONLY BE USED FOR TESTING REMOVED THIS AFTER DONE WITH IT
import matplotlib.pyplot as plt
import numpy as np
import threading
import random
import queue
import time

def looper():    
    # i as interval in seconds      
    while True:
        ax.cla()
        print("Called")
        q.put(random.randint(-50,50))
        print("Called1")
        q.get()
        print("Called2")
        ax.plot(list(q.queue))
        print("Called3")
        fig.canvas.draw()
        print("Called4")
        fig.canvas.flush_events()
        print("Called5")
        time.sleep(1)

# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
line1 = ax.plot([1,2,3,4,5])
q = queue.Queue()
for i in range(50):
    q.put(i)
print("Hello")

looper()
# for phase in np.linspace(0, 314, 100):
#     ax.plot([1,3,4,5,6])
#     fig.canvas.draw()
#     fig.canvas.flush_events()

