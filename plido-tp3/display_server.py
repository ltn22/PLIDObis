import socket
import binascii
import cbor2 as cbor
import beebotte
import config_bbt #secret keys
import datetime
import time
import pprint
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

bbt = beebotte.BBT(config_bbt.API_KEY, config_bbt.SECRET_KEY)

def to_bbt(channel, res_name, cbor_msg, factor=1, period=10, epoch=None):
    global bbt

    prev_value = 0
    data_list = []
    if epoch:
        back_time = epoch
    else:
        back_time = time.mktime(datetime.datetime.now().timetuple())

    back_time -= len(cbor_msg)*period

    for e in cbor_msg:
        prev_value += e

        back_time += period

        data_list.append({"resource": res_name,
                          "data" : prev_value*factor,
                          "ts": back_time*1000} )

    pprint.pprint (data_list)

    bbt.writeBulk(channel, data_list)


while True:
    data, addr = s.recvfrom(1500)

    j = cbor.loads(data)
    to_bbt("capteurs", "temperature", j, factor=0.01)
