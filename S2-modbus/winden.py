#!/usr/bin/env python
"""
Pymodbus Server With Updating Thread
--------------------------------------------------------------------------

This is an example of having a background thread updating the
context while the server is operating. This can also be done with
a python thread::

    from threading import Thread

    thread = Thread(target=updating_writer, args=(context,))
    thread.start()
"""
# --------------------------------------------------------------------------- #
# import the modbus libraries we need
# --------------------------------------------------------------------------- #
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer

from random import random
from termcolor import colored, cprint
import curses

import datetime
import sys
import os


# --------------------------------------------------------------------------- #
# import the twisted libraries we need
# --------------------------------------------------------------------------- #
from twisted.internet.task import LoopingCall

# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging
logging.basicConfig()
log = logging.getLogger()
#log.setLevel(logging.DEBUG)

# --------------------------------------------------------------------------- #
# define your callback process
# --------------------------------------------------------------------------- #

level = 7000
variation = -5

first = True
variation = -5
ref_time = datetime.datetime.now()
counting = False

class Color:
    # Foreground
    F_Default = "\x1b[39m"
    F_Black = "\x1b[30m"
    F_Red = "\x1b[31m"
    F_Green = "\x1b[32m"
    F_Yellow = "\x1b[33m"
    F_Blue = "\x1b[34m"
    F_Magenta = "\x1b[35m"
    F_Cyan = "\x1b[36m"
    F_LightGray = "\x1b[37m"
    F_DarkGray = "\x1b[90m"
    F_LightRed = "\x1b[91m"
    F_LightGreen = "\x1b[92m"
    F_LightYellow = "\x1b[93m"
    F_LightBlue = "\x1b[94m"
    F_LightMagenta = "\x1b[95m"
    F_LightCyan = "\x1b[96m"
    F_White = "\x1b[97m"
    # Background
    B_Default = "\x1b[49m"
    B_Black = "\x1b[40m"
    B_Red = "\x1b[41m"
    B_Green = "\x1b[42m"
    B_Yellow = "\x1b[43m"
    B_Blue = "\x1b[44m"
    B_Magenta = "\x1b[45m"
    B_Cyan = "\x1b[46m"
    B_LightGray = "\x1b[47m"
    B_DarkGray = "\x1b[100m"
    B_LightRed = "\x1b[101m"
    B_LightGreen = "\x1b[102m"
    B_LightYellow = "\x1b[103m"
    B_LightBlue = "\x1b[104m"
    B_LightMagenta = "\x1b[105m"
    B_LightCyan = "\x1b[106m"
    B_White = "\x1b[107m"
    

def youreDead():
    str = """
          _ ._  _ , _ ._
        (_ ' ( `  )_  .__)
      ( (  (    )   `)  ) _)
     (__ (_   (_ . _) _) ,__)
         `~~`\ ' . /`~~`
              ;   ;
              /   \\
_____________/_ __ \_____________
           YOU ARE DEAD
"""
    print (Color.F_Red)
    print (str)
    print (Color.F_White)
    os._exit(1)

def saveTheWorld():
    str = """
.. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
.. . . . . . . .#######. . . . . . . . . . . . . . . . . .
.. . . . . . .#. .#### . . . ####. . .###############. . .
.. . ########. ##. ##. . . ######################### . . .
.. . . ##########. . . . ######################. . . . . .
.. . . .######## . . . .   ################### . . . . . .
.. . . . ### .   . . . .#####. ##############. # . . . . .
.. . . . . ##### . . . .#######. ##########. . . . . . . .
.. . . . . .###### . . . .#### . . . . .## . . . . . . . .
.. . . . . . ##### . . . .#### # . . . . . ##### . . . . .
.. . . . . . ### . . . . . ##. . . . . . . . ### .#. . . .
.. . . . . . ##. . . . . . . . . . . . . . . . . . . . . .
.. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
                  YOU SAVE THE WORLD
"""
    print (Color.F_Green)
    print (str)
    print (Color.F_White)
    os._exit(1)
    

def updating_writer(a):
    global first
    global variation
    global ref_time
    global counting
    
    """ A worker process that runs every so often and
    updates live values of the context. It should be noted
    that there is a race condition for the update.

    :param arguments: The input arguments to the call
    """

    p = 0.9
    min = -10
    max = +30
    
    log.debug("updating the context")
    context = a[0]
    register = 4
    slave_id = 28
    address = 0xff
    values = context[slave_id].getValues(register, address, count=1)

    retroaction = context[48].getValues(6, 0x200, count=1)

    variation += min + (max - min) * pow(random(), p)     
    if variation > 0 : variation = 0    
    
    if first:
        values[0] = 7000
        first = False
    else:
        values[0] = int (values[0] +variation + retroaction[0])

    context[slave_id].setValues(register, address, values)

    
    if values[0] < 2000:
        txtcolor = Color.F_Red
    elif values[0] < 4000:
        txtcolor = Color.F_Magenta
    elif values[0] < 6000:
        txtcolor = Color.F_Yellow
    elif values[0] < 9500:
        txtcolor = Color.F_White
    else:
        txtcolor = Color.F_Green

    if retroaction[0] > 0:
        watercolor= Color.F_Blue
    else:
        watercolor = Color.F_White
    
    print("\033[{};{}H{}".format(2, 1, txtcolor), end="") 
    print ("Water Level {0:.2f}% {1} Added water {2:2} L/s".format(values[0]/100.0, watercolor, retroaction[0]), end='')
    print (" "*5, end='')
    

    if values[0] < 1000:
        youreDead()
        sys.exit(0)
    elif values[0] < 9500:
        counting = False
        print("\033[{};{}H".format(3, 1), end="")
        print (" "*79)
    elif values[0] < 10000:
        if counting == False:
            ref_time = datetime.datetime.now()
            counting = True
        difference =  datetime.datetime.now() - ref_time
        print("\033[{};{}H".format(3, 2), end="")
        
        print (Color.F_White," Stable duration ", difference, end='')
        if difference.total_seconds() > 60:
            saveTheWorld()
            sys.exit(0)
    else:
        youreDead()
        sys.exit(0)

    print ("")

            
def run_updating_server():
    # ----------------------------------------------------------------------- # 
    # initialize your data store
    # ----------------------------------------------------------------------- # 
    
    store1 = ModbusSlaveContext(
        di=ModbusSparseDataBlock({0x10: 12}),
        cp=ModbusSparseDataBlock({0x10: 13}),
        hr=ModbusSparseDataBlock({0x10: 14}),
        ir=ModbusSparseDataBlock({0x100: 7000}))
    
    store2 = ModbusSlaveContext(
        di=ModbusSparseDataBlock({0x10: 12}),
        cp=ModbusSparseDataBlock({0x10: 13}),
        hr=ModbusSparseDataBlock({0x10: 14}),
        ir=ModbusSparseDataBlock({0x100: 7000}))
    
    slaves = {
        28: ModbusSlaveContext(slaves=store1),
        48: ModbusSlaveContext(slaves=store2)
        }
    context = ModbusServerContext(slaves=slaves, single=False)
    
    # ----------------------------------------------------------------------- # 
    # initialize the server information
    # ----------------------------------------------------------------------- # 
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'pymodbus Server'
    identity.ModelName = 'pymodbus Server'
    identity.MajorMinorRevision = '2.2.0'
    
    # ----------------------------------------------------------------------- # 
    # run the server you want
    # ----------------------------------------------------------------------- # 
    time = 0.1
    loop = LoopingCall(f=updating_writer, a=(context,))
    loop.start(time, now=False) # initially delay by time
    StartTcpServer(context, identity=identity, address=("0.0.0.0", 5020))


if __name__ == "__main__":

    os.system("clear")
    print("")
    
    run_updating_server()
