import datetime
import os
import time
import serial
import RPi.GPIO as GPIO
from tkinter import *
from tkinter import messagebox

"""
ROCKET GUI Version 0.1

Author: Ken Sodetz
Since: 10/11/2017

Created for Purdue Orbital Electrical and Software Sub team

Parses and displays data from the a Raspberry Pi 3 to verbosely
display all pertinent system data (data that can be changed) and environmental 
data (data that cannot be changed). 

"""

# Set up GPIO pins for use, see documentation for pin layout

# orange wire
launch_signal = 11
# yellow wire
on_signal = 12
# white wire
gui_switch = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(launch_signal, GPIO.IN)
GPIO.setup(on_signal, GPIO.OUT)
GPIO.setup(gui_switch, GPIO.OUT)

GPIO.output(on_signal, GPIO.HIGH)
GPIO.output(on_signal, GPIO.LOW)
GPIO.output(gui_switch, GPIO.LOW)

# Set window options
top = Tk()
top.geometry("600x600")
hxw = 600  # height and width of top frame
top.title("Ground Station Graphical User Interface V0.1")

# ============================ #
# ========== FRAMES ========== #
# ============================ #

# Initialize uppermost frame
frame = Frame(top, width=hxw, height=hxw, bg="#333333")
frame.pack(fill='both', expand='yes')

# Initialize and place subFrameLeft
subFrameLeft = Frame(top, bg="#3C3F41", height="300", width=hxw / 2 - 5, relief=RAISED)
subFrameLeft.place(x=0, y=5)

# Initialize and place subFrameRight
subFrameRight = Frame(top, bg="#3C3F41", height="300", width=hxw / 2 - 5, relief=RAISED)
subFrameRight.place(x=hxw / 2 + 5, y=5)

# Initialize and place subFrameBottom
subFrameBottom = Frame(top, bg="#3C3F41", height="200", width=hxw, relief=RAISED)
subFrameBottom.place(x=0, y=hxw - 285)

# ============================ #
# ==== MENU BAR & COMMANDS === #
# ============================ #

# Text for 'About' menu item
aboutText = "Ground Station Graphical User Interface Version 0.1\n\n" \
            "Author: Ken Sodetz\n" \
            "Since: 10/11/2017\n\n" \
            "Created for Purdue Orbital Electrical and Software Sub team\n\n" \
            "Parses and displays data from the a Raspberry Pi 3 to verbosely display all\npertinent system data " \
            "(data that can be changed) and environmental data\n(data that cannot be changed)"


# Temp menu item
def doNothing():
    file_window = Toplevel(top)
    button = Button(file_window, text="Close", command=lambda: close_window(file_window))
    button.pack()


# Log menu item method
def log_menu():
    log_window = Toplevel(top)
    log_window.title("Log")
    loggedLabel = Label(log_window, text="The current variables have been logged in 'status_log.txt'")
    loggedLabel.pack()
    button = Button(log_window, text="Close", command=lambda: close_window(log_window))
    button.pack()
    log("MANUAL")


# About menu item method
def about():
    about_window = Toplevel(top)
    about_window.title("About")
    about_window.resizable(width=False, height=False)
    text = Text(about_window)
    text.insert(INSERT, aboutText)
    text.config(state=DISABLED)
    text.pack()
    top.img = img = PhotoImage(file="PurdueOrbitalLogoSmall.gif")
    logo = Label(about_window, image=img)
    logo.place(x=220, y=200)
    button = Button(about_window, text="Close", command=lambda: close_window(about_window))
    button.pack()


# Close menu window method
def close_window(window):
    window.destroy()


# Restart program method
def restart_program():
    python = sys.executable
    GPIO.output(gui_switch, GPIO.LOW)
    GPIO.cleanup()
    log("RESTART")
    os.execl(python, python, *sys.argv)


# Reset variables window
def reset_variables_window():
    reset_window = messagebox.askokcancel("Reset All Variables?", "Are you sure you want to reset all variables?")
    if reset_window:
        log("RESET")
        reset_variables()
        updateEnvironment()
        global verify_ok_to_launch
        verify_ok_to_launch = False
        statusLabelChange("NOT VERIFIED")
        abortButton.config(state=DISABLED)


# Reset all variables
def reset_variables():
    GPIO.output(gui_switch, GPIO.LOW)
    global temperature
    temperature = 0.0
    global pressure
    pressure = 0.0
    global humidity
    humidity = 0.0
    global altitude
    altitude = 0.0
    global direction
    direction = 0.0
    global acceleration
    acceleration = 0.0
    global velocity
    velocity = 0.0
    global angle_result
    angle_result = "null"


# Menu Bar
menuBar = Menu(top)

# File Menu
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Restart", command=restart_program)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=top.quit)
menuBar.add_cascade(label="File", menu=fileMenu)

# Program Menu
programMenu = Menu(menuBar, tearoff=0)
programMenu.add_command(label="Reset", command=reset_variables_window)
programMenu.add_command(label="Log", command=log_menu)
menuBar.add_cascade(label="Program", menu=programMenu)

# Help Menu
helpMenu = Menu(menuBar, tearoff=0)
helpMenu.add_command(label="Help Index", command=doNothing)
helpMenu.add_separator()
helpMenu.add_command(label="About", command=about)
menuBar.add_cascade(label="Help", menu=helpMenu)

top.config(menu=menuBar)


# ============================ #
# ======= STATUS LOGS ======== #
# ============================ #

def log(status):
    fo = open("status_log.txt", "a")
    currentDate = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    if status == "ABORT":
        fo.write("-------MISSION ABORTED-------\n")
    elif status == "VERIFIED":
        fo.write("-------STATUS VERIFIED-------\n")
    elif status == "MANUAL":
        fo.write("-----MANUAL LOG INVOKED------\n")
    elif status == "RESET":
        fo.write("-------VARIABLES RESET-------\n")
    elif status == "RESTART":
        fo.write("-------PROGRAM RESTART-------\n")
    else:
        fo.write("-----STATUS NOT VERIFIED-----\n")

    fo.write("TIMESTAMP:" + currentDate + "\n")
    fo.write("*****************************\n")
    fo.write("----------LOGS START---------\n")
    fo.write("temperature = " + repr(temperature) + "\n")
    fo.write("pressure = " + repr(pressure) + "\n")
    fo.write("humidity = " + repr(humidity) + "\n")
    fo.write("altitude = " + repr(altitude) + "\n")
    fo.write("direction = " + repr(direction) + "\n")
    fo.write("acceleration = " + repr(acceleration) + "\n")
    fo.write("velocity = " + repr(velocity) + "\n")
    fo.write("horizontalAngle = " + repr(angle_result) + "\n")
    fo.write("----------LOGS END-----------\n")
    fo.write("-----------------------------\n\n")
    fo.close()


# ============================ #
# ===== GLOBAL VARIABLES ===== #
# ============================ #

is_launched = False  # has the rocket launched?
has_aborted = False  # has the process been aborted?
verify_ok_to_launch = False  # is the system verified for launch?
bgColor = "#333333"  # background color
subFrameColor = "#3C3F41"  # sub frame background color
standardTextWidth = 18  # standard text width
standardDataWidth = 10  # standard data width
# angle_result = "null"

# Environmental Variables (currently placeholders)
temperature = 26.6
pressure = 101.325
humidity = 67.2

# System Variables (currently placeholders)
altitude = 1024.45
direction = 36
acceleration = 3.06
velocity = 5.01
angle_result = 46.0

# ============================ #
# ========== LABELS ========== #
# ============================ #

# # Abort Mission Label
# abortLabel = Label(subFrameBottom, text="Abort Mission:", bg=bgColor, fg="white")
# abortLabel.place(x=10, y=55)
#
# # Verify Launch Label
# verifyLabel = Label(subFrameBottom, text="Verify Launch:", bg=bgColor, fg="white")
# verifyLabel.place(x=10, y=125)

# Status Label to show real time status
statusLabel = Label(subFrameBottom, text="NOT VERIFIED", fg="orange", bg="#808080", width="20", height="2")
statusLabel.place(x=hxw / 2 + hxw / 8, y=80)

# Label to mark status
statusTextLabel = Label(subFrameBottom, text="Current Status:", fg="white", bg=bgColor)
statusTextLabel.place(x=hxw / 2 + hxw / 8 + 30, y=50)

# SubFrameLeft Label: Environmental Data
frameLeftLabel = Label(subFrameLeft, text="Environmental Data:", fg="white", bg=subFrameColor)
frameLeftLabel.place(x=(hxw / 2) / 4 + 15, y=5)

# SubFrameLeft Label: System Data
frameRightLabel = Label(subFrameRight, text="System Data:", fg="white", bg=subFrameColor)
frameRightLabel.place(x=(hxw / 2) / 4 + 20, y=5)

# Temperature Label
tempLabel = Label(subFrameLeft, text="Temperature (Celsius): ", fg="white", bg=bgColor, width=standardTextWidth)
tempLabel.place(x=10, y=40)

# Temperature Data
tempDataLabel = Label(subFrameLeft, text=temperature, fg="white", bg=bgColor, width=standardDataWidth)
tempDataLabel.place(x=160, y=40)

# Altitude Label
altLabel = Label(subFrameRight, text="Altitude (Meters): ", fg="white", bg=bgColor, width=standardTextWidth)
altLabel.place(x=10, y=40)

# Altitude Data
altDataLabel = Label(subFrameRight, text=altitude, fg="white", bg=bgColor, width=standardDataWidth)
altDataLabel.place(x=160, y=40)

# Pressure Label
pressureLabel = Label(subFrameLeft, text="Pressure (kPa): ", fg="white", bg=bgColor, width=standardTextWidth)
pressureLabel.place(x=10, y=80)

# Pressure Data
pressureDataLabel = Label(subFrameLeft, text=pressure, fg="white", bg=bgColor, width=standardDataWidth)
pressureDataLabel.place(x=160, y=80)

# Cardinal Direction Label
cardinalLabel = Label(subFrameRight, text="Direction (°): ", fg="white", bg=bgColor, width=standardTextWidth)
cardinalLabel.place(x=10, y=80)

# Cardinal Direction Data
cardinalDataLabel = Label(subFrameRight, text=direction, fg="white", bg=bgColor, width=standardDataWidth)
cardinalDataLabel.place(x=160, y=80)

# Humidity Label
humidLabel = Label(subFrameLeft, text="Humidity (Percent): ", fg="white", bg=bgColor, width=standardTextWidth)
humidLabel.place(x=10, y=120)

# Humidity Data
humidityDataLabel = Label(subFrameLeft, text=humidity, fg="white", bg=bgColor, width=standardDataWidth)
humidityDataLabel.place(x=160, y=120)

# Acceleration Label
accLabel = Label(subFrameRight, text="Acceleration (M/s/s): ", fg="white", bg=bgColor, width=standardTextWidth)
accLabel.place(x=10, y=120)

# Acceleration Data
accDataLabel = Label(subFrameRight, text=acceleration, fg="white", bg=bgColor, width=standardDataWidth)
accDataLabel.place(x=160, y=120)

# Velocity Label
velocityLabel = Label(subFrameRight, text="Velocity (M/s): ", fg="white", bg=bgColor, width=standardTextWidth)
velocityLabel.place(x=10, y=160)

# Velocity Data
velocityDataLabel = Label(subFrameRight, text=velocity, fg="white", bg=bgColor, width=standardDataWidth)
velocityDataLabel.place(x=160, y=160)

# Angle Label
angleLabel = Label(subFrameRight, text="Angle (°): ", fg="white", bg=bgColor, width=standardTextWidth)
angleLabel.place(x=10, y=200)

# Angle Data
angleDataLabel = Label(subFrameRight, text=angle_result, fg="white", bg=bgColor, width=standardDataWidth)
angleDataLabel.place(x=160, y=200)

# Angle Entry Label
angleEntryLabel = Label(subFrameLeft, text="Positive angle between 30° and 75°", fg="white", bg=subFrameColor,
                        width=26)
angleEntryLabel.place(x=40, y=230)


# ============================ #
# == UPDATE LABEL FUNCTIONS == #
# ============================ #

# Function to change status label
def statusLabelChange(change_to):
    statusLabel.config(text=change_to)
    if change_to == "VERIFIED":
        statusLabel.config(fg="green")
    elif change_to == "NOT VERIFIED":
        statusLabel.config(fg="orange")
    elif change_to == "MISSION ABORTED":
        statusLabel.config(fg="red")


# Function to show abort message box
def abortMessageCallBack():
    abort_response = messagebox.askyesno("Abort Mission?", "Do you really want to abort the mission?")
    if abort_response:
        global has_aborted
        has_aborted = True
        global verify_ok_to_launch
        verify_ok_to_launch = False
        statusLabelChange("MISSION ABORTED")
        abortButton.config(state=DISABLED)
        log("ABORT")
        GPIO.output(gui_switch, GPIO.LOW)
    else:
        has_aborted = False


# Function to show verify message box
def verifyMessageCallBack():
    verify_response = messagebox.askyesno("Verify Launch", "Do you want to verify for launch?")
    if verify_response:
        global verify_ok_to_launch
        verify_ok_to_launch = True
        abortButton.config(state=NORMAL)
        statusLabelChange("VERIFIED")
        log("VERIFIED")
        GPIO.output(gui_switch, GPIO.HIGH)
    else:
        verify_ok_to_launch = False
        statusLabelChange("NOT VERIFIED")
        abortButton.config(state=DISABLED)
        log("NOT")


def getAngle():
    this_angle_result = angleEntry.get()
    global angle_result
    if len(angleEntry.get()) > 0 and 30.0 <= float(this_angle_result) <= 75.0:
        angle_result = float(this_angle_result)
        if 30.0 <= angle_result <= 75.0:
            angleDataLabel.config(text=angle_result)


# Function to update Environment Data
def updateEnvironment():
    tempDataLabel.config(text=temperature)
    pressureDataLabel.config(text=pressure)
    humidityDataLabel.config(text=humidity)
    altDataLabel.config(text=altitude)
    cardinalDataLabel.config(text=direction)
    accDataLabel.config(text=acceleration)
    velocityDataLabel.config(text=velocity)
    angleDataLabel.config(text=angle_result)


# ============================ #
# ==== BUTTONS AND ENTRIES === #
# ============================ #

# Info Text Line
infoText = Label(subFrameBottom, fg="white", bg=bgColor, width=40)
infoText.place(x=160, y=15)


# When mouse hovers over the abort button, show info on the infoText line
def on_enter_abort(event):
    infoText.config(text="Abort Mission Button", fg="red")


# When mouse hovers over the verify button, show info on the infoText line
def on_enter_verify(event):
    infoText.config(text="Verify Mission Button", fg="green")


# When mouse leaves, clear infoText line
def on_leave(event):
    global infoText
    infoText.config(text=" ")


# Abort Mission Button
abortButton = Button(subFrameBottom, text="ABORT MISSION", state=DISABLED, bg="red", command=abortMessageCallBack,
                     width="20")
abortButton.place(x=100, y=55)
abortButton.bind("<Enter>", on_enter_abort)
abortButton.bind("<Leave>", on_leave)

# Verify Launch Button
verifyButton = Button(subFrameBottom, text="VERIFY LAUNCH", bg="green", command=verifyMessageCallBack, cursor="shuttle",
                      width="20")
verifyButton.place(x=100, y=125)
verifyButton.bind("<Enter>", on_enter_verify)
verifyButton.bind("<Leave>", on_leave)

# Angle Entry
angleEntry = Entry(subFrameLeft, bd=5, bg=bgColor, fg="white", width=standardDataWidth, textvariable=angle_result)
angleEntry.place(x=40, y=260)

# Get Angle Input Button
angleInputButton = Button(subFrameLeft, text="ENTER", width=8, command=getAngle)
angleInputButton.place(x=160, y=260)

# Start window
top.mainloop()
GPIO.cleanup()
