#!/usr/bin/env python3

import sys, getopt
from flask import Flask
from flask import request
from flask import Response
import pprint
import json
import binascii
import base64

import socket
import select
import time

app = Flask(__name__)
app.debug = True

defPort = 9999

@app.route('/TTN', methods=['POST'])
def get_from_LNS():

    fromGW = request.get_json(force=True)
    print ("HTTP POST RECEIVED")
    pprint.pprint(fromGW)

    if "payload_raw" in fromGW:
        payload = base64.b64decode(fromGW["payload_raw"])
        print (binascii.hexlify(payload))

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



