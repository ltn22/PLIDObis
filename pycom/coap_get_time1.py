import CoAP
import socket

SERVER = "192.168.11.109" # change to your server's IP address
PORT   = 5683

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

coap = CoAP.Message()
coap.new_header(code=CoAP.GET)
coap.add_option (CoAP.Uri_path, "time")
coap.dump(hexa=True)

s.sendto (coap.to_byte(), (SERVER, PORT))

s.settimeout(10)
resp,addr = s.recvfrom(2000)
answer = CoAP.Message(resp)
answer.dump(hexa=True)
