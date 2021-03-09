import CoAP
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


coap = CoAP.Message()
coap.new_header()
#coap.add_option_path("time")
coap.dump()

s.settimeout(10)
s.sendto (coap.to_byte(), ("10.35.131.225", 5683))
#s.sendto (coap.to_byte(), ("79.137.84.149", 5683))
resp,addr = s.recvfrom(2000)
answer = CoAP.Message(resp)
answer.dump()
