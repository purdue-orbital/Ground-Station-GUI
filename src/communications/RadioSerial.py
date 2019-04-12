import serial
import traceback
from xbee import XBee

ser = serial.Serial('/dev/ttyAMA0', 9600)

# xbee = XBee(ser)

while True:

    try:
        # response = xbee.wait_read_frame()
        response = ser.readline().strip()
        print(response)

    except Exception as e:
        traceback.print_exc()
        print(e)
        break

ser.close()


        
