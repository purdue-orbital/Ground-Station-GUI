from tkinter import *
from tkinter import messagebox
import datetime
import time
import os
from enum import Enum
# import serial
# import RPi.GPIO as GPIO

"""
ROCKET GUI Version 0.2

Author: Matt Drozt
Since: 10/31/2018

Created for Purdue Orbital Electrical and Software Sub team

Parses and displays data from the a Raspberry Pi 3 to verbosely
display all pertinent system data (data that can be changed) and environmental
data (data that cannot be changed).

"""


class status(Enum):
    ABORT = "MISSION ABORTED"
    VERIFIED = "STATUS VERIFIED"
    NOTVERIFIED = "STATUS NOT VERIFIED"
    MANUAL = "MANUAL LOG INVOKED"
    RESET = "VARIABLES RESET"
    RESTART = "PROGRAM RESTART"


class MyWindow:
    def __init__(self, name):
        self.name = name
        self.width = 600
        self.height = 600
        self.bg = "#333333"
        self.FrameColor = "#3C3F41"

        name.title("Ground Station Graphical User Interface V0.2")
        #name.iconbitmap('MyOrbital.ico')
        # name.configure(background=self.bg)

        window_geometry = str(self.width) + 'x' + str(self.height)
        self.name.geometry(window_geometry)

        # Environment Data
        self.temperature = StringVar()
        self.temperature.set(15000.0)
        self.pressure = StringVar()
        self.pressure.set(6000.0)
        self.humidity = StringVar()
        self.humidity.set(10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000.0)

        # System Data
        self.altitude = StringVar()
        self.altitude.set(15000000)
        self.direction = StringVar()
        self.direction.set(.1234)
        self.acceleration = StringVar()
        self.acceleration.set(90)
        self.velocity = StringVar()
        self.velocity.set(12)
        self.user_angle = StringVar()
        self.user_angle.set(458)

        self.make_tool_bar()

        self.make_grid()
        self.make_environmental_section()
        self.make_system_section()

    def make_tool_bar(self):
        menu_bar = Menu(self.name)

        file_menu = Menu(menu_bar, tearoff=0)
        program_menu = Menu(menu_bar, tearoff=0)
        help_menu = Menu(menu_bar, tearoff=0)

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Program", menu=program_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        file_menu.add_command(label="Restart", command=self.restart_program)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.name.quit)

        program_menu.add_command(label="Reset", command=self.reset_variables_window)
        # program_menu.add_command(label="Log", command=self.log_menu)

        # help_menu.add_command(label="Help Index", command=self.do_nothing)
        # help_menu.add_separator()
        # help_menu.add_command(label="About", command=self.about)

        self.name.config(menu=menu_bar)

    def make_grid(self):
        total_rows = 10
        total_columns = 8

        my_rows = range(0, total_rows)
        my_columns = range(0, total_columns)

        for column in my_columns:
            self.name.columnconfigure(column, weight=1)

        for row in my_rows:
            self.name.rowconfigure(row, weight=1, uniform=1)

    def make_environmental_section(self):
        # Create and Place Section Header
        environmental_data_label = Label(self.name, text="Environmental Data")
        environmental_data_label.grid(row=0, column=2)

        # Create and Place Labels for Data
        temperature_label = Label(self.name, text="Temperature (Celsius):")
        pressure_label = Label(self.name, text="Pressure (kPa):")
        humidity_label = Label(self.name, text="Humidity (Percent):")

        temperature_label.grid(row=1, column=1)
        pressure_label.grid(row=2, column=1)
        humidity_label.grid(row=3, column=1)

        # Place Data Across from Corresponding Label
        temperature_data = Label(self.name, textvariable=self.temperature)
        pressure_data = Label(self.name, textvariable=self.pressure)
        humidity_data = Label(self.name, textvariable=self.humidity)

        temperature_data.grid(row=1, column=3)
        pressure_data.grid(row=2, column=3)
        humidity_data.grid(row=3, column=3)

    def make_system_section(self):
        # Create and Place Section Header
        system_data_label = Label(self.name, text="System Data")
        system_data_label.grid(row=0, column=6)

        # Create and Place Labels for Data
        altitude_label = Label(self.name, text="Altitude (km):")
        direction_label = Label(self.name, text="Direction(rad):")
        acceleration_label = Label(self.name, text="Acceleration (m/s/s):")
        velocity_label = Label(self.name, text="Velocity (m/s):")
        angle_label = Label(self.name, text="Angle (rad):")

        altitude_label.grid(row=1, column=5)
        direction_label.grid(row=2, column=5)
        acceleration_label.grid(row=3, column=5)
        velocity_label.grid(row=4, column=5)
        angle_label.grid(row=5, column=5)

        # Place Data Across from Corresponding Label
        altitude_data = Label(self.name, textvariable=self.altitude)
        direction_data = Label(self.name, textvariable=self.direction)
        acceleration_data = Label(self.name, textvariable=self.acceleration)
        velocity_data = Label(self.name, textvariable=self.velocity)
        angle_data = Label(self.name, textvariable=self.user_angle)

        altitude_data.grid(row=1, column=7)
        direction_data.grid(row=2, column=7)
        acceleration_data.grid(row=3, column=7)
        velocity_data.grid(row=4, column=7)
        angle_data.grid(row=5, column=7)

    def log(self, status):
        fo = open("status_log.txt", "a")
        current_date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        if status == status.ABORT:
            fo.write("-------MISSION ABORTED-------\n")
        elif status == status.VERIFIED:
            fo.write("-------STATUS VERIFIED-------\n")
        elif status == status.MANUAL:
            fo.write("-----MANUAL LOG INVOKED------\n")
        elif status == status.RESET:
            fo.write("-------VARIABLES RESET-------\n")
        elif status == status.RESTART:
            fo.write("-------PROGRAM RESTART-------\n")
        elif status == status.NOTVERIFIED:
            fo.write("-----STATUS NOT VERIFIED-----\n")

        fo.write("TIMESTAMP:" + current_date + "\n")
        fo.write("*****************************\n")
        fo.write("----------LOGS START---------\n")
        fo.write("temperature = " + repr(self.temperature) + "\n")
        fo.write("pressure = " + repr(self.pressure) + "\n")
        fo.write("humidity = " + repr(self.humidity) + "\n")
        fo.write("altitude = " + repr(self.altitude) + "\n")
        fo.write("direction = " + repr(self.direction) + "\n")
        fo.write("acceleration = " + repr(self.acceleration) + "\n")
        fo.write("velocity = " + repr(self.velocity) + "\n")
        fo.write("----------LOGS END-----------\n")
        fo.write("-----------------------------\n\n")
        fo.close()

    def restart_program(self):
        python = sys.executable
        # GPIO.output(self.gui_switch, GPIO.LOW)
        # GPIO.cleanup()
        self.log(status.RESTART)
        os.execl(python, python, *sys.argv)

    def reset_variables_window(self):
        # Creates a pop up window that asks if you are sure that you want to rest the variables.
        # If yes then all the variables are reset
        reset_window = messagebox.askokcancel("Reset All Variables?", "Are you sure you want to reset all variables?")
        if reset_window:
            self.log(status.RESET)
            self.reset_variables()
            # self.verify_ok_to_launch = False
            # self.status_label_change("NOT VERIFIED")
            # self.abortButton.config(state=DISABLED)

    def reset_variables(self):
        # Resets all of the data on screen to zero

        # GPIO.output(self.gui_switch, GPIO.LOW)
        self.temperature.set(0.0)
        self.pressure.set(0.0)
        self.humidity.set(0.0)

        self.altitude.set(0.0)
        self.direction.set(0.0)
        self.acceleration.set(0.0)
        self.velocity.set(0.0)
        self.user_angle.set("null")

root = Tk()
window = MyWindow(root)

root.mainloop()
