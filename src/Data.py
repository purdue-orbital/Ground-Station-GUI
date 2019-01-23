from tkinter import *


class Data:
    def __init__(self, place_window, labels_column, data_column):
        # Environment Data
        self.temperature_data = 11
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

        # Create and Place Section Header
        environmental_data_label = Label(place_window, text="Environmental Data", font=('times', 15, 'underline'))
        environmental_data_label.grid(row=0, column=labels_column, columnspan=data_column,
                                      sticky=N + S + E + W)

        # Create and Place Labels for Data
        temperature_label = Label(place_window, text="Temperature (Celsius):")
        pressure_label = Label(place_window, text="Pressure (kPa):")
        humidity_label = Label(place_window, text="Humidity (Percent):")

        temperature_label.grid(row=1, column=labels_column)
        pressure_label.grid(row=2, column=labels_column)
        humidity_label.grid(row=3, column=labels_column)

        # Place Data Across from Corresponding Label
        temperature_data = Label(place_window, textvariable=self.temperature)
        pressure_data = Label(place_window, textvariable=self.pressure)
        humidity_data = Label(place_window, textvariable=self.humidity)

        temperature_data.grid(row=1, column=data_column)
        pressure_data.grid(row=2, column=data_column)
        humidity_data.grid(row=3, column=data_column)

        space = 5

        # Create and Place Section Header
        system_data_label = Label(place_window, text="System Data", font=('times', 15, 'underline'))
        system_data_label.grid(row=space, column=labels_column, columnspan=data_column, sticky=N + S + E + W)

        # Create and Place Labels for Data
        altitude_label = Label(place_window, text="Altitude (km):")
        direction_label = Label(place_window, text="Direction(rad):")
        acceleration_label = Label(place_window, text="Acceleration (m/s/s):")
        velocity_label = Label(place_window, text="Velocity (m/s):")
        angle_label = Label(place_window, text="Angle (rad):")

        altitude_label.grid(row=space + 1, column=labels_column)
        direction_label.grid(row=space + 2, column=labels_column)
        acceleration_label.grid(row=space + 3, column=labels_column)
        velocity_label.grid(row=space + 4, column=labels_column)
        angle_label.grid(row=space + 5, column=labels_column)

        # Place Data Across from Corresponding Label
        altitude_data = Label(place_window, textvariable=self.altitude)
        direction_data = Label(place_window, textvariable=self.direction)
        acceleration_data = Label(place_window, textvariable=self.acceleration)
        velocity_data = Label(place_window, textvariable=self.velocity)
        angle_data = Label(place_window, textvariable=self.user_angle)

        altitude_data.grid(row=space + 1, column=data_column)
        direction_data.grid(row=space + 2, column=data_column)
        acceleration_data.grid(row=space + 3, column=data_column)
        velocity_data.grid(row=space + 4, column=data_column)
        angle_data.grid(row=space + 5, column=data_column)

        self.display_variables()

    def display_variables(self):
        self.temperature.set(self.temperature_data)
        self.pressure.set(self.pressure_data)
        self.humidity.set(self.humidity_data)

        self.altitude.set(self.altitude_data)
        self.direction.set(self.direction_data)
        self.acceleration.set(self.acceleration_data)
        self.velocity.set(self.velocity_data)
        self.user_angle.set(self.user_angle_data)

    def reset_variables(self):
        # Resets all of the data on screen to zero

        # GPIO.output(self.gui_switch, GPIO.LOW)
        self.temperature_data = 0.0
        self.pressure_data = 0.0
        self.humidity_data = 0.0

        self.altitude_data = 0.0
        self.direction_data = 0.0
        self.acceleration_data = 0.0
        self.velocity_data = 0.0
        self.user_angle_data = 0.0

        self.display_variables()
