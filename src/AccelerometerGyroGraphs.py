#! /usr/bin/python3.6
from tkinter import *
import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import queue

# ! Thread these function
# Functions to update the graphs
def update_baloon_acc(x, y, z):
    baloon_acc_xQ.get()
    baloon_acc_xQ.put(x)
    baloon_acc_yQ.get()
    baloon_acc_yQ.put(y)
    baloon_acc_zQ.get()
    baloon_acc_zQ.put(z)
    ax1.clear()
    ax1.set_ylabel("Acceleration (m/s^2)")
    ax1.set_title("Balloon")
    ax1.plot(list(baloon_acc_xQ.queue), 'xkcd:yellow')
    ax1.plot(list(baloon_acc_yQ.queue), 'xkcd:cyan')
    ax1.plot(list(baloon_acc_zQ.queue), 'xkcd:fuchsia')


def update_strato_acc(x, y, z):
    strato_acc_xQ.get()
    strato_acc_xQ.put(x)
    strato_acc_yQ.get()
    strato_acc_yQ.put(y)
    strato_acc_zQ.get()
    strato_acc_zQ.put(z)
    ax2.set_title("Stratologger")
    ax2.plot(list(strato_acc_xQ.queue), 'xkcd:yellow')
    ax2.plot(list(strato_acc_yQ.queue), 'xkcd:cyan')
    ax2.plot(list(strato_acc_zQ.queue), 'xkcd:fuchsia')


def update_rocket_acc(x, y, z):
    rocket_acc_xQ.get()
    rocket_acc_xQ.put(x)
    rocket_acc_yQ.get()
    rocket_acc_yQ.put(y)
    rocket_acc_zQ.get()
    rocket_acc_zQ.put(z)
    ax3.set_title("Rocket")
    ax3.plot(list(rocket_acc_xQ.queue), 'xkcd:yellow')
    ax3.plot(list(rocket_acc_yQ.queue), 'xkcd:cyan')
    ax3.plot(list(rocket_acc_zQ.queue), 'xkcd:fuchsia')


def update_baloon_gyro(x, y, z):
    baloon_gyro_xQ.get()
    baloon_gyro_xQ.put(x)
    baloon_gyro_yQ.get()
    baloon_gyro_yQ.put(y)
    baloon_gyro_zQ.get()
    baloon_gyro_zQ.put(z)
    ax4.clear()
    ax4.set_ylabel("Gyro (degrees/s)")
    ax4.plot(list(baloon_gyro_xQ.queue), 'xkcd:yellow')
    ax4.plot(list(baloon_gyro_yQ.queue), 'xkcd:cyan')
    ax4.plot(list(baloon_gyro_zQ.queue), 'xkcd:fuchsia')


def update_strato_gyro(x, y, z):
    rocket_gyro_xQ.get()
    rocket_gyro_xQ.put(x)
    rocket_gyro_yQ.get()
    rocket_gyro_yQ.put(y)
    rocket_gyro_zQ.get()
    rocket_gyro_zQ.put(z)
    ax5.set_xlabel("Time (s)")
    ax5.plot(list(rocket_gyro_xQ.queue), 'xkcd:yellow')
    ax5.plot(list(rocket_gyro_yQ.queue), 'xkcd:cyan')
    ax5.plot(list(rocket_gyro_zQ.queue), 'xkcd:fuchsia')


def update_rocket_gyro(x, y, z):
    strato_gyro_xQ.get()
    strato_gyro_xQ.put(x)
    strato_gyro_yQ.get()
    strato_gyro_yQ.put(y)
    strato_gyro_zQ.get()
    strato_gyro_zQ.put(z)
    ax6.plot(list(strato_gyro_xQ.queue), 'xkcd:yellow')
    ax6.plot(list(strato_gyro_yQ.queue), 'xkcd:cyan')
    ax6.plot(list(strato_gyro_zQ.queue), 'xkcd:fuchsia')


root = tk.Tk()

# top 3 graphs
frameTop = Frame(root)
# bottom 3 graphs
frameBot = Frame(root)

# DARK THEME!!!!!
plt.style.use('dark_background')

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

# Initialize the data frame and attack it to tk
figure1 = plt.Figure(figsize=(4.8, 4.8), dpi=100)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, frameTop)
bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

figure2 = plt.Figure(figsize=(4.8, 4.8), dpi=100)
ax2 = figure2.add_subplot(111)
bar2 = FigureCanvasTkAgg(figure2, frameTop)
bar2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

figure3 = plt.Figure(figsize=(4.8, 4.8), dpi=100)
ax3 = figure3.add_subplot(111)
bar3 = FigureCanvasTkAgg(figure3, frameTop)
bar3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

figure4 = plt.Figure(figsize=(4.8, 4.8), dpi=100)
ax4 = figure4.add_subplot(111)
bar4 = FigureCanvasTkAgg(figure4, frameBot)
bar4.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

figure5 = plt.Figure(figsize=(4.8, 4.8), dpi=100)
ax5 = figure5.add_subplot(111)
bar5 = FigureCanvasTkAgg(figure5, frameBot)
bar5.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

figure6 = plt.Figure(figsize=(4.8, 4.8), dpi=100)
ax6 = figure6.add_subplot(111)
bar6 = FigureCanvasTkAgg(figure6, frameBot)
bar6.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

# add both the top 3 and bottom 3 grahps to the main frame
frameTop.pack(fill=tk.BOTH)
frameBot.pack(fill=tk.BOTH)
update_baloon_acc(5, 6, 7)
update_baloon_gyro(5, 6, 7)
update_rocket_acc(5, 6, 7)
update_rocket_gyro(5, 6, 7)
update_strato_acc(5, 6, 7)
update_strato_gyro(5, 6, 7)
root.mainloop()
