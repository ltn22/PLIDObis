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
import random

from pymongo import MongoClient


class sensor_emulated:

    def __init__(self, mac, name, t_range, p_range, h_range):
        self.t_min, self.t_max = t_range
        self.p_min, self.p_max = p_range
        self.h_min, self.h_max = h_range


        self.mt = 0.0
        self.mp = 0.0
        self.mh = 0.0
        self.nb_elm = 0

        my_sensor = {
            "@context": "http://user.ackl.io/schema/Sensor",
            "ThingID" : mac,
            "Name" : name+mac,
            "Manufacturer" : "pycom LOPY4",
            "Link" : "LoRaWAN Acklio",
            "Location" : name,
            "Address" : mac
            }

        # look if the device identified by name exists in the DB

        found_item = collection.find_one ({"Location" : name })
        if found_item is None:
            print (name, "do not exist in the database")
            self.sensor_id = collection.insert_one(my_sensor).inserted_id

            print ("new id is ", self.sensor_id)
        else:
            self.sensor_id = found_item["_id"]
            print (name, "already in database", self.sensor_id)


    def store_measurement(self):
        t = random.uniform (self.t_min, self.t_max)
        p = random.uniform (self.p_min, self.p_max)
        h = random.uniform (self.h_min, self.h_max)

        self.mt += t
        self.mp += p
        self.mh += h
        self.nb_elm += 1

        my_measure = {
            "@context" : "http://user.ackl.io/schema/BME280",
            "Temperature" : t,
            "Pressure"    : p/10, 
            "Humidity"  : h,
            "SensorCharacteristics" : self.sensor_id,
            "Date" : datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
            }
        
        id = collection.insert_one(my_measure)
 
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
    for e in [("0123456789abcde", "bedroom", (15, 20), (1000, 1200), (30, 50)), 
              ("badc0ffee0ddf00d", "kitchen", (20, 25), (1000, 1200), (30, 60)),
              ("ca11ab1eca55e77e", "office", (18, 25), (1000, 1200), (40, 70)),
              ("5ca1ab1eb16b00b5", "bathroom", (18, 27), (1000, 1200), (30, 90))]:
        sensor = sensor_emulated (*e)
        sensor_list.append(sensor)
    
    while True:
        for s in sensor_list:
            s.store_measurement()

        print (".", end="")
        time.sleep(60)

if __name__ == "__main__":
    main()
