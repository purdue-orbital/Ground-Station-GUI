#! /usr/bin/python3.6
import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import queue

# ! Thread this function
# Function to update the graph
def updateAltitude(alt):
    alititudeQ.get()
    alititudeQ.put(alt)
    ax1.clear()
    ax1.plot(list(alititudeQ.queue))
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Altitude (m)")
    ax1.set_title("Altitude vs Time")

root = tk.Tk()

# DARK THEME!!!!!
plt.style.use('dark_background')

# initialize the queue to 0
alititudeQ = queue.Queue()
amount_of_point_to_graph = 20
for i in range(0, amount_of_point_to_graph):
    alititudeQ.put(0)

# Initialize the data frame and attack it to tk
df1 = DataFrame(list(alititudeQ.queue))
figure1 = plt.Figure(figsize=(50, 50), dpi=250)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

# Start the animation and run tk
updateAltitude(1)
root.mainloop()
