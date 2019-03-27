from tkinter import *


class Data:
    def __init__(self, place_window, data_name, labels_column, data_column):
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
        environmental_data_label = Label(place_window, text=data_name, font=('times', 15, 'underline'))
        environmental_data_label.grid(row=0, column=labels_column, columnspan=3,
                                      sticky=N + S + E + W)

        # Create and Place Labels for Data
        longitude_label = Label(place_window, text="Longitude:")
        latitude_label = Label(place_window, text="Latitude:")
        gyroX_label = Label(place_window, text="Gyro X:")
        gyroY_label = Label(place_window, text="Gyro Y:")
        gyroZ_label = Label(place_window, text="Gyro Z:")
        cardinalDirection_label = Label(place_window, text="Direction:")
        temperature_label = Label(place_window, text="Temperature (Celsius):")
        accelX_label = Label(place_window, text="Acceleration X:")
        accelY_label = Label(place_window, text="Acceleration Y:")
        accelZ_label = Label(place_window, text="Acceleration Z:")

        longitude_data_label = Label(place_window, text=self.longitude.get())
        latitude_data_label = Label(place_window, text=self.latitude.get())
        gyroX_data_label = Label(place_window, text=self.gyroX.get())
        gyroY_data_label = Label(place_window, text=self.gyroY.get())
        gyroZ_data_label = Label(place_window, text=self.gyroZ.get())
        cardinalDirection_data_label = Label(place_window, text=self.cardinalDirection.get())
        temperature_data_label = Label(place_window, text=self.temperature.get())
        accelX_data_label = Label(place_window, text=self.accelX.get())
        accelY_data_label = Label(place_window, text=self.accelY.get())
        accelZ_data_label = Label(place_window, text=self.accelZ.get())

        longitude_label.grid(row=1, column=labels_column)
        latitude_label.grid(row=2, column=labels_column)
        gyroX_label.grid(row=3, column=labels_column)
        gyroY_label.grid(row=4, column=labels_column)
        gyroZ_label.grid(row=5, column=labels_column)
        cardinalDirection_label.grid(row=6, column=labels_column)
        temperature_label.grid(row=7, column=labels_column)
        accelX_label.grid(row=8, column=labels_column)
        accelY_label.grid(row=9, column=labels_column)
        accelZ_label.grid(row=10, column=labels_column)

        longitude_data_label.grid(row=1, column=data_column)
        latitude_data_label.grid(row=2, column=data_column)
        gyroX_data_label.grid(row=3, column=data_column)
        gyroY_data_label.grid(row=4, column=data_column)
        gyroZ_data_label.grid(row=5, column=data_column)
        cardinalDirection_data_label.grid(row=6, column=data_column)
        temperature_data_label.grid(row=7, column=data_column)
        accelX_data_label.grid(row=8, column=data_column)
        accelY_data_label.grid(row=9, column=data_column)
        accelZ_data_label.grid(row=10, column=data_column)


    def display_variables(self):
        self.longitude.set(self.longitude_data)
        self.latitude.set(self.latitude_data)
        self.gyroX.set(self.gyroX_data)
        self.gyroY.set(self.gyroY_data)
        self.gyroZ.set(self.gyroZ_data)
        self.cardinalDirection.set(self.cardinalDirection_data)
        self.temperature.set(self.temperature_data)
        self.accelX.set(self.accelX_data)
        self.accelY.set(self.accelY)
        self.accelZ.set(self.accelZ)

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
