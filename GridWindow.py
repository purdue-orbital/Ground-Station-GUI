from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime
import time
import os
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


class MyWindow:
    def __init__(self, name):
        self.name = name
        self.width = 600
        self.height = 600
        self.bg = "#333333"
        self.FrameColor = "#3C3F41"

        name.title("Ground Station Graphical User Interface V0.2")
        name.iconbitmap('MyOrbital.ico')
        # name.configure(background=self.bg)

        window_geometry = str(self.width) + 'x' + str(self.height)
        self.name.geometry(window_geometry)

        # Environment Data
        self.temperature = 55
        self.pressure = 123
        self.humidity = 42

        # System Data
        self.altitude = 15000000000
        self.direction = 36
        self.acceleration = 3.06
        self.velocity = 5.01
        self.user_angle = 55.07

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

    def update_variables(self):

        temperature_data = Label(self.name, text=self.temperature)
        pressure_data = Label(self.name, text=self.pressure)
        humidity_data = Label(self.name, text=self.humidity)

        altitude_data = Label(self.name, text=self.altitude)
        direction_data = Label(self.name, text=self.direction)
        acceleration_data = Label(self.name, text=self.acceleration)
        velocity_data = Label(self.name, text=self.velocity)
        angle_data = Label(self.name, text=self.user_angle)

        temperature_data.grid(row=1, column=3)
        pressure_data.grid(row=2, column=3)
        humidity_data.grid(row=3, column=3)

        altitude_data.grid(row=1, column=7)
        direction_data.grid(row=2, column=7)
        acceleration_data.grid(row=3, column=7)
        velocity_data.grid(row=4, column=7)
        angle_data.grid(row=5, column=7)

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
        temperature_data = Label(self.name, text=self.temperature)
        pressure_data = Label(self.name, text=self.pressure)
        humidity_data = Label(self.name, text=self.humidity)

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
        altitude_data = Label(self.name, text=self.altitude)
        direction_data = Label(self.name, text=self.direction)
        acceleration_data = Label(self.name, text=self.acceleration)
        velocity_data = Label(self.name, text=self.velocity)
        angle_data = Label(self.name, text=self.user_angle)

        altitude_data.grid(row=1, column=7)
        direction_data.grid(row=2, column=7)
        acceleration_data.grid(row=3, column=7)
        velocity_data.grid(row=4, column=7)
        angle_data.grid(row=5, column=7)

    def log(self, status):
        fo = open("status_log.txt", "a")
        current_date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
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
        # fo.write("horizontalAngle = " + repr(self.angle_result) + "\n")
        fo.write("----------LOGS END-----------\n")
        fo.write("-----------------------------\n\n")
        fo.close()

    def restart_program(self):
        python = sys.executable
        # GPIO.output(self.gui_switch, GPIO.LOW)
        # GPIO.cleanup()
        self.log("RESTART")
        os.execl(python, python, *sys.argv)

    def reset_variables_window(self):
        # Creates a pop up window that asks if you are sure that you want to rest the variables.
        # If yes then all the variables are reset
        reset_window = messagebox.askokcancel("Reset All Variables?", "Are you sure you want to reset all variables?")
        if reset_window:
            self.log("RESET")
            self.reset_variables()
            # self.verify_ok_to_launch = False
            # self.status_label_change("NOT VERIFIED")
            # self.abortButton.config(state=DISABLED)

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
        self.user_angle = "null"

        self.update_variables()


root = Tk()
window = MyWindow(root)

root.mainloop()
