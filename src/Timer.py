import time
import tkinter as tk
from tkinter import *

milliseconds = 0;
seconds = 0;
minutes = 0;
hours = 0;
start = time.time()
# your code


def tick():
    global milliseconds, seconds, minutes, hours, start
    currTime = str(time.time() - start)
    dot = currTime.find('.')
    milliseconds = currTime[dot+1:dot+3]
    seconds = int(currTime[:dot])
    minutes = int(seconds)//60
    seconds = int(seconds)%60
    hours = int(minutes)//60
    minutes = int(minutes)%60

    #print(str(hours)+":"+str(minutes)+":"+str(seconds)+":"+str(milliseconds))
    clock_frame.config(text=str(hours).zfill(2)+":"+str(minutes).zfill(2)+":"+str(seconds).zfill(2)+":"+str(milliseconds).zfill(2))
    clock_frame.after(10, tick)

root = tk.Tk()
root.title('Clock')
clock_frame = tk.Label(root, font=('times', 100, 'bold'), bg='black', fg='green')
clock_frame.pack(fill='both', expand=1)
root.geometry('700x500')
tick()
root.mainloop()
