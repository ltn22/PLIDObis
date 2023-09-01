import socket
import binascii



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
    forward_port = args.forward_port
else: #if a port is specified, the loopback port is also change
    forward_port = defPort+5683
forward_address = args.forward_address


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((forward_address, forward_port))

while True:
    data, addr = s.recvfrom(1500)
    print (data)
    s.sendto("Pleased to meet you!".encode(), addr)
