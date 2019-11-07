from Status import *
from tkinter import *
from tkinter import ttk


class Control:
    def __init__(self, place_window, command_row, command_column, col_span, bg):

        self.mission_status = Status.NOT_VERIFIED
        self.display_mission_status_text = StringVar()
        self.change_status_display(self.mission_status)
        self.display_mission_status = Label(place_window, textvariable=self.display_mission_status_text)

        # Config Status Label
        mission_status_label = Label(place_window, text="Current Status", font=('times', 15, 'underline'), bg=bg)
        mission_status_label.grid(row=command_row, column=command_column,
                                  columnspan=col_span, sticky=N + S + E + W)

        self.display_mission_status = Label(place_window, textvariable=self.display_mission_status_text,
                                            font=('times', 20, 'bold'), bg=bg)
        self.display_mission_status.grid(row=command_row + 1, column=command_column,
                                         columnspan=col_span, sticky=N + S + E + W)

        # Config button styles
        ttk.Style().configure("green.TButton", background="green")
        ttk.Style().configure("red.TButton", background="red")

        # Config Verify Button
        self.verify_button = ttk.Button(place_window, text="VERIFY", style="green.TButton")
        self.verify_button.grid(row=command_row + 2, column=command_column,
                                columnspan=col_span, sticky=N + S + E + W)

        # Config Abort Button
        self.abort_button = ttk.Button(place_window, text="ABORT", style="red.TButton")
        self.abort_button.grid(row=command_row + 3, column=command_column,
                               columnspan=col_span, sticky=N + S + E + W)

        self.verify_button.state(["disabled"])
        self.abort_button.state(["disabled"])

    def change_status_display(self, status):
        if status == Status.ABORT:
            self.display_mission_status_text.set("ABORT")
        elif status == Status.NOT_VERIFIED:
            self.display_mission_status_text.set("NOT VERIFIED")
        elif status == Status.VERIFIED:
            self.display_mission_status_text.set("VERIFIED")
        elif status == Status.LAUNCHED:
            self.display_mission_status_text.set("LAUNCHED")
        elif status == Status.TIMEOUT:
            self.display_mission_status_text.set("RADIO TIME OUT")

