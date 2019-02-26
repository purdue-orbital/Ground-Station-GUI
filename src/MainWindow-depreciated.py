import datetime
import os
import time
#import serial
#import RPi.GPIO as GPIO
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime
import time
import os

"""
ROCKET GUI Version 0.1

Author: Ken Sodetz
Since: 10/11/2017

Created for Purdue Orbital Electrical and Software Sub team

Parses and displays data from the a Raspberry Pi 3 to verbosely
display all pertinent system data (data that can be changed) and environmental 
data (data that cannot be changed). 

"""

# GLOBALS
DarkGray = "#333333"
LightGray = "#3C3F41"


class DataWindow:
    def __init__(self, name):
        self.name = name
        self.width = 600
        self.height = 600
        self.abort_button_state = DISABLED
        self.status_label_text = "NOT VERIFIED"
        self.status_label_text_color = "orange"
        bgColor = "#333333"
        standardDataWidth = 6

        self.subFrameLeft = Frame(self.name, bg=LightGray, height=self.height / 2, width=self.width / 2 - 5,
                                  relief=RAISED)
        self.subFrameRight = Frame(self.name, bg=LightGray, height=self.height / 2, width=self.width / 2 - 5,
                                   relief=RAISED)
        self.subFrameBottom = Frame(self.name, bg="#3C3F41", height=self.height / 3, width=self.width, relief=RAISED)

        self.abortButton = Button(self.subFrameBottom, text="ABORT MISSION", state=self.abort_button_state, bg="red",
                                  command=self.abort_message_callback, width="20")

        # Variables Used Across Functions in Class
        self.temperature = 26.6555555
        self.pressure = 101.325
        self.humidity = 67.2
        self.altitude = 150000
        self.direction = 36
        self.acceleration = 3.06
        self.velocity = 5.01

        self.angle_result = 55.07

        self.verify_ok_to_launch = False
        self.has_aborted = False

        self.tempDataLabel = Label(self.subFrameLeft, text=self.temperature, fg="white", bg=bgColor, width=standardDataWidth)
        self.altDataLabel = Label(self.subFrameRight, text=self.altitude, fg="white", bg=bgColor, width=standardDataWidth)
        self.pressureDataLabel = Label(self.subFrameLeft, text=self.pressure, fg="white", bg=bgColor, width=standardDataWidth)
        self.cardinalDataLabel = Label(self.subFrameRight, text=self.direction, fg="white", bg=bgColor, width=standardDataWidth)
        self.humidityDataLabel = Label(self.subFrameLeft, text=self.humidity, fg="white", bg=bgColor, width=standardDataWidth)
        self.accDataLabel = Label(self.subFrameRight, text=self.acceleration, fg="white", bg=bgColor, width=standardDataWidth)
        self.velocityDataLabel = Label(self.subFrameRight, text=self.velocity, fg="white", bg=bgColor, width=standardDataWidth)
        self.angleDataLabel = Label(self.subFrameRight, text=self.angle_result, fg="white", bg=bgColor, width=standardDataWidth)

        self.infoText = Label(self.subFrameBottom, fg="white", bg=bgColor, width=40)
        self.angleEntry = Entry(self.subFrameLeft, bd=5, bg=bgColor, fg="white", width=standardDataWidth,
                                textvariable=self.angle_result)

        # Set up GPIO pins for use, see documentation for pin layout
        # orange wire
        self.launch_signal = 11
        # yellow wire
        self.on_signal = 12
        # white wire
        self.gui_switch = 7

        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setwarnings(False)
        # GPIO.setup(self.launch_signal, GPIO.IN)
        # GPIO.setup(self.on_signal, GPIO.OUT)
        # GPIO.setup(self.gui_switch, GPIO.OUT)

        # GPIO.output(self.on_signal, GPIO.HIGH)
        # GPIO.output(self.on_signal, GPIO.LOW)
        # GPIO.output(self.gui_switch, GPIO.LOW)

        # Setup Window
        name.configure(background=DarkGray)
        name.title("Ground Station Graphical User Interface V0.1")
        # name.iconbitmap('MyOrbital.ico')

        window_geometry = str(self.width) + 'x' + str(self.height)
        self.name.geometry(window_geometry)
        self.make_menu()

        self.draw_frames()

    def get_angle(self):
        input_angle_result = self.angleEntry.get()
        if len(self.angleEntry.get()) > 0 and 30.0 <= float(input_angle_result) <= 75.0:
            self.angle_result = round(float(input_angle_result), 4)
            if 30.0 <= self.angle_result <= 75.0:
                self.angleDataLabel.config(text=self.angle_result)

    def on_enter_abort(self, event):
        self.infoText.config(text="Abort Mission Button", fg="red")

    def on_enter_verify(self, event):
        self.infoText.config(text="Verify Mission Button", fg="green")

    def on_leave(self, event):
        self.infoText.config(text=" ")

    def log(self, status):
        fo = open("status.log", "a")
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
        fo.write("temperature = " + repr(self.temperature) + "\n")
        fo.write("pressure = " + repr(self.pressure) + "\n")
        fo.write("humidity = " + repr(self.humidity) + "\n")
        fo.write("altitude = " + repr(self.altitude) + "\n")
        fo.write("direction = " + repr(self.direction) + "\n")
        fo.write("acceleration = " + repr(self.acceleration) + "\n")
        fo.write("velocity = " + repr(self.velocity) + "\n")
        fo.write("horizontalAngle = " + repr(self.angle_result) + "\n")
        fo.write("----------LOGS END-----------\n")
        fo.write("-----------------------------\n\n")
        fo.close()

    def close_window(self, window):
        window.destroy()

    def log_menu(self):
        log_window = Toplevel(self.name)
        log_window.title("Log")
        loggedLabel = Label(log_window, text="The current variables have been logged in 'status.log'")
        loggedLabel.pack()
        button = Button(log_window, text="Close", command=lambda: self.close_window(log_window))
        button.pack()
        self.log("MANUAL")

    def update_size(self):
        # Resets the variables width and height to the actual size of the window
        # self.width = self.name.winfo_width()
        # self.height = self.name.winfo_height()

        # Destroys the current frames and redraws them with the correct width and height dimensions
        self.destroy_frames()
        self.draw_frames()

    def update_variables(self):
        # Updates the variables values
        self.tempDataLabel.config(text=self.temperature)
        self.pressureDataLabel.config(text=self.pressure)
        self.humidityDataLabel.config(text=self.humidity)
        self.altDataLabel.config(text=self.altitude)
        self.cardinalDataLabel.config(text=self.direction)
        self.accDataLabel.config(text=self.acceleration)
        self.velocityDataLabel.config(text=self.velocity)
        self.angleDataLabel.config(text=self.angle_result)

    def draw_frames(self):
        # Draws the frames and immediately draws the items in the frames
        self.subFrameLeft = Frame(self.name, bg=LightGray, height=self.height / 2, width=self.width / 2 - 5,
                                  relief=RAISED)
        self.subFrameRight = Frame(self.name, bg=LightGray, height=self.height / 2, width=self.width / 2 - 5,
                                   relief=RAISED)
        self.subFrameBottom = Frame(self.name, bg="#3C3F41", height=self.height / 3, width=self.width, relief=RAISED)

        self.statusLabel = Label(self.subFrameBottom, text=self.status_label_text, fg=self.status_label_text_color,
                                 bg="#808080", width= int(20/600 * self.width), height=int(2/600 * self.width))

        self.subFrameLeft.place(x=0, y=5)
        self.subFrameRight.place(x=self.width / 2 + 5, y=5)
        self.subFrameBottom.place(x=0, y=self.height * 315 / 600)

        self.add_frame_features()

    def destroy_frames(self):
        # Deletes the frames and their contents
        self.subFrameLeft.destroy()
        self.subFrameRight.destroy()
        self.subFrameBottom.destroy()

    def reset_variables(self):
        # Resets all of the data on screen to zero

        # GPIO.output(self.gui_switch, GPIO.LOW)
        self.temperature = 0.0
        self.pressure = 0.0
        self.humidity = 0.0
        self.altitude = 0.0
        self.direction = 0.0
        self.acceleration = 0.0
        self.velocity = 0.0
        self.angle_result = "null"

        self.update_variables()

    def status_label_change(self, change_to):
        # Updates the Mission Current Status label text color and text
        self.status_label_text = change_to
        self.statusLabel.config(text=self.status_label_text)
        if change_to == "VERIFIED":
            self.status_label_text_color = "green"
            self.statusLabel.config(fg=self.status_label_text_color)
        elif change_to == "NOT VERIFIED":
            self.status_label_text_color = "orange"
            self.statusLabel.config(fg=self.status_label_text_color)
        elif change_to == "MISSION ABORTED":
            self.status_label_text_color = "red"
            self.statusLabel.config(fg=self.status_label_text_color)

    def verify_message_callback(self):
        # Creates a pop up window that asks if you are sure that you want to verify the launch. If yes then verify
        verify_response = messagebox.askyesno("Verify Launch", "Do you want to verify for launch?")
        if verify_response:
            self.verify_ok_to_launch = True
            self.abort_button_state = NORMAL
            self.abortButton.config(state=self.abort_button_state)
            self.status_label_change("VERIFIED")
            self.log("VERIFIED")
            # GPIO.output(self.gui_switch, GPIO.HIGH)
        else:
            self.verify_ok_to_launch = False
            self.status_label_change("NOT VERIFIED")
            self.abortButton.config(state=DISABLED)
            self.log("NOT")

    def abort_message_callback(self):
        # Creates a pop up window that asks if you are sure that you want to abort the launch. If yes then abort
        abort_response = messagebox.askyesno("Abort Mission?", "Do you really want to abort the mission?")
        if abort_response:
            self.has_aborted = True
            self.verify_ok_to_launch = False
            self.status_label_change("MISSION ABORTED")
            self.abort_button_state = DISABLED
            self.abortButton.config(state=self.abort_button_state)
            self.log("ABORT")
            # GPIO.output(self.gui_switch, GPIO.LOW)
        else:
            self.has_aborted = False

    def add_frame_features(self):
        # Draws all of the features inside the frames including labels, buttons, etc.
        width = self.width
        height = self.height
        bgColor = "#333333"
        subFrameColor = "#3C3F41"
        standardTextWidth = int(3/100 * width)
        standardDataWidth = int(1/100 * width)

        x_place = 4/15 * width
        x_label_place = 1/60 * width

        subFrameLeft = self.subFrameLeft
        subFrameRight = self.subFrameRight
        subFrameBottom = self.subFrameBottom

        self.tempDataLabel = Label(self.subFrameLeft, text=round(self.temperature, 4), fg="white", bg=bgColor,
                                   width=standardDataWidth)
        self.altDataLabel = Label(self.subFrameRight, text=round(self.altitude, 4), fg="white", bg=bgColor,
                                  width=standardDataWidth)
        self.pressureDataLabel = Label(self.subFrameLeft, text=round(self.pressure, 4), fg="white", bg=bgColor,
                                       width=standardDataWidth)
        self.cardinalDataLabel = Label(self.subFrameRight, text=round(self.direction, 4), fg="white", bg=bgColor,
                                       width=standardDataWidth)
        self.humidityDataLabel = Label(self.subFrameLeft, text=round(self.humidity, 4), fg="white", bg=bgColor,
                                       width=standardDataWidth)
        self.accDataLabel = Label(self.subFrameRight, text=round(self.acceleration, 4), fg="white", bg=bgColor,
                                  width=standardDataWidth)
        self.velocityDataLabel = Label(self.subFrameRight, text=round(self.velocity, 4), fg="white", bg=bgColor,
                                       width=standardDataWidth)
        self.angleDataLabel = Label(self.subFrameRight, text=round(self.angle_result, 4), fg="white", bg=bgColor,
                                    width=standardDataWidth)

        abortLabel = Label(subFrameBottom, text="Abort Mission:", bg=bgColor, fg="white", width=int(1/50*width))
        abortLabel.place(x=x_label_place, y=int(55 / 600 * height))

        verifyLabel = Label(subFrameBottom, text="Verify Launch:", bg=bgColor, fg="white", width=int(1/50*width))
        verifyLabel.place(x=x_label_place, y=int(125 / 600 * height))

        self.statusLabel.place(x=width * 5 / 8, y=int(2 / 15 * height))

        statusTextLabel = Label(subFrameBottom, text="Current Status:", fg="white", bg=bgColor,
                                width=int(12/600 * width), height=1)
        statusTextLabel.place(x=int(405/600 * width), y=int(1 / 12 * height))

        frameLeftLabel = Label(subFrameLeft, text="Environmental Data:", fg="white", bg=subFrameColor)
        frameLeftLabel.place(x=int(90 / 600 * width), y=5 / 600 * height)

        frameRightLabel = Label(subFrameRight, text="System Data:", fg="white", bg=subFrameColor)
        frameRightLabel.place(x=int(90 / 600 * (width), y=5 / 600 * height)

        tempLabel = Label(subFrameLeft, text="Temperature (Celsius): ", fg="white", bg=bgColor, width=standardTextWidth)
        tempLabel.place(x=x_label_place, y=int(1/15 * height))

        self.tempDataLabel.place(x=x_place, y=int(1/15 * height))

        altLabel = Label(subFrameRight, text="Altitude (Meters): ", fg="white", bg=bgColor, width=standardTextWidth)
        altLabel.place(x=x_label_place, y=int(1/15 * height))

        self.altDataLabel.place(x=x_place, y=int(1/15 * height))

        pressureLabel = Label(subFrameLeft, text="Pressure (kPa): ", fg="white", bg=bgColor, width=standardTextWidth)
        pressureLabel.place(x=x_label_place, y=int(2/15 * height))

        self.pressureDataLabel.place(x=x_place, y=int(2/15 * height))

        cardinalLabel = Label(subFrameRight, text="Direction (°): ", fg="white", bg=bgColor, width=standardTextWidth)
        cardinalLabel.place(x=x_label_place, y=int(2/15 * height))

        self.cardinalDataLabel.place(x=x_place, y=int(2/15 * height))

        humidLabel = Label(subFrameLeft, text="Humidity (Percent): ", fg="white", bg=bgColor, width=standardTextWidth)
        humidLabel.place(x=x_label_place, y=int(1/5 * height))

        self.humidityDataLabel.place(x=x_place, y=int(1/5 * height))

        accLabel = Label(subFrameRight, text="Acceleration (M/s/s): ", fg="white", bg=bgColor, width=standardTextWidth)
        accLabel.place(x=x_label_place, y=int(1/5 * height))

        self.accDataLabel.place(x=x_place, y=int(1/5 * height))

        velocityLabel = Label(subFrameRight, text="Velocity (M/s): ", fg="white", bg=bgColor, width=standardTextWidth)
        velocityLabel.place(x=x_label_place, y=int(4/15 * height))

        self.velocityDataLabel.place(x=x_place, y=int(4/15 * height))

        angleLabel = Label(subFrameRight, text="Angle (°): ", fg="white", bg=bgColor, width=standardTextWidth)
        angleLabel.place(x=x_label_place, y=int(1/3 * height))

        self.angleDataLabel.place(x=x_place, y=int(1/3 * height))

        angleEntryLabel = Label(subFrameLeft, text="Positive angle between 30° and 75°", fg="white", bg=subFrameColor,
                                width=int(26/600 * width))
        angleEntryLabel.place(x=int(40/600 * width), y=int(230/600 * height))

        self.abortButton = Button(self.subFrameBottom, text="ABORT MISSION", state=self.abort_button_state, bg="red",
                                  command=self.abort_message_callback, width=int(20 / 600 * self.width),
                                  height=int(1.5 / 600 * self.height))

        self.abortButton.place(x=int(1/6 * width), y=int(55/600 * height))
        self.abortButton.bind("<Enter>", self.on_enter_abort)
        self.abortButton.bind("<Leave>", self.on_leave)

        verifyButton = Button(subFrameBottom, text="VERIFY LAUNCH", background="green", command=self.verify_message_callback,
                              width=int(20/600 * width), height=int(1.5/600 * height))

        verifyButton.place(x=int(1/6 * width), y=int(125/600 * height))
        verifyButton.bind("<Enter>", self.on_enter_verify)
        verifyButton.bind("<Leave>", self.on_leave)

        self.infoText = Label(self.subFrameBottom, fg="white", bg=bgColor, width=int(40/600 * width))
        self.infoText.place(x=x_place, y=int(15/600 * height))

        self.angleEntry = Entry(subFrameLeft, bd=5, bg=bgColor, fg="white", width=int(1/50 * width),
                           textvariable=self.angle_result)
        self.angleEntry.place(x=int(40/600 * width), y=int(260/600 * height))

        angleInputButton = ttk.Button(subFrameLeft, text="ENTER", width=int(15/600 * width), command=self.get_angle)
        angleInputButton.place(x=x_place, y=int(260/600 * height))

    def reset_variables_window(self):
        # Creates a pop up window that asks if you are sure that you want to rest the variables.
        # If yes then all the variables are reset
        reset_window = messagebox.askokcancel("Reset All Variables?", "Are you sure you want to reset all variables?")
        if reset_window:
            self.log("RESET")
            self.reset_variables()
            self.verify_ok_to_launch = False
            self.status_label_change("NOT VERIFIED")
            self.abortButton.config(state=DISABLED)

    def do_nothing(self):
        file_window = Toplevel(self.name)
        button = Button(file_window, text="Close", command=lambda: self.close_window(file_window))
        button.pack()

    def about(self):

        aboutText = "Ground Station Graphical User Interface Version 0.1\n\n" \
                    "Author: Ken Sodetz\n" \
                    "Since: 10/11/2017\n\n" \
                    "Created for Purdue Orbital Electrical and Software Sub team\n\n" \
                    "Parses and displays data from the a Raspberry Pi 3 to verbosely display all\npertinent system data " \
                    "(data that can be changed) and environmental data\n(data that cannot be changed)"

        about_window = Toplevel(self.name)
        about_window.title("About")
        about_window.resizable(width=False, height=False)
        text = Text(about_window)
        text.insert(INSERT, aboutText)
        text.config(state=DISABLED)
        text.pack()
        self.name.img = img = PhotoImage(file="PurdueOrbitalLogoSmall.gif")
        logo = Label(about_window, image=img)
        logo.place(x=220, y=200)
        button = Button(about_window, text="Close", command=lambda: self.close_window(about_window))
        button.pack()

    def restart_program(self):
        python = sys.executable
        # GPIO.output(self.gui_switch, GPIO.LOW)
        # GPIO.cleanup()
        self.log("RESTART")
        os.execl(python, python, *sys.argv)

    def make_menu(self):
        menuBar = Menu(self.name)

        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Restart", command=self.restart_program)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.name.quit)
        menuBar.add_cascade(label="File", menu=fileMenu)

        programMenu = Menu(menuBar, tearoff=0)
        programMenu.add_command(label="Reset", command=self.reset_variables_window)
        programMenu.add_command(label="Resize", command=self.update_size)
        programMenu.add_command(label="Log", command=self.log_menu)
        menuBar.add_cascade(label="Program", menu=programMenu)

        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="Help Index", command=self.do_nothing)
        helpMenu.add_separator()
        helpMenu.add_command(label="About", command=self.about)
        menuBar.add_cascade(label="Help", menu=helpMenu)

        self.name.config(menu=menuBar)


root = Tk()
window = DataWindow(root)


def config_resize(event):
    if window.width != window.name.winfo_width() or window.height != window.name.winfo_height():
        window.width = window.name.winfo_width()
        window.height = window.name.winfo_height()
        print("Var Width = " + str(window.width) + "   Act Width = " + str(window.name.winfo_width())
              + "        Var Height = " + str(window.height) + "   Real Height = " + str(window.name.winfo_height()))
        time.sleep(.0005)
        window.update_size()
        time.sleep(.0005)

root.bind('<Configure>', config_resize)
# Backup ideas!!!
# root.bind('<B1-Motion>', mouse_resize)
# root.bind('r', key_resize)


root.mainloop()
# GPIO.cleanup()
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
    loggedLabel = Label(log_window, text="The current variables have been logged in 'status.log'")
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
    top.img = img = PhotoImage(file="../rec/PurdueOrbitalLogoSmall.gif")
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
    fo = open("status.log", "a")
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
