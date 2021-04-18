#!/usr/bin/env python3

# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

"""This is a usage example of aiocoap that demonstrates how to implement a
simple server. See the "Usage Examples" section in the aiocoap documentation
for some more information."""

""" This program receives POST from devices, direclty from Wi-Fi and through
generic_coap_relay.py for LPWAN devices.

It takes a CBOR coded Time Series and trandform it on a JSON structure for
beebotte to display graphs. beebotte credentials are stored un config_bbt.py 
file.
"""

import datetime
import time
import logging
import binascii
import pprint
from virtual_sensor import virtual_sensor

from pymongo import MongoClient


class sensor_emulated:

    def __init__(self, mac, name, t, p, h):
        self.temperature = virtual_sensor(start=t, variation = 0.1)
        self.pressure    = virtual_sensor(start=p, variation = 1) 
        self.humidity    = virtual_sensor(start=h, variation = 3, min=20, max=80) 

        my_sensor = {
            "@context": "http://user.ackl.io/schema/Sensor",
            "ThingID" : mac,
            "Name" : "Room 23",
            "Manufacturer" : "pycom LOPY4",
            "Link" : "LoRaWAN Acklio",
            "Location" : name,
            "Address" : mac
            }

        # look if the device identified by name exists in the DB

        found_item = collection.find_one ({"Name" : name })
        if found_item == None:
            print (name, "do not exist in the database")
            self.sensor_id = collection.insert_one(my_sensor).inserted_id

            print ("new id is ", self.sensor_id)
        else:
            self.sensor_id = found_item["_id"]
            print (name, "already in database", self.sensor_id)


    def store_measurement(self):
        t = self.temperature.read_value()
        p = self.pressure.read_value()
        h = self.humidity.read_value()

        print (t, p, h)
        my_measure = {
            "@context" : "http://user.ackl.io/schema/BME280",
            "Temperature" : t,
            "Pression"    : p/10, 
            "Humiditity"  : h,
            "SensorCharacteristics" : self.sensor_id,
            "Date" : datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
            }
        
        id = collection.insert_one(my_measure)
        print (my_measure)
 
# logging setup

#logging.basicConfig(level=logging.INFO)
#logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    global collection 
    global sensor_id

    client = MongoClient()
    db = client ["meteo-data"]
    collection = db["measure"] # a new collection for structured data

    # look for the object representing your device, if not found, create it

    #
    # MUST be changed with your device characteristics
    #

    sensor_list = []
    for e in [("0123456789abcde", "bedroom", 18, 10000, 30), 
              ("badc0ffee0ddf00d", "kitchen", 25, 10000, 50),
              ("ca11ab1eca55e77e", "office", 20, 10000, 40),
              ("5ca1ab1eb16b00b5", "bathroom", 27, 10000, 70)]:
        print (e)
        sensor = sensor_emulated (*e)
        sensor_list.append(sensor)
    
    print (sensor_list)

    while True:
        for s in sensor_list:
            s.store_measurement()

        print (".", end="")
        time.sleep(60)



 
if __name__ == "__main__":
    main()
