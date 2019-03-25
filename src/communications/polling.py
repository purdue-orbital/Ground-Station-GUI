from digi.xbee.devices import XBeeDevice

# TODO: Replace with the serial port where your local module is connected to. 
PORT = "/dev/ttyS6"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600


def main():
    print(" +-------------------------------------------------+")
    print(" | XBee Python Library Receive Data Polling Sample |")
    print(" +-------------------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        device.flush_queues()

        print("Waiting for data...\n")

        while True:
            xbee_message = device.read_data()
            if xbee_message is not None:
                print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                         xbee_message.data.decode()))

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()
