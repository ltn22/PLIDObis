from network import WLAN
import time
import socket
import machine
from machine import RTC
import pycom
import binascii
import json

from wifi_conf import known_nets

print('\nStarting LoRaWAN concentrator')

# Disable Hearbeat
pycom.heartbeat(False)

def machine_cb (arg):
    evt = machine.events()
    if (evt & machine.PYGATE_START_EVT):
        # Green
        pycom.rgbled(0x103300)
    elif (evt & machine.PYGATE_ERROR_EVT):
        # Red
        pycom.rgbled(0x331000)
    elif (evt & machine.PYGATE_STOP_EVT):
        # RGB off
        pycom.rgbled(0x000000)

# register callback function
machine.callback(trigger = (machine.PYGATE_START_EVT | machine.PYGATE_STOP_EVT | machine.PYGATE_ERROR_EVT), handler=machine_cb)

from network import WLAN
wl = WLAN()
wl.mode(WLAN.STA) # Try to connect to a wifi given is wifi_conf.py

print("Scanning for known wifi nets")
available_nets = wl.scan()
print (available_nets)
nets = frozenset([e.ssid for e in available_nets])

known_nets_names = frozenset([key for key in known_nets])
net_to_use = list(nets & known_nets_names)
print ("net to use", net_to_use)
try:
    net_to_use = net_to_use[0]
    net_properties = known_nets[net_to_use]
    pwd = net_properties['pwd']
    sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
    if 'wlan_config' in net_properties:
        wl.ifconfig(config=net_properties['wlan_config'])
    wl.connect(net_to_use, (sec, pwd), timeout=10000)
    while not wl.isconnected():
        machine.idle() # save power while waiting
    print("Connected to "+net_to_use+" with IP address: " + wl.ifconfig()[0])

except Exception as e:
    ssid = "PLIDO_"+str(hexlify(wl.mac()[0][4:]))[2:6]
    wl = WLAN()
    wl.init(mode=WLAN.AP,  ssid=ssid, auth=wl.auth(), antenna=WLAN.INT_ANT)
    print("Failed to connect to any known network, going into AP mode")
    print("To connect look for '{}' access point, key = '{}'".format(ssid, wl.auth()[1] ))
    print (wl.mode())


print('Syncing RTC via ntp...', end='')
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

while not rtc.synced():
    print('.', end='')
    time.sleep(.5)
print(" OK\n")


rgw_id = binascii.hexlify(machine.unique_id())
rgw_id += b'0000' # Id is on 6 bytes, need 8
print ("Your Gateway ID", rgw_id.decode())


# Read the GW config file from Filesystem
with  open('/flash/config.json','r') as fp:
    buf = fp.read()

buf_json = json.loads(buf)
buf_json["gateway_conf"]["gateway_ID"] = rgw_id.decode() # convert in ASCII
buf = json.dumps(buf_json)

time.sleep(10)

# Start the Pygate
machine.pygate_init(buf)
# disable degub messages
# machine.pygate_debug_level(1)
