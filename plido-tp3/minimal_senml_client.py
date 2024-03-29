from virtual_sensor import virtual_sensor
import time
import socket
import json
import kpn_senml as senml
import pprint
import binascii
import datetime
import time
import pprint

import socket
import binascii
import argparse



parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose",
                    action="store_true",
                    help="show uplink and downlink messages")
parser.add_argument('--http_port',  default=9999,
                    help="set http port for POST requests")
parser.add_argument('--forward_address',  default='127.0.0.1',
                    help="IP address to forward packets")

args = parser.parse_args()
verbose = args.verbose
defPort = int(args.http_port)
if defPort == 9999:
    forward_port = 33033
else: #if a port is specified, the loopback port is also change
    forward_port = defPort+5683
forward_address = args.forward_address


NB_ELEMENT = 5


temperature = virtual_sensor(start=20, variation = 0.1)
pressure    = virtual_sensor(start=1000, variation = 1)
humidity    = virtual_sensor(start=30, variation = 3, min=20, max=80)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    pack = senml.SenmlPack("device1")
    pack.base_time = time.mktime( datetime.datetime.now().timetuple())

    for k in range(NB_ELEMENT):
        t = round(temperature.read_value(), 2)
        h = round(humidity.read_value(), 2)
        p = int(pressure.read_value() *100) # unit is Pa not hPa


        rec = senml.SenmlRecord("temperature",
            unit=senml.SenmlUnits.SENML_UNIT_DEGREES_CELSIUS,
            value=t)
        rec.time = time.mktime(datetime.datetime.now().timetuple())
        pack.add(rec)

        rec = senml.SenmlRecord("humidity",
            unit=senml.SenmlUnits.SENML_UNIT_RELATIVE_HUMIDITY,
            value=h)
        rec.time = time.mktime(datetime.datetime.now().timetuple())
        pack.add(rec)

        rec = senml.SenmlRecord("pressure",
            unit=senml.SenmlUnits.SENML_UNIT_PASCAL,
            value=p)
        rec.time = time.mktime(datetime.datetime.now().timetuple())
        pack.add(rec)

        time.sleep(10)

        pprint.pprint(json.loads(pack.to_json()))
        print ("JSON length: ", len(pack.to_json()), "bytes")
        print ("CBOR length: ", len(pack.to_cbor()), "bytes")

    s.sendto(pack.to_cbor(), ("127.0.0.1", forward_port))
