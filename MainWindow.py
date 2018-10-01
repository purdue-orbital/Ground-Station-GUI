from tkinter import *
from tkinter import messagebox
import datetime
import time
import os
# import serial
# import RPi.GPIO as GPIO

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


class MyWindow:
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
        self.temperature = 26.6
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

        window_geometry = str(self.width) + 'x' + str(self.height)
        self.name.geometry(window_geometry)
        self.make_menu()

        self.draw_frames()

    def get_angle(self):
        input_angle_result = self.angleEntry.get()
        if len(self.angleEntry.get()) > 0 and 30.0 <= float(input_angle_result) <= 75.0:
            self.angle_result = float(input_angle_result)
            if 30.0 <= self.angle_result <= 75.0:
                self.angleDataLabel.config(text=self.angle_result)

    def on_enter_abort(self, event):
        self.infoText.config(text="Abort Mission Button", fg="red")

    def on_enter_verify(self, event):
        self.infoText.config(text="Verify Mission Button", fg="green")

    def on_leave(self, event):
        self.infoText.config(text=" ")

    def log(self, status):
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
        loggedLabel = Label(log_window, text="The current variables have been logged in 'status_log.txt'")
        loggedLabel.pack()
        button = Button(log_window, text="Close", command=lambda: self.close_window(log_window))
        button.pack()
        self.log("MANUAL")

    def update_size(self):
        self.width = self.name.winfo_width()
        self.height = self.name.winfo_height()

        self.destroy_frames()
        self.draw_frames()

    def update_variables(self):
        self.tempDataLabel.config(text=self.temperature)
        self.pressureDataLabel.config(text=self.pressure)
        self.humidityDataLabel.config(text=self.humidity)
        self.altDataLabel.config(text=self.altitude)
        self.cardinalDataLabel.config(text=self.direction)
        self.accDataLabel.config(text=self.acceleration)
        self.velocityDataLabel.config(text=self.velocity)
        self.angleDataLabel.config(text=self.angle_result)

    def draw_frames(self):
        self.subFrameLeft = Frame(self.name, bg=LightGray, height=self.height / 2, width=self.width / 2 - 5,
                                  relief=RAISED)
        self.subFrameRight = Frame(self.name, bg=LightGray, height=self.height / 2, width=self.width / 2 - 5,
                                   relief=RAISED)
        self.subFrameBottom = Frame(self.name, bg="#3C3F41", height=self.height / 3, width=self.width, relief=RAISED)

        self.abortButton = Button(self.subFrameBottom, text="ABORT MISSION", state=self.abort_button_state, bg="red",
                                  command=self.abort_message_callback, width=int(20/600 * self.width),
                                  height=int(1.5/600 * self.height))

        self.statusLabel = Label(self.subFrameBottom, text=self.status_label_text, fg=self.status_label_text_color,
                                 bg="#808080", width= int(20/600 * self.width), height=int(2/600 * self.width))

        self.subFrameLeft.place(x=0, y=5)
        self.subFrameRight.place(x=self.width / 2 + 5, y=5)
        self.subFrameBottom.place(x=0, y=self.height * 315 / 600)

        self.add_frame_features()

    def destroy_frames(self):
        self.subFrameLeft.destroy()
        self.subFrameRight.destroy()
        self.subFrameBottom.destroy()

    def reset_variables(self):
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
        # print(change_to)
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
        width = self.width
        height = self.height
        bgColor = "#333333"
        subFrameColor = "#3C3F41"
        standardTextWidth = int(18/600 * width)
        standardDataWidth = int(6/600 * width)

        x_place = 4/15 * width
        x_label_place = 1/60 * width

        subFrameLeft = self.subFrameLeft
        subFrameRight = self.subFrameRight
        subFrameBottom = self.subFrameBottom

        self.tempDataLabel = Label(self.subFrameLeft, text=self.temperature, fg="white", bg=bgColor,
                                   width=standardDataWidth)
        self.altDataLabel = Label(self.subFrameRight, text=self.altitude, fg="white", bg=bgColor,
                                  width=standardDataWidth)
        self.pressureDataLabel = Label(self.subFrameLeft, text=self.pressure, fg="white", bg=bgColor,
                                       width=standardDataWidth)
        self.cardinalDataLabel = Label(self.subFrameRight, text=self.direction, fg="white", bg=bgColor,
                                       width=standardDataWidth)
        self.humidityDataLabel = Label(self.subFrameLeft, text=self.humidity, fg="white", bg=bgColor,
                                       width=standardDataWidth)
        self.accDataLabel = Label(self.subFrameRight, text=self.acceleration, fg="white", bg=bgColor,
                                  width=standardDataWidth)
        self.velocityDataLabel = Label(self.subFrameRight, text=self.velocity, fg="white", bg=bgColor,
                                       width=standardDataWidth)
        self.angleDataLabel = Label(self.subFrameRight, text=self.angle_result, fg="white", bg=bgColor,
                                    width=standardDataWidth)

        abortLabel = Label(subFrameBottom, text="Abort Mission:", bg=bgColor, fg="white", width=int(12/600*width))
        abortLabel.place(x=x_label_place, y=int(55 / 600 * height))

        verifyLabel = Label(subFrameBottom, text="Verify Launch:", bg=bgColor, fg="white", width=int(12/600*width))
        verifyLabel.place(x=x_label_place, y=int(125 / 600 * height))

        self.statusLabel.place(x=width * 5 / 8, y=int(2 / 15 * height))

        statusTextLabel = Label(subFrameBottom, text="Current Status:", fg="white", bg=bgColor,
                                width=int(12/600 * width), height=1)
        statusTextLabel.place(x=int(405/600 * width), y=int(1 / 12 * height))

        frameLeftLabel = Label(subFrameLeft, text="Environmental Data:", fg="white", bg=subFrameColor)
        frameLeftLabel.place(x=int(90 / 600 * width), y=5 / 600 * height)

        frameRightLabel = Label(subFrameRight, text="System Data:", fg="white", bg=subFrameColor)
        frameRightLabel.place(x=int(90 / 600 * width), y=5 / 600 * height)

        tempLabel = Label(subFrameLeft, text="Temperature (Celsius): ", fg="white", bg=bgColor, width=standardTextWidth)
        tempLabel.place(x=x_label_place, y=int(40/600 * height))

        self.tempDataLabel.place(x=x_place, y=int(40/600 * height))

        altLabel = Label(subFrameRight, text="Altitude (Meters): ", fg="white", bg=bgColor, width=standardTextWidth)
        altLabel.place(x=x_label_place, y=int(40/600 * height))

        self.altDataLabel.place(x=x_place, y=int(40/600 * height))

        pressureLabel = Label(subFrameLeft, text="Pressure (kPa): ", fg="white", bg=bgColor, width=standardTextWidth)
        pressureLabel.place(x=x_label_place, y=int(80/600 * height))

        self.pressureDataLabel.place(x=x_place, y=int(80/600 * height))

        cardinalLabel = Label(subFrameRight, text="Direction (°): ", fg="white", bg=bgColor, width=standardTextWidth)
        cardinalLabel.place(x=x_label_place, y=int(80/600 * height))

        self.cardinalDataLabel.place(x=x_place, y=int(80/600 * height))

        humidLabel = Label(subFrameLeft, text="Humidity (Percent): ", fg="white", bg=bgColor, width=standardTextWidth)
        humidLabel.place(x=x_label_place, y=int(120/600 * height))

        self.humidityDataLabel.place(x=x_place, y=int(120/600 * height))

        accLabel = Label(subFrameRight, text="Acceleration (M/s/s): ", fg="white", bg=bgColor, width=standardTextWidth)
        accLabel.place(x=x_label_place, y=int(120/600 * height))

        self.accDataLabel.place(x=x_place, y=int(120/600 * height))

        velocityLabel = Label(subFrameRight, text="Velocity (M/s): ", fg="white", bg=bgColor, width=standardTextWidth)
        velocityLabel.place(x=x_label_place, y=int(160/600 * height))

        self.velocityDataLabel.place(x=x_place, y=int(160/600 * height))

        angleLabel = Label(subFrameRight, text="Angle (°): ", fg="white", bg=bgColor, width=standardTextWidth)
        angleLabel.place(x=x_label_place, y=int(200/600 * height))

        self.angleDataLabel.place(x=x_place, y=int(200/600 * height))

        angleEntryLabel = Label(subFrameLeft, text="Positive angle between 30° and 75°", fg="white", bg=subFrameColor,
                                width=int(26/600 * width))
        angleEntryLabel.place(x=int(40/600 * width), y=int(230/600 * height))

        self.abortButton.place(x=int(1/6 * width), y=int(55/600 * height))
        self.abortButton.bind("<Enter>", self.on_enter_abort)
        self.abortButton.bind("<Leave>", self.on_leave)

        verifyButton = Button(subFrameBottom, text="VERIFY LAUNCH", bg="green", command=self.verify_message_callback,
                              width=int(20/600 * width), height=int(1.5/600 * height))

        verifyButton.place(x=int(1/6 * width), y=int(125/600 * height))
        verifyButton.bind("<Enter>", self.on_enter_verify)
        verifyButton.bind("<Leave>", self.on_leave)

        self.infoText = Label(self.subFrameBottom, fg="white", bg=bgColor, width=int(40/600 * width))
        self.infoText.place(x=x_place, y=int(15/600 * height))

        self.angleEntry = Entry(subFrameLeft, bd=5, bg=bgColor, fg="white", width=int(1/50 * width),
                           textvariable=self.angle_result)
        self.angleEntry.place(x=int(40/600 * width), y=int(260/600 * height))

        angleInputButton = Button(subFrameLeft, text="ENTER", width=int(15/600 * width), command=self.get_angle)
        angleInputButton.place(x=x_place, y=int(260/600 * height))

    def reset_variables_window(self):
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
p = MyWindow(root)
root.mainloop()
# GPIO.cleanup()
