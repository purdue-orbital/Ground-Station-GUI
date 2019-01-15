import datetime
import time
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from enum import Enum
# import serial
import RPi.GPIO as GPIO

from Timer import *


"""
ROCKET GUI Version 0.2

Author: Matt Drozt, Ken Sodetz, Jay Rixie
Since: 10/31/2018

Created for Purdue Orbital Electrical and Software Sub team

Parses and displays data from the a Raspberry Pi 3 to verbosely
display all pertinent system data (data that can be changed) and environmental
data (data that cannot be changed).

"""


class Status(Enum):
    ABORT = "MISSION ABORTED"
    VERIFIED = "STATUS VERIFIED"
    NOT_VERIFIED = "STATUS NOT VERIFIED"
    MANUAL = "MANUAL LOG INVOKED"
    RESET = "VARIABLES RESET"
    RESTART = "PROGRAM RESTART"


class MyWindow:
    def __init__(self, name):
        ground_station_path = os.getcwd()
        self.status_log_path = os.path.join(ground_station_path, "logs/status_log.txt")
        self.image_folder_path = os.path.join(ground_station_path, "res/img")

        self.name = name
        self.width = 1920
        self.height = 600

        self.data_column = 10
        self.labels_column = self.data_column - 2

        self.command_row = 7
        self.command_column = 3

        self.mission_status = Status.NOT_VERIFIED
        self.display_mission_status_text = StringVar()
        self.change_status_display(self.mission_status)
        self.display_mission_status = Label(self.name, textvariable=self.display_mission_status_text)

        self.abort_method = None

        self.verify_button = ttk.Button(self.name, text="VERIFY", command=self.verify_message_callback)
        self.abort_button = ttk.Button(self.name, text="ABORT", command=self.abort_message_callback)

        name.title("Ground Station Graphical User Interface v0.2")
        # name.iconbitmap(os.path.join(self.image_folder_path, "MyOrbital.ico"))

        window_geometry = str(self.width) + 'x' + str(self.height)
        self.name.geometry(window_geometry)

        # Environment Data
        self.temperature_data = 15000.0
        self.pressure_data = 6000.0
        self.humidity_data = 100.0

        self.temperature = StringVar()
        self.pressure = StringVar()
        self.humidity = StringVar()

        # System Data
        self.altitude_data = 15000000
        self.direction_data = .1234
        self.acceleration_data = 90
        self.velocity_data = 12
        self.user_angle_data = 458

        self.altitude = StringVar()
        self.direction = StringVar()
        self.acceleration = StringVar()
        self.velocity = StringVar()
        self.user_angle = StringVar()

        # Set up GPIO pins for use, see documentation for pin layout
        # orange wire
        self.launch_signal = 11
        # yellow wire
        self.on_signal = 12
        # white wire
        self.gui_switch = 7

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.launch_signal, GPIO.IN)
        GPIO.setup(self.on_signal, GPIO.OUT)
        GPIO.setup(self.gui_switch, GPIO.OUT)

        GPIO.output(self.on_signal, GPIO.HIGH)
        GPIO.output(self.on_signal, GPIO.LOW)
        GPIO.output(self.gui_switch, GPIO.LOW)

        self.display_variables()
        self.make_tool_bar()

        self.make_grid()
        self.make_command_section()
        self.make_environmental_section()
        self.make_system_section()

        self.my_timer = Timer(name, 0, self.command_row - 1, 0, self.labels_column - 1)

    def display_variables(self):
        self.temperature.set(self.temperature_data)
        self.pressure.set(self.pressure_data)
        self.humidity.set(self.humidity_data)

        self.altitude.set(self.altitude_data)
        self.direction.set(self.direction_data)
        self.acceleration.set(self.acceleration_data)
        self.velocity.set(self.velocity_data)
        self.user_angle.set(self.user_angle_data)

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
        program_menu.add_command(label="Log", command=self.log_menu)

        help_menu.add_command(label="Help Index", command=self.do_nothing)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.about_menu)

        self.name.config(menu=menu_bar)

    def make_grid(self):
        total_rows = 12
        total_columns = self.data_column + 1

        my_rows = range(0, total_rows)
        my_columns = range(0, total_columns)

        for column in my_columns:
            self.name.columnconfigure(column, weight=1)

        for row in my_rows:
            self.name.rowconfigure(row, weight=1, uniform=1)

    def make_environmental_section(self):
        # Create and Place Section Header
        environmental_data_label = Label(self.name, text="Environmental Data", font=('times', 15, 'underline'))
        environmental_data_label.grid(row=0, column=self.labels_column, columnspan=self.data_column, sticky=N+S+E+W)

        # Create and Place Labels for Data
        temperature_label = Label(self.name, text="Temperature (Celsius):")
        pressure_label = Label(self.name, text="Pressure (kPa):")
        humidity_label = Label(self.name, text="Humidity (Percent):")

        temperature_label.grid(row=1, column=self.labels_column)
        pressure_label.grid(row=2, column=self.labels_column)
        humidity_label.grid(row=3, column=self.labels_column)

        # Place Data Across from Corresponding Label
        temperature_data = Label(self.name, textvariable=self.temperature)
        pressure_data = Label(self.name, textvariable=self.pressure)
        humidity_data = Label(self.name, textvariable=self.humidity)

        temperature_data.grid(row=1, column=self.data_column)
        pressure_data.grid(row=2, column=self.data_column)
        humidity_data.grid(row=3, column=self.data_column)

    def make_system_section(self):
        space = 5

        # Create and Place Section Header
        system_data_label = Label(self.name, text="System Data", font=('times', 15, 'underline'))
        system_data_label.grid(row=space, column=self.labels_column, columnspan=self.data_column, sticky=N+S+E+W)

        # Create and Place Labels for Data
        altitude_label = Label(self.name, text="Altitude (km):")
        direction_label = Label(self.name, text="Direction(rad):")
        acceleration_label = Label(self.name, text="Acceleration (m/s/s):")
        velocity_label = Label(self.name, text="Velocity (m/s):")
        angle_label = Label(self.name, text="Angle (rad):")

        altitude_label.grid(row=space + 1, column=self.labels_column)
        direction_label.grid(row=space + 2, column=self.labels_column)
        acceleration_label.grid(row=space + 3, column=self.labels_column)
        velocity_label.grid(row=space + 4, column=self.labels_column)
        angle_label.grid(row=space + 5, column=self.labels_column)

        # Place Data Across from Corresponding Label
        altitude_data = Label(self.name, textvariable=self.altitude)
        direction_data = Label(self.name, textvariable=self.direction)
        acceleration_data = Label(self.name, textvariable=self.acceleration)
        velocity_data = Label(self.name, textvariable=self.velocity)
        angle_data = Label(self.name, textvariable=self.user_angle)

        altitude_data.grid(row=space + 1, column=self.data_column)
        direction_data.grid(row=space + 2, column=self.data_column)
        acceleration_data.grid(row=space + 3, column=self.data_column)
        velocity_data.grid(row=space + 4, column=self.data_column)
        angle_data.grid(row=space + 5, column=self.data_column)

    def make_command_section(self):
        mission_status_label = Label(self.name, text="Current Status", font=('times', 15, 'underline'))
        mission_status_label.grid(row=self.command_row, column=self.command_column-1,
                                  columnspan=self.command_column + 1, sticky=N+S+E+W)

        self.display_mission_status = Label(self.name, textvariable=self.display_mission_status_text, font=('times',
                                                                                                            20, 'bold'))
        self.display_mission_status.grid(row=self.command_row + 1, column=self.command_column-1,
                                         columnspan=self.command_column+1, sticky=N+S+E+W)

        self.verify_button = ttk.Button(self.name, text="VERIFY", command=self.verify_message_callback)
        self.verify_button.grid(row=self.command_row + 2, column=self.command_column-1,
                                columnspan=self.command_column+1, sticky=N+S+E+W)

        self.abort_button = ttk.Button(self.name, text="ABORT", command=self.abort_message_callback)
        self.abort_button.grid(row=self.command_row + 3, column=self.command_column-1,
                               columnspan=self.command_column+1, sticky=N+S+E+W)

    def log(self, status):
        fo = open(self.status_log_path, "a")
        current_date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        if status == Status.ABORT:
            fo.write("-------MISSION ABORTED-------\n")
        elif status == Status.VERIFIED:
            fo.write("-------STATUS VERIFIED-------\n")
        elif status == Status.MANUAL:
            fo.write("-----MANUAL LOG INVOKED------\n")
        elif status == Status.RESET:
            fo.write("-------VARIABLES RESET-------\n")
        elif status == Status.RESTART:
            fo.write("-------PROGRAM RESTART-------\n")
        elif status == Status.NOT_VERIFIED:
            fo.write("-----STATUS NOT VERIFIED-----\n")

        fo.write("DATE:" + current_date + "\n")
        fo.write("TIMESTAMP:" + repr(self.my_timer.current_time) + "\n")
        fo.write("*****************************\n")
        fo.write("----------LOGS START---------\n")
        fo.write("temperature = " + repr(self.temperature_data) + "\n")
        fo.write("pressure = " + repr(self.pressure_data) + "\n")
        fo.write("humidity = " + repr(self.humidity_data) + "\n")
        fo.write("altitude = " + repr(self.altitude_data) + "\n")
        fo.write("direction = " + repr(self.direction_data) + "\n")
        fo.write("acceleration = " + repr(self.acceleration_data) + "\n")
        fo.write("velocity = " + repr(self.velocity_data) + "\n")
        fo.write("----------LOGS END-----------\n")
        fo.write("-----------------------------\n\n")
        fo.close()

    def log_menu(self):
        log_window = Toplevel(self.name)
        log_window.title("Manual Log")
        logged_label = Label(log_window, text="The current variables have been logged in 'logs/status_log.txt'")
        logged_label.pack()
        button = Button(log_window, text="Close", command=lambda: log_window.destroy())
        button.pack()
        self.log(Status.MANUAL)

    def about_menu(self):

        about_text = "Ground Station Graphical User Interface Version 0.2\n\n" \
                    "Author: Matt Drozt, Ken Sodetz\n" \
                    "Since: 11/27/2018\n\n" \
                    "Created for Purdue Orbital Electrical and Software Sub team\n\n" \
                    "Parses and displays data from the a Raspberry Pi 3 to verbosely display all\n" \
                    "pertinent system data " \
                    "(data that can be changed) and environmental data\n(data that cannot be changed)"

        about_window = Toplevel(self.name)
        about_window.title("About")
        about_window.resizable(width=False, height=False)
        text = Text(about_window)
        text.insert(INSERT, about_text)
        text.config(state=DISABLED)
        text.pack()
        self.name.img = img = PhotoImage(file=os.path.join(self.image_folder_path, "orbital-logo-reduced.gif"))
        logo = Label(about_window, image=img)
        logo.place(x=0, y=200)
        button = Button(about_window, text="Close", command=lambda: about_window.destroy())
        button.pack()

    def do_nothing(self):
        file_window = Toplevel(self.name)
        button = Button(file_window, text="Close", command=lambda: file_window.destroy())
        button.pack()

    def restart_program(self):
        python = sys.executable
        GPIO.output(self.gui_switch, GPIO.LOW)
        GPIO.cleanup()
        self.log(Status.RESTART)
        os.execl(python, python, *sys.argv)

    def reset_variables_window(self):
        # Creates a pop up window that asks if you are sure that you want to rest the variables.
        # If yes then all the variables are reset
        reset_window = messagebox.askokcancel("Reset All Variables?", "Are you sure you want to reset all variables?")
        if reset_window:
            self.log(Status.RESET)
            self.reset_variables()

    def reset_variables(self):
        # Resets all of the data on screen to zero

        GPIO.output(self.gui_switch, GPIO.LOW)
        self.temperature_data = 0.0
        self.pressure_data = 0.0
        self.humidity_data = 0.0

        self.altitude_data = 0.0
        self.direction_data = 0.0
        self.acceleration_data = 0.0
        self.velocity_data = 0.0
        self.user_angle_data = 0.0

        self.display_variables()

    def verify_message_callback(self):
        if self.mission_status == Status.NOT_VERIFIED:
            verify_response = messagebox.askyesno("Verify Mission?", "Do you want to verify the mission")
            if verify_response:
                self.mission_status = Status.VERIFIED
                self.change_status_display(self.mission_status)
                self.log(self.mission_status)
                GPIO.output(self.gui_switch, GPIO.HIGH)
                self.my_timer.start = time.time()
                self.my_timer.clock_run = True
                self.my_timer.tick()
                self.verify_button.config(text="UNVERIFY")

        elif self.mission_status == Status.VERIFIED:
            verify_response = messagebox.askyesno("Unverify Mission?", "Do you want to unverify the mission")
            if verify_response:
                self.mission_status = Status.NOT_VERIFIED
                self.change_status_display(self.mission_status)
                self.log(self.mission_status)
                self.my_timer.clock_run = False
                self.verify_button.config(text="VERIFY")

        elif self.mission_status == Status.ABORT:
            verify_response = messagebox.askyesno("Verify Mission?", "Do you want to verify the mission")
            if verify_response:
                self.mission_status = Status.VERIFIED
                self.change_status_display(self.mission_status)
                self.log(self.mission_status)
                self.my_timer.start = time.time()
                self.my_timer.clock_run = True
                self.my_timer.tick()
                self.verify_button.config(text="UNVERIFY")

    def abort_message_callback(self):
        abort_response = messagebox.askyesno("Abort Mission?", "Do you really want to abort the mission?")
        if abort_response:
            self.abort_method_window()

    def abort_method_window(self):
        method_window = Toplevel(self.name)
        method_window.geometry("250x150")
        method_window.resizable(width=False, height=False)

        cmd_button = ttk.Button(method_window, text="CMD", width=20, command=lambda: self.select_cdm(method_window))
        qdm_button = ttk.Button(method_window, text="QDM", width=20, command=lambda: self.select_qdm(method_window))
        exit_button = ttk.Button(method_window, text="Close", width=20, command=lambda: method_window.destroy())

        msg = Message(method_window, text="Please select a mission abort method", font=('times', 12, 'bold'), width=200,
                      justify=CENTER, pady=15)

        msg.pack()
        cmd_button.pack()
        qdm_button.pack()
        exit_button.pack()

    def select_cdm(self, close_window):
        self.abort_method = "CDM"
        self.mission_status = Status.ABORT
        self.log(self.mission_status)
        self.my_timer.clock_run = False
        self.verify_button.config(text="VERIFY")
        self.change_status_display(self.mission_status)
        GPIO.output(self.gui_switch, GPIO.LOW)
        close_window.destroy()

    def select_qdm(self, close_window):
        self.abort_method = "QDM"
        self.mission_status = Status.ABORT
        self.my_timer.clock_run = False
        self.verify_button.config(text="VERIFY")
        self.log(self.mission_status)
        self.change_status_display(self.mission_status)
        GPIO.output(self.gui_switch, GPIO.LOW)
        close_window.destroy()

    def change_status_display(self, status):
        if status == Status.ABORT:
            self.display_mission_status_text.set("ABORT")
        elif status == Status.NOT_VERIFIED:
            self.display_mission_status_text.set("NOT VERIFIED")
        elif status == Status.VERIFIED:
            self.display_mission_status_text.set("VERIFIED")


root = Tk()
window = MyWindow(root)

root.mainloop()
GPIO.cleanup()
