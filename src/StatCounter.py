from tkinter import *


class StatCounter:
    def __init__(self, place_window, check_name, column_place, row_place, bg):
        self.counter = 0
        self.counterStrVar = StringVar()
        self.counterStrVar.set(self.counter)

        self.counter_title_label = Label(place_window, text=check_name, font=('times', 12, 'underline'), bg=bg)
        self.counter_title_label.grid(row=row_place, column=column_place, sticky=S + E + W)

        self.counter_label = Label(place_window, textvariable=self.counterStrVar, bg=bg)
        self.counter_label.grid(row=row_place + 1, column=column_place, sticky=N + E + W)

    def count(self):
        self.counter = self.counter + 1
        self.counterStrVar.set(self.counter)

    def set_count(self, count):
        self.counter = count
        self.counterStrVar.set(self.counter)

    def get_count(self):
        return self.counter

    def reset(self):
        self.counter = 0
        self.counterStrVar.set(self.counter)
