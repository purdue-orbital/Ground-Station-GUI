import serial

ser = serial.Serial('/dev/ttyS10', 9600)
while True:
    data = ser.readline()
    print(data)
