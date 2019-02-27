import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import time
import random


root = tk.Tk()
Data1 = {
    'xList' : [1,2,3,4,5,6],
    'yList' : [6,5,4,3,2,1]
}

df1 = DataFrame(Data1, columns=['xList', 'yList'])
df1 = df1[['xList', 'yList']].groupby('xList').sum()

figure1 = plt.Figure(figsize=(6, 5), dpi=100)
ax1 = figure1.add_subplot(111)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df1.plot(kind='bar', legend=True, ax=ax1)
# ax1.set_title('Country Vs. GDP Per Capita')

# def func():
#     print("called")
#     ax1.clear()
#     plt.cla()
#     Data1['Country'].pop()
#     Data1['Country'].append(randomword(3))
#     df1 = DataFrame(Data1, columns=['Country', 'GDP_Per_Capita'])
#     df1 = df1[['Country', 'GDP_Per_Capita']].groupby('Country').sum()
#     print("SOmehting : ")
#     print(df1)
#     df1.plot(kind='bar', legend=True, ax=ax1)
#     ax1.set_title('Country Vs. GDP Per Capita')
#     plt.pause(0.001)
#     root.after(1000, func)

num = 7

def animate(i):
    global num
    Data1['xList'].pop()
    num += 1
    Data1['xList'].append(num)
    # Data1['yList'].pop()
    # Data1['yList'].append(random.randint(1,10))
    ax1.clear()
    ax1.plot(Data1['xList'], Data1['yList'])

ani = animation.FuncAnimation(figure1, animate, interval=2000)
root.mainloop()
