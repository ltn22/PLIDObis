import time
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    s.sendto ("message", ("192.168.1.47", 33033))
    time.sleep(10)
