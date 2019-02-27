#! /usr/bin/python3.6
import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import random
import queue

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
figure1 = plt.Figure(figsize=(5,5), dpi=100)
ax1 = figure1.add_subplot(231)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

figure2 = plt.Figure(figsize=(5,5), dpi=100)
ax2 = figure2.add_subplot(232)
bar2 = FigureCanvasTkAgg(figure2, root)
bar2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

figure3 = plt.Figure(figsize=(5,5), dpi=100)
ax3 = figure3.add_subplot(233)
bar3 = FigureCanvasTkAgg(figure3, root)
bar3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

figure4 = plt.Figure(figsize=(5,5), dpi=100)
ax4 = figure4.add_subplot(234)
bar4 = FigureCanvasTkAgg(figure4, root)
bar4.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

figure5 = plt.Figure(figsize=(25,25), dpi=100)
ax5 = figure5.add_subplot(235)
bar5 = FigureCanvasTkAgg(figure5, root)
bar5.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

figure6 = plt.Figure(figsize=(25,25), dpi=100)
ax6 = figure6.add_subplot(236)
bar6 = FigureCanvasTkAgg(figure6, root)
bar6.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)


# Function to update the graph, we call it every second, should be replaced with a callback
def animate(i):
    alititudeQ.get()
    alititudeQ.put(random.randint(-50, 50))
    ax1.clear()
    ax1.plot(list(alititudeQ.queue))
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Altitude (m)")
    ax1.set_title("Altitude vs Time")

# Start the animation and run tk
ani = animation.FuncAnimation(figure1, animate, interval=2000)
root.mainloop()
