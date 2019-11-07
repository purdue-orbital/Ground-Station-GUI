import time
from tkinter import *
from threading import Timer as ThreadingTimer


class Timer:
    def __init__(self, place_window, row_start, row_span, column_start, column_span, bg):
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0
        self.hours = 0
        self.start = 0
        self.clock_run = False

        self.current_time = "00:00:00:00"

        self.clock_frame = Label(place_window, font=('times', 50, 'bold'), bg=bg, fg='white', text="00:00:00:00")
        self.clock_frame.grid(row=row_start, rowspan=row_span, column=column_start, columnspan=column_span,
                              sticky=N + S + E + W)

    def tick(self):
        current_time = str(time.time() - self.start)
        dot = current_time.find('.')
        self.milliseconds = current_time[dot + 1:dot + 3]
        self.seconds = int(current_time[:dot])
        self.minutes = int(self.seconds) // 60
        self.seconds = int(self.seconds) % 60
        self.hours = int(self.minutes) // 60
        self.minutes = int(self.minutes) % 60

        self.current_time = str(self.hours).zfill(2) + ":" + str(self.minutes).zfill(2) + ":" + str(self.seconds).zfill(
            2) + ":" + str(self.milliseconds).zfill(2)

        self.clock_frame.config(text=str(self.hours).zfill(2) + ":" + str(self.minutes).zfill(2)
                                     + ":" + str(self.seconds).zfill(2) + ":" + str(self.milliseconds).zfill(2))

        if self.clock_run:
            self.clock_frame.after(10, self.tick)
        else:
            self.current_time = "00:00:00:00"
            self.clock_frame.config(text="00:00:00:00")


class ShutdownTimer(object):
    def __init__(self, interval, function):
        print("init")
        self.count = 0
        self._timer = None
        self.interval = interval
        self.function = function
        self.is_running = False
        self.start()

    def _run(self):
        print("_run")
        self.start()
        self.function()

    def start(self):
        print("start")
        if not self.is_running:
            self._timer = ThreadingTimer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        print("stop")
        self._timer.cancel()
        self.is_running = False

