from virtual_sensor import virtual_sensor
import time
import socket

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



temperature = virtual_sensor(start=20, variation = 0.1)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    t = temperature.read_value()

    s.sendto (str(t).encode(), ("127.0.0.1", forward_port))
    time.sleep(10)
