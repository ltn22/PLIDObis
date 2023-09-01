import socket
import binascii
import cbor2 as cbor

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


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((forward_address, forward_port))

samples =0
t_m = 0.0
p_m = 0.0
h_m = 0.0
j_max = 0

while True:
    data, addr = s.recvfrom(1500)
    print (data, "=>", binascii.hexlify(data))

    j = cbor.loads(data)
    print (j)

    samples += 1
    t_m += j[0]
    p_m += j[1]
    h_m += j[2]
    if len(data) > j_max: j_max = len(data)
    print ("{:7.2f} {:10.2f} {:7.2f} | {:}".format(t_m/samples, p_m/samples, h_m/samples, j_max))
