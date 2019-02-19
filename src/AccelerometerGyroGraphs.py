import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# DARK THEME!!!!!
plt.style.use('dark_background')

# Graph 6 plots in a 2x3 fashion
fig, axs = plt.subplots(nrows=2, ncols=3, sharex=True, sharey=True)

# Adjust the space so there is more space  
plt.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)

#Setup titles and axis labels

plt.axes(axs[0,0])
plt.plot([5,7,10,15])
plt.ylabel("Acceleration (m/s^2)")
plt.title("Balloon")
plt.axes(axs[1,0])
plt.ylabel("Gyro (degrees/s)")
plt.plot([5,10,15])
plt.axes(axs[0,1])
plt.title("Rocket")
plt.plot([5,10,15])
plt.axes(axs[1,1])
plt.xlabel("Time (s)")
plt.plot([5,10,15])
plt.axes(axs[0,2])
plt.title("Stratologger")
plt.plot([5,10,15])
plt.axes(axs[1,2])
plt.plot([5,10,15])
plt.show()