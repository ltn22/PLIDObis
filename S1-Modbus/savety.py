#!/usr/bin/env python
"""
Pymodbus Synchronous Client Examples
--------------------------------------------------------------------------

The following is an example of how to use the synchronous modbus client
implementation from pymodbus.

It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::

    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result
"""
# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# --------------------------------------------------------------------------- #
# configure the client logging
# --------------------------------------------------------------------------- #
import logging

import time
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

UNIT = 0x1


def run_sync_client():
    from pymodbus.transaction import ModbusRtuFramer

    client = ModbusClient('0.0.0.0', port=5020)

    client.connect()

    while True:
        rr = client.read_input_registers(0xff, 1, unit=28)
        level = rr.registers[0]

        print(level)

        if level < 8000:
            print("opening water")
            client.write_register(0x200, 200, unit=48)
        elif level < 9600:
            client.write_register(0x200, 10, unit=48)
        else:
            client.write_register(0x200, 0, unit=48)

            

        time.sleep (1)
        

    # ----------------------------------------------------------------------- #
    # close the client
    # ----------------------------------------------------------------------- #
    client.close()


if __name__ == "__main__":
    run_sync_client()
