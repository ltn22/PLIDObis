from network import WLAN
#from network import ETH
import time
import socket
import machine
from machine import RTC
import pycom

print('\nStarting LoRaWAN concentrator')
# Disable Hearbeat
pycom.heartbeat(False)
#192.168.4.1
# 7e 47 40 00 63 c7 cd b6
# Define callback function for Pygate events
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


print('Connecting to WiFi...',  end='')

# Connect to a Wifi Network
wlan = WLAN(mode=WLAN.STA)
wlan.connect(ssid='lora', auth=(WLAN.WPA2, "Marinito"))
#wlan.connect(ssid='chirppygate', auth=(WLAN.WPA2, "marino92"))

while not wlan.isconnected():
    print('.', end='')
    time.sleep(1)
print(" OK")

#eth = ETH()

#eth.init()
#print('Connecting to Ethernet...',  end='')
#while not eth.isconnected():
#    print('.', end='')
#    time.sleep(1)
#print(" OK")

#print(eth.ifconfig())
#print(socket.getaddrinfo("pycom.io", 80))

# Sync time via NTP server for GW timestamps on Events
print('Syncing RTC via ntp...', end='')
rtc = RTC()
rtc.ntp_sync(server="pool.ntp.org")

while not rtc.synced():
    print('.', end='')
    time.sleep(.5)
print(" OK\n")

# Read the GW config file from Filesystem
fp = open('/flash/config.json','r')
buf = fp.read()

# Start the Pygate
machine.pygate_init(buf)
# disable degub messages
# machine.pygate_debug_level(1)
