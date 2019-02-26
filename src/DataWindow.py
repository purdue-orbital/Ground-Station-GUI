import datetime
import time
import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import RPi.GPIO as GPIO

from Status import *
from Timer import Timer
from Data import Data
from Control import Control

"""
ROCKET GUI Version 0.2
Author: Matt Drozt, Ken Sodetz, Jay Rixie, Emanuel Pituch
Since: 10/31/2018
Created for Purdue Orbital Ground Stations Sub-Team
Parses and displays data from the a Raspberry Pi 3 to verbosely
display all pertinent system data (data that can be changed) and environmental
data (data that cannot be changed).
"""


class DataWindow:
    def __init__(self, name, queue):
        self.queue = queue

        # Base file writing from program's execution directory
        program_path = os.path.dirname(os.path.realpath(__file__))
        self.status_log_path = os.path.join(program_path, "../logs/status.log")
        self.image_folder_path = os.path.join(program_path, "../res/img")

        self.name = name

        self.abort_method = None

        name.title("Ground Station Graphical User Interface v0.2")
        # name.iconbitmap(os.path.join(self.image_folder_path, "MyOrbital.ico"))

        self.name.geometry('1000x600')

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

        self.make_tool_bar()

        self.make_grid()

        self.start_timer = Timer(name, 0, 3, 0, 7)
        self.timer = Timer(name, 3, 3, 0, 7)
        self.data = Data(name, 8, 10)
        self.control = Control(name, 7, 3)

        self.control.verify_button.config(command=self.verify_message_callback)
        self.control.abort_button.config(command=self.abort_message_callback)

        # Running variable to see if program was terminated
        self.running = 1

        # Running variable to check if in testing mode
        self.testing = 0

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
        file_menu.add_command(label="Exit", command=self.close)

        program_menu.add_command(label="Start Mission", command=self.start_mission)
        program_menu.add_command(label="Reset", command=self.reset_variables_window)
        program_menu.add_command(label="Log", command=self.log_menu)

        help_menu.add_command(label="Help Index", command=self.do_nothing)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self.about_menu)

        self.name.config(menu=menu_bar)

    def make_grid(self):
        total_rows = 12
        total_columns = 12

        my_rows = range(0, total_rows)
        my_columns = range(0, total_columns)

        for column in my_columns:
            self.name.columnconfigure(column, weight=1)

        for row in my_rows:
            self.name.rowconfigure(row, weight=1, uniform=1)

    def start_mission(self):
        self.start_timer.start = time.time()
        self.start_timer.clock_run = True
        self.start_timer.tick()

        self.control.verify_button.state(["!disabled"])
        self.control.abort_button.state(["!disabled"])

    def reset_variables_window(self):
        # Creates a pop up window that asks if you are sure that you want to rest the variables.
        # If yes then all the variables are reset
        reset_window = messagebox.askokcancel("Reset All Variables?", "Are you sure you want to reset all variables?")
        if reset_window:
            self.log(Status.RESET)
            self.data.reset_variables()

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
        fo.write("MISSION START TIMESTAMP:" + repr(self.start_timer.current_time) + "\n")
        fo.write("VERIFY START TIMESTAMP:" + repr(self.timer.current_time) + "\n")
        fo.write("*****************************\n")
        fo.write("----------LOGS START---------\n")
        fo.write("temperature = " + repr(self.data.temperature_data) + "\n")
        fo.write("pressure = " + repr(self.data.pressure_data) + "\n")
        fo.write("humidity = " + repr(self.data.humidity_data) + "\n")
        fo.write("altitude = " + repr(self.data.altitude_data) + "\n")
        fo.write("direction = " + repr(self.data.direction_data) + "\n")
        fo.write("acceleration = " + repr(self.data.acceleration_data) + "\n")
        fo.write("velocity = " + repr(self.data.velocity_data) + "\n")
        fo.write("----------LOGS END-----------\n")
        fo.write("-----------------------------\n\n")
        fo.close()

    def log_menu(self):
        log_window = Toplevel(self.name)
        log_window.title("Manual Log")
        logged_label = Label(log_window, text="The current variables have been logged in 'logs/status.log'")
        logged_label.pack()
        button = Button(log_window, text="Close", command=lambda: log_window.destroy())
        button.pack()
        self.log(Status.MANUAL)

    def about_menu(self):

        about_text = "Ground Station Graphical User Interface Version 0.2\n\n" \
                     "Author: Matt Drozt, Ken Sodetz, Jay Rixie, Emanuel Pituch\n" \
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

    def verify_message_callback(self):
        if self.control.mission_status == Status.NOT_VERIFIED:
            verify_response = messagebox.askyesno("Verify Mission?", "Do you want to verify the mission")
            if verify_response:
                self.control.mission_status = Status.VERIFIED
                self.control.change_status_display(self.control.mission_status)
                self.log(self.control.mission_status)
                GPIO.output(self.gui_switch, GPIO.HIGH)
                self.timer.start = time.time()
                self.timer.clock_run = True
                self.timer.tick()
                self.control.verify_button.config(text="UNVERIFY")

        elif self.control.mission_status == Status.VERIFIED:
            verify_response = messagebox.askyesno("Unverify Mission?", "Do you want to unverify the mission")
            if verify_response:
                self.control.mission_status = Status.NOT_VERIFIED
                self.control.change_status_display(self.control.mission_status)
                self.log(self.control.mission_status)
                self.timer.clock_run = False
                self.control.verify_button.config(text="VERIFY")

        elif self.control.mission_status == Status.ABORT:
            verify_response = messagebox.askyesno("Verify Mission?", "Do you want to verify the mission")
            if verify_response:
                self.control.mission_status = Status.VERIFIED
                self.control.change_status_display(self.control.mission_status)
                self.log(self.control.mission_status)
                self.timer.start = time.time()
                self.timer.clock_run = True
                self.timer.tick()
                self.control.verify_button.config(text="UNVERIFY")

    def abort_message_callback(self):
        abort_response = messagebox.askyesno("Abort Mission?", "Do you really want to abort the mission?")
        if abort_response:
            self.abort_method_window()

    def abort_method_window(self):
        method_window = Toplevel(self.name)
        method_window.geometry("250x200")
        method_window.resizable(width=False, height=False)

        cmd_button = ttk.Button(method_window, text="CMD", width=20, command=lambda: self.select_cdm(method_window))
        qdm_button = ttk.Button(method_window, text="QDM", width=20, command=lambda: self.select_qdm(method_window))
        exit_button = ttk.Button(method_window, text="Close", width=20, command=lambda: self.name.destroy())

        msg = Message(method_window, text="Please select a mission abort method", font=('times', 12, 'bold'), width=200,
                      justify=CENTER, pady=15)

        msg.pack()
        cmd_button.pack()
        qdm_button.pack()
        exit_button.pack()

    def select_cdm(self, close_window):
        self.abort_method = "CDM"
        self.control.mission_status = Status.ABORT
        self.log(self.control.mission_status)
        self.timer.clock_run = False
        self.control.verify_button.config(text="VERIFY")
        self.control.change_status_display(self.control.mission_status)
        GPIO.output(self.gui_switch, GPIO.LOW)
        close_window.destroy()

    def select_qdm(self, close_window):
        self.abort_method = "QDM"
        self.control.mission_status = Status.ABORT
        self.timer.clock_run = False
        self.control.verify_button.config(text="VERIFY")
        self.log(self.control.mission_status)
        self.control.change_status_display(self.control.mission_status)
        GPIO.output(self.gui_switch, GPIO.LOW)
        close_window.destroy()

    def process_incoming(self):
        # Process data in queue
        while self.queue.qsize():
            try:
                data_json = self.queue.get(0)
                # Set the data variables equal to the corresponding json entries
                self.data.temperature_data = data_json["temperature"]
                self.data.pressure_data = data_json["pressure"]
                self.data.humidity_data = data_json["humidity"]
                self.data.altitude_data = data_json["altitude"]
                self.data.direction_data = data_json["direction"]
                self.data.acceleration_data = data_json["acceleration"]
                self.data.velocity_data = data_json["velocity"]
                self.data.user_angle_data = data_json["user_angle"]
                # Reload variables
                self.data.display_variables()
            except self.queue.Empty:
                pass

    def set_testing(self, isTesting):
        self.testing = isTesting

    def close(self):
        self.running = 0