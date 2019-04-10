import datetime
import time
import os
import queue
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import RPi.GPIO as GPIO

from Status import Status
from Timer import Timer
from Data import Data
from Mode import Mode
from Control import Control
from CommunicationDriver import Comm
from QualityCheck import QualityCheck
from AltitudeGraph import AltitudeGraph
from AccelerometerGyroGraphs import AccelerometerGyroGraphs


class DataWindow:
    def __init__(self, name, data_queue):
        self.queue = data_queue
        bg_color = "#484949"
        frames_bg = "#969694"
        self.framesBg = frames_bg
        time_bg = "#1e1e1e"
        yellow = "#f8fc16"

        # Base file writing from program's execution directory
        program_path = os.path.dirname(os.path.realpath(__file__))
        self.status_log_path = os.path.join(program_path, "../logs/status.log")
        self.image_folder_path = os.path.join(program_path, "../res/img")

        self.name = name

        self.abort_method = None

        name.title("Ground Station Graphical User Interface v0.2")
        # name.iconbitmap(os.path.join(self.image_folder_path, "MyOrbital.ico"))

        self.name.geometry('1000x600')
        self.name.configure(bg=bg_color)

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

        # Make timer sections
        self.start_timer = Timer(name, 0, 2, 0, 5, time_bg)
        self.timer = Timer(name, 2, 2, 0, 5, time_bg)

        # Make data sections
        self.dataRocket = Data(name, "Rocket Data", 6, 8, frames_bg)
        self.dataBalloon = Data(name, "Balloon Data", 9, 11, frames_bg)

        # Config button styles
        ttk.Style().configure("yellow.TButton", background=yellow)

        # Place Graph buttons TODO: Move these to data class
        self.init_graph_queues()
        self.altGraph = ttk.Button(name, text="Altitude", style="yellow.TButton", command=self.open_altitude_graph)
        self.sixGraph = ttk.Button(name, text="Direction", style="yellow.TButton", command=self.open_acc_gyro_graphs)
        self.altGraph.grid(column=6, columnspan=3, row=11, rowspan=1, sticky=N + S + E + W)
        self.sixGraph.grid(column=9, columnspan=3, row=11, rowspan=1, sticky=N + S + E + W)

        # Adds our logo
        logo = PhotoImage(file=os.path.join(self.image_folder_path, "orbital-logo-reduced.gif"))
        logo_label = Label(name, image=logo)
        logo_label.image = logo
        logo_label.grid(row=12, column=6, rowspan=5, columnspan=6)

        self.control = Control(name, 5, 2, 1, frames_bg)

        # Graph Initialization
        self.altitude_graph = AltitudeGraph()

        # Place Quality Indicators and Labels
        self.QDM_check = QualityCheck(name, "QDM", 1, 10, frames_bg)
        self.CDM_check = QualityCheck(name, "CDM", 3, 10, frames_bg)

        self.drogue_check = QualityCheck(name, "Drogue Chute", 1, 12, frames_bg)
        self.ignition_check = QualityCheck(name, "Ignition", 2, 12, frames_bg)
        self.main_check = QualityCheck(name, "Main Chute", 3, 12, frames_bg)

        self.platform_stability_check = QualityCheck(name, "Platform Stability", 1, 14, frames_bg)
        self.CRASH_check = QualityCheck(name, "CRASH System", 3, 14, frames_bg)

        self.control.verify_button.config(command=self.verify_message_callback)
        self.control.abort_button.config(command=self.abort_message_callback)

        # Running variable to see if program was terminated
        self.running = 1

    def init_graph_queues(self):
        # Create several queue that holds the number for each line in every graph
        self.baloon_acc_xQ = queue.Queue()
        self.baloon_acc_yQ = queue.Queue()
        self.baloon_acc_zQ = queue.Queue()
        self.baloon_gyro_xQ = queue.Queue()
        self.baloon_gyro_yQ = queue.Queue()
        self.baloon_gyro_zQ = queue.Queue()
        self.rocket_acc_xQ = queue.Queue()
        self.rocket_acc_yQ = queue.Queue()
        self.rocket_acc_zQ = queue.Queue()
        self.rocket_gyro_xQ = queue.Queue()
        self.rocket_gyro_yQ = queue.Queue()
        self.rocket_gyro_zQ = queue.Queue()
        self.alititudeQ = queue.Queue()

        amount_of_point_to_graph = 20
        for i in range(0, amount_of_point_to_graph):
            self.baloon_acc_xQ.put(0)
            self.baloon_acc_yQ.put(0)
            self.baloon_acc_zQ.put(0)
            self.baloon_gyro_xQ.put(0)
            self.baloon_gyro_yQ.put(0)
            self.baloon_gyro_zQ.put(0)
            self.rocket_acc_xQ.put(0)
            self.rocket_acc_yQ.put(0)
            self.rocket_acc_zQ.put(0)
            self.rocket_gyro_xQ.put(0)
            self.rocket_gyro_yQ.put(0)
            self.rocket_gyro_zQ.put(0)
            self.alititudeQ.put(0)

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
        total_rows = 18
        total_columns = 12

        my_rows = range(0, total_rows)
        my_columns = range(0, total_columns)

        for column in my_columns:
            self.name.columnconfigure(column, weight=1)

        for row in my_rows:
            self.name.rowconfigure(row, weight=1, uniform=1)

        for col in range(1, 4):
            for row in range(5, 16):
                color_frame = Label(self.name, bg=self.framesBg)
                color_frame.grid(row=row, column=col, sticky=N + S + E + W)

    def start_mission(self):
        if not self.start_timer.clock_run:
            self.start_timer.start = time.time()
            self.start_timer.clock_run = True
            self.start_timer.tick()

        self.control.verify_button.state(["!disabled"])
        self.control.abort_button.state(["!disabled"])

        Comm.get_instance(self).testing()
        Comm.get_instance(self).send("Starting")

    def reset_variables_window(self):
        # Creates a pop up window that asks if you are sure that you want to rest the variables.
        # If yes then all the variables are reset
        reset_window = messagebox.askokcancel("Reset All Variables?", "Are you sure you want to reset all variables?")
        if reset_window:
            self.log(Status.RESET)
            self.dataBalloon.reset_variables()
            self.dataRocket.reset_variables()

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
        fo.write("----------ROCKET DATA--------\n")
        fo.write("Longitude = " + repr(self.dataRocket.longitude_data) + "\n")
        fo.write("Latitude = " + repr(self.dataRocket.latitude_data) + "\n")
        fo.write("Gyro(X) = " + repr(self.dataRocket.gyroX_data) + "\n")
        fo.write("Gyro(Y) = " + repr(self.dataRocket.gyroY_data) + "\n")
        fo.write("Gyro(Z) = " + repr(self.dataRocket.gyroZ_data) + "\n")
        fo.write("Cardinal Direction = " + repr(self.dataRocket.cardinalDirection_data) + "\n")
        fo.write("Temperature = " + repr(self.dataRocket.temperature_data) + "\n")
        fo.write("Acceleration(X) = " + repr(self.dataRocket.accelX_data) + "\n")
        fo.write("Acceleration(Y) = " + repr(self.dataRocket.accelY_data) + "\n")
        fo.write("Acceleration(Z) = " + repr(self.dataRocket.accelZ_data) + "\n")
        fo.write("----------BALLOON DATA-------\n")
        fo.write("Longitude = " + repr(self.dataBalloon.longitude_data) + "\n")
        fo.write("Latitude = " + repr(self.dataBalloon.latitude_data) + "\n")
        fo.write("Gyro(X) = " + repr(self.dataBalloon.gyroX_data) + "\n")
        fo.write("Gyro(Y) = " + repr(self.dataBalloon.gyroY_data) + "\n")
        fo.write("Gyro(Z) = " + repr(self.dataBalloon.gyroZ_data) + "\n")
        fo.write("Cardinal Direction = " + repr(self.dataBalloon.cardinalDirection_data) + "\n")
        fo.write("Temperature = " + repr(self.dataBalloon.temperature_data) + "\n")
        fo.write("Acceleration(X) = " + repr(self.dataBalloon.accelX_data) + "\n")
        fo.write("Acceleration(Y) = " + repr(self.dataBalloon.accelY_data) + "\n")
        fo.write("Acceleration(Z) = " + repr(self.dataBalloon.accelZ_data) + "\n")
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
                     "Author: Ken Sodetz, Matt Drozt, Jay Rixie, Emanuel Pituch\n" \
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

        cmd_button = ttk.Button(method_window, text="CDM", width=20, command=lambda: self.select_cdm(method_window))
        qdm_button = ttk.Button(method_window, text="QDM", width=20, command=lambda: self.select_qdm(method_window))
        exit_button = ttk.Button(method_window, text="Close", width=20, command=lambda: self.name.destroy())

        msg = Message(method_window, text="Please select a mission abort method", font=('times', 12, 'bold'), width=200,
                      justify=CENTER, pady=15)

        msg.pack()
        cmd_button.pack()
        qdm_button.pack()
        exit_button.pack()
        # send_button.pack()

    def test_launch(self):
        c = Comm.get_instance(self)
        m = c.get_mode()

        c.testing()
        c.send("launch")
        c.set_mode(m)

    def test_launch(self):
        c = Comm.get_instance(self)
        m = c.get_mode()

        c.testing()
        c.send("abort")
        c.set_mode(m)

    def test_launch(self):
        c = Comm.get_instance(self)
        m = c.get_mode()

        c.testing()
        c.send("stability")
        c.set_mode(m)

    def select_cdm(self, close_window):
        c = Comm.get_instance(self)
        c.flight()
        c.send("cdm")

        self.abort_method = "CDM"
        self.control.mission_status = Status.ABORT
        self.log(self.control.mission_status)
        self.timer.clock_run = False
        self.control.verify_button.config(text="VERIFY")
        self.control.change_status_display(self.control.mission_status)
        GPIO.output(self.gui_switch, GPIO.LOW)
        close_window.destroy()

    def select_qdm(self, close_window):
        # TODO Make Comms Global
        c = Comm.get_instance(self)
        c.flight()
        c.send("qdm")

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
                data_json = self.queue.get()

                print(data_json)
                origin = data_json["origin"]

                if origin == "rocket":
                    data = self.dataRocket
                elif origin == "balloon":
                    data = self.dataBalloon
                else:
                    print("JSON ORIGIN INCORRECT")

                alt = data_json["alt"]

                data.altitude_data = data_json["alt"]

                gps_json = data_json["GPS"]
                data.longitude_data = gps_json["long"]
                data.latitude_data = gps_json["lat"]
                gyro_json = data_json["gyro"]
                data.gyroX_data = gyro_json["x"]
                data.gyroY_data = gyro_json["y"]
                data.gyroZ_data = gyro_json["z"]
                data.cardinalDirection_data = data_json["mag"]
                data.temperature_data = data_json["temp"]
                acc_json = data_json["acc"]
                data.accelX_data = acc_json["x"]
                data.accelY_data = acc_json["y"]
                data.accelZ_data = acc_json["z"]

                data.display_variables()
                self.altitude_graph.update_altitude(alt)

                # insert it into the queues
                self.alititudeQ.get()
                self.alititudeQ.put(alt)
                # altitude_graph.update_altitude(self.alititudeQ)
                # if origin == "rocket":
                #     self.rocket_acc_xQ.get()
                #     self.rocket_acc_yQ.get()
                #     self.rocket_acc_zQ.get()
                #     self.rocket_gyro_xQ.get()
                #     self.rocket_gyro_yQ.get()
                #     self.rocket_gyro_zQ.get()
                #     self.rocket_acc_xQ.put(data.accelX_data)
                #     self.rocket_acc_yQ.put(data.accelY_data)
                #     self.rocket_acc_zQ.put(data.accelZ_data)
                #     self.rocket_gyro_xQ.put(data.gyroX_data)
                #     self.rocket_gyro_yQ.put(data.gyroY_data)
                #     self.rocket_gyro_zQ.put(data.gyroZ_data)
                #     self.acc_gyro_graphs.update_rocket_acc(self.rocket_acc_xQ, self.rocket_acc_yQ, self.rocket_acc_zQ)
                #     self.acc_gyro_graphs.update_rocket_gyro(self.rocket_gyro_xQ, self.rocket_gyro_yQ,
                #                                             self.rocket_gyro_zQ)
                # elif origin == "balloon":
                #     # TODO None of these are initialized
                #     self.balloon_acc_xQ.get()
                #     self.balloon_acc_yQ.get()
                #     self.balloon_acc_zQ.get()
                #     self.balloon_gyro_xQ.get()
                #     self.balloon_gyro_yQ.get()
                #     self.balloon_gyro_zQ.get()
                #     self.balloon_acc_xQ.put(data.accelX_data)
                #     self.balloon_acc_yQ.put(data.accelY_data)
                #     self.balloon_acc_zQ.put(data.accelZ_data)
                #     self.balloon_gyro_xQ.put(data.gyroX_data)
                #     self.balloon_gyro_yQ.put(data.gyroY_data)
                #     self.balloon_gyro_zQ.put(data.gyroZ_data)
                #     self.acc_gyro_graphs.update_balloon_acc(self.baloon_acc_xQ, self.baloon_acc_yQ, self.baloon_acc_zQ)
                #     self.acc_gyro_graphs.update_balloon_gyro(self.baloon_gyro_xQ, self.baloon_gyro_yQ,
                #                                             self.baloon_gyro_zQ)


                # Set the data variables equal to the corresponding json entries
                # self.data.temperature_data = data_json["temperature"]
                # self.data.pressure_data = data_json["pressure"]
                # self.data.humidity_data = data_json["humidity"]
                # self.data.altitude_data = data_json["altitude"]
                # self.data.direction_data = data_json["direction"]
                # self.data.acceleration_data = data_json["acceleration"]
                # self.data.velocity_data = data_json["velocity"]
                # self.data.user_angle_data = data_json["user_angle"]
                # Reload variables

            except queue.Empty:
                pass

    def close(self):
        self.running = 0

    def open_altitude_graph(self):
        self.altitude_graph.update_altitude(self.alititudeQ)

    def open_acc_gyro_graphs(self):
        self.acc_gyro_graphs = AccelerometerGyroGraphs()
        self.acc_gyro_graphs.update_rocket_acc(self.rocket_acc_xQ, self.rocket_acc_yQ, self.rocket_acc_zQ)
        self.acc_gyro_graphs.update_rocket_gyro(self.rocket_gyro_xQ, self.rocket_gyro_yQ, self.rocket_gyro_zQ)
        self.acc_gyro_graphs.update_balloon_acc(self.baloon_acc_xQ, self.baloon_acc_yQ, self.baloon_acc_zQ)
        self.acc_gyro_graphs.update_balloon_gyro(self.baloon_gyro_xQ, self.baloon_gyro_yQ, self.baloon_gyro_zQ)
