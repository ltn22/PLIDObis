from virtual_sensor import virtual_sensor 
import time
import socket
import json
import kpn_senml as senml
import pprint
import binascii

temperature = virtual_sensor(start=20, variation = 0.1)
pressure    = virtual_sensor(start=1000, variation = 1) 
humidity    = virtual_sensor(start=30, variation = 3, min=20, max=80) 
 
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sens = senml.SenmlPack("device1") 

t = temperature.read_value()
p = pressure.read_value()
h = humidity.read_value()

rec = senml.SenmlRecord("temperature", 
    unit=senml.SenmlUnits.SENML_UNIT_DEGREES_CELSIUS, 
    value=t)         
sens.add(rec)



print(len(sens.to_json()), sens.to_json())
print(len(sens.to_cbor()), binascii.hexlify(sens.to_cbor()))