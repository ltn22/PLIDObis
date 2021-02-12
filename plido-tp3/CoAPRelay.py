#!/usr/bin/env python3

import sys, getopt
from flask import Flask
from flask import request
from flask import Response
import pprint
import json
import binascii

import socket
import select

app = Flask(__name__)
app.debug = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
defPort = 9999

@app.route('/sigfox', methods=['POST'])
def get_from_LNS():

    fromGW = request.get_json(force=True)
    print ("HTTP POST RECEIVED")
    pprint.pprint(fromGW)
    if "data" in fromGW:
        payload = binascii.unhexlify(fromGW["data"])

        sock.sendto(payload, ("127.0.0.1", 33033))

    resp = Response(status=200)
    print (resp)
    return resp                                    

try:
    opts, args = getopt.getopt(sys.argv[1:],"hp:",["port="])
except getopt.GetoptError:
    print ("{0} -p <port> -h".format(sys.argv[0]))
    sys.exit(2)
    
for opt, arg in opts:
    if opt == '-h':
        print ("{0} -p <port> -h".format(sys.argv[0]))
        sys.exit()
    elif opt in ("-p", "--port"):
        defPort = int(arg)


app.run(host="0.0.0.0", port=defPort)



