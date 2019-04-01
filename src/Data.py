from tkinter import *


class Data:
    def __init__(self, place_window, data_name, labels_column, data_column, bg):
        # Environment Data
        self.longitude_data = 0
        self.latitude_data = 0
        self.gyroX_data = 0
        self.gyroY_data = 0
        self.gyroZ_data = 0
        self.cardinalDirection_data = 0
        self.temperature_data = 0
        self.accelX_data = 0
        self.accelY_data = 0
        self.accelZ_data = 0

        self.longitude = StringVar()
        self.latitude = StringVar()
        self.gyroX = StringVar()
        self.gyroY = StringVar()
        self.gyroZ = StringVar()
        self.cardinalDirection = StringVar()
        self.temperature = StringVar()
        self.accelX = StringVar()
        self.accelY = StringVar()
        self.accelZ = StringVar()

        self.display_variables()

        # Create and Place Section Header
        data_label = Label(place_window, text=data_name, font=('times', 15, 'underline'), bg=bg)
        data_label.grid(row=0, column=labels_column, columnspan=3, sticky=N + S + E + W)

        labelFrames = [
            Label(place_window, text="Longitude:", bg=bg),
            Label(place_window, text="Latitude:", bg=bg),
            Label(place_window, text="Gyro X:", bg=bg),
            Label(place_window, text="Gyro Y:", bg=bg),
            Label(place_window, text="Gyro Z:", bg=bg),
            Label(place_window, text="Direction:", bg=bg),
            Label(place_window, text="Temperature (Celsius):", bg=bg),
            Label(place_window, text="Acceleration X:", bg=bg),
            Label(place_window, text="Acceleration Y:", bg=bg),
            Label(place_window, text="Acceleration Z:", bg=bg)
        ]

        dataFrames = [
            Label(place_window, textvariable=self.longitude, bg=bg),
            Label(place_window, textvariable=self.latitude, bg=bg),
            Label(place_window, textvariable=self.gyroX, bg=bg),
            Label(place_window, textvariable=self.gyroY, bg=bg),
            Label(place_window, textvariable=self.gyroZ, bg=bg),
            Label(place_window, textvariable=self.cardinalDirection, bg=bg),
            Label(place_window, textvariable=self.temperature, bg=bg),
            Label(place_window, textvariable=self.accelX, bg=bg),
            Label(place_window, textvariable=self.accelY, bg=bg),
            Label(place_window, textvariable=self.accelZ, bg=bg)
        ]

        row = 1
        for frame in labelFrames:
            frame.grid(row=row, column=labels_column, sticky=N + S + E + W)
            row += 1

        row = 1
        for frame in dataFrames:
            frame.grid(row=row, column=data_column, sticky=N + S + E + W)
            row += 1

        for i in range(1, data_column - labels_column):
            for j in range(1, 11):
                colorFrame = Label(place_window, bg=bg)
                colorFrame.grid(row=j, column=labels_column + i, sticky=N + S + E + W)

    def display_variables(self):
        self.longitude.set(self.longitude_data)
        self.latitude.set(self.latitude_data)
        self.gyroX.set(self.gyroX_data)
        self.gyroY.set(self.gyroY_data)
        self.gyroZ.set(self.gyroZ_data)
        self.cardinalDirection.set(self.cardinalDirection_data)
        self.temperature.set(self.temperature_data)
        self.accelX.set(self.accelX_data)
        self.accelY.set(self.accelY_data)
        self.accelZ.set(self.accelZ_data)

    def reset_variables(self):
        # Resets all of the data on screen to zero

        # GPIO.output(self.gui_switch, GPIO.LOW)
        self.longitude_data = 0
        self.latitude_data = 0
        self.gyroX_data = 0
        self.gyroY_data = 0
        self.gyroZ_data = 0
        self.cardinalDirection_data = 0
        self.temperature_data = 0
        self.accelX_data = 0
        self.accelY_data = 0
        self.accelZ_data = 0

        self.display_variables()

