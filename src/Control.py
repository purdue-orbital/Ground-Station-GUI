from Status import *
from tkinter import *
from tkinter import ttk


class Control:
    def __init__(self, place_window, command_row, command_column):
        self.mission_status = Status.NOT_VERIFIED
        self.display_mission_status_text = StringVar()
        self.change_status_display(self.mission_status)
        self.display_mission_status = Label(place_window, textvariable=self.display_mission_status_text)

        mission_status_label = Label(place_window, text="Current Status", font=('times', 15, 'underline'))
        mission_status_label.grid(row=command_row, column=command_column - 1,
                                  columnspan=command_column + 1, sticky=N + S + E + W)

        self.display_mission_status = Label(place_window, textvariable=self.display_mission_status_text,
                                            font=('times', 20, 'bold'))
        self.display_mission_status.grid(row=command_row + 1, column=command_column - 1,
                                         columnspan=command_column + 1, sticky=N + S + E + W)

        self.verify_button = ttk.Button(place_window, text="VERIFY")
        self.verify_button.grid(row=command_row + 2, column=command_column - 1,
                                columnspan=command_column + 1, sticky=N + S + E + W)

        self.abort_button = ttk.Button(place_window, text="ABORT")
        self.abort_button.grid(row=command_row + 3, column=command_column - 1,
                               columnspan=command_column + 1, sticky=N + S + E + W)

    def change_status_display(self, status):
        if status == Status.ABORT:
            self.display_mission_status_text.set("ABORT")
        elif status == Status.NOT_VERIFIED:
            self.display_mission_status_text.set("NOT VERIFIED")
        elif status == Status.VERIFIED:
            self.display_mission_status_text.set("VERIFIED")