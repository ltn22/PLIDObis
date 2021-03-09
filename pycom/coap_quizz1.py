import CoAP
import socket
import time

SERVER = "192.168.1.26" # change to your server's IP address
PORT   = 5683
destination = (SERVER, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

coap = CoAP.Message()
coap.new_header(code=CoAP.POST)
coap.add_option (CoAP.Uri_path, "temp")
coap.add_option (CoAP.Uri_path, "sens1")
coap.add_option (CoAP.Uri_query, "max")
coap.add_payload("23.5")
coap.dump(hexa=True)

answer = CoAP.send_ack(s, destination, coap)
answer.dump()
