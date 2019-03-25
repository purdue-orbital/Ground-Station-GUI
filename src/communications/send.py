#!/usr/bin/env python3

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
from digi.xbee.util import utils

import logging



local_xbee = XBeeDevice("/dev/ttyS6", 9600)

local_xbee.open()

addr = local_xbee.get_64bit_addr()

print(addr)

#remote_xbee = RemoteXBeeDevice(local_xbee, XBee64BitAddress.from_hex_string("0013A20040F6E10C"))
remote_xbee = RemoteXBeeDevice(local_xbee, XBee64BitAddress.from_hex_string("0013A2004148887C"))


local_xbee.send_data(remote_xbee, "Hello World!")


local_xbee.close()


#dev_logger = logging.getLogger("local_xbee")

#handler = logging.StreamHandler()

#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#handler.setFormatter(formatter)

#dev_logger.addHandler(handler)

#dev_logger = utils.enable_logger("local_xbee", logging.INFO)

#dev_logger.getMessage()



