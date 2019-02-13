import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np

fig = plt.figure()

# def animate(i):
#     pullData = open("sampleText.txt","r").read()
#     dataArray = pullData.split('\n')
#     xar = [5,6,7,8,9,34,12,13,43]
#     yar = [5,6,7,3,1,3,4,2,1,2]
#     for eachLine in dataArray:
#         if len(eachLine)>1:
#             x,y = eachLine.split(',')
#             xar.append(int(x))
#             yar.append(int(y))
#     ax1.clear()
#     ax1.plot(xar,yar)
# ani = animation.FuncAnimation(fig, animate, interval=1000)
t = np.arange(0, 50, 1)
s = [5,7,10,15]
fig, axs = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True)
plt.axes(axs[0,0])
plt.plot([5,7,10,15])
plt.ylabel("Acceleration (m/s^2)")
plt.xlabel("Balloon")
plt.axes(axs[1,0])
plt.ylabel("Gyro (degrees/s)")
plt.plot([5,10,15])
plt.axes(axs[0,1])
plt.xlabel("Rocket")
plt.plot([5,10,15])
plt.axes(axs[1,1])
plt.plot([5,10,15])
plt.axes(axs[0,2])
plt.xlabel("Stratologger")
plt.plot([5,10,15])
plt.axes(axs[1,2])
plt.plot([5,10,15])
plt.show()