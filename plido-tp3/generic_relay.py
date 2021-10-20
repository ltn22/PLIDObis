#!/usr/bin/env python3

import sys
import argparse
from flask import Flask
from flask import request
from flask import Response
import pprint
import json
import binascii

import socket
import select
import time
import base64

import requests

app = Flask(__name__)
app.debug = True

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

defPort = 9999

def forward_data(payload):
    global verbose

    inputs = [sock]
    outputs = []

    if verbose:
        print ("--UP->", binascii.hexlify(payload))
    sock.sendto(payload, ("127.0.0.1", 33033))

    readable, writable, exceptional = select.select(inputs, outputs, inputs, 0.1)

    if readable == []:
        if verbose:
            print ("no DW")
        return None   

    for s in readable:
            replyStr = s.recv(1000)
            if verbose:
                print ("<-DW--", binascii.hexlify(replyStr))
            return replyStr

    return None


@app.route('/sigfox', methods=['POST'])
def get_from_sigfox():

    fromGW = request.get_json(force=True)
    print ("SIGFOX POST RECEIVED")
    pprint.pprint(fromGW)

    downlink = None
    if "data" in fromGW:
        payload = binascii.unhexlify(fromGW["data"])
        downlink = forward_data(payload)

    resp = Response(status=200)
    print (resp)
    return resp                                    

@app.route('/TTN', methods=['POST']) # API V2 obsolete
def get_from_TTN():
    fromGW = request.get_json(force=True)
    pprint.pprint(fromGW)

    downlink = None
    if "payload_raw" in fromGW:
        payload = base64.b64decode(fromGW["payload_raw"])
        downlink = forward_data(payload)

    if downlink != None:
        downlink_msg = {
            "dev_id": fromGW["dev_id"],    # The device ID
            "port":   fromGW["port"],      # LoRaWAN FPort
            "confirmed": False,            # Whether the downlink should be confirmed by the device
            "payload_raw": base64.b64encode(downlink).decode()     # Base64 encoded payload: [0x01, 0x02, 0x03, 0x04]
        }
        print (downlink_msg)
        x = requests.post(fromGW["downlink_url"], data = json.dumps(downlink_msg))

        print(x) 

    resp = Response(status=200)
    print (resp)
    return resp 


    #   "identifiers": [
    # {
    #   "device_ids": {
    #     "device_id": "plido-lopy",
    #     "application_ids": {
    #       "application_id": "plido-measures"
    #     }
    #   }
    # },

@app.route('/ttn', methods=['POST']) # API V3 current
def get_from_ttn():
    fromGW = request.get_json(force=True)
    pprint.pprint(fromGW)

    downlink = None
    if "uplink_message" in fromGW:
        payload = base64.b64decode(fromGW["uplink_message"]["frm_payload"])
        downlink = forward_data(payload)

    downlink = b"010203" # To Be remove just for tests
    if downlink != None:
        downlink_msg = {
            "port":   fromGW["uplink_message"]["f_port"],      # LoRaWAN FPort
            "confirmed": False,            # Whether the downlink should be confirmed by the device
            "payload_raw": base64.b64encode(downlink).decode()     # Base64 encoded payload: [0x01, 0x02, 0x03, 0x04]
        }
        downlink_url = "https://eu1.cloud.thethings.network/api/v3/as/applications/" + \
                        fromGW["end_device_ids"]["application_ids"]["application_id"] + \
                        "/devices/" + \
                        fromGW["end_device_ids"]["device_id"] + \
                        "/down/push'

        print(downlink_url)
        print (downlink_msg)
        x = requests.post(downlink_url, data = json.dumps(downlink_msg))

        print(x) 

    resp = Response(status=200)
    print (resp)
    return resp 

@app.route('/lns', methods=['POST']) 
def get_from_acklio():

    fromGW = request.get_json(force=True)
    print (fromGW)
    downlink = None
    if "data" in fromGW:
        payload = base64.b64decode(fromGW["data"])
        downlink = forward_data(payload)

    if downlink == None:
        resp = Response(status=200)
    else:
        answer = {
            "fPort" : fromGW["fPort"],
            "devEUI": fromGW["devEUI"],
            "data"  : base64.b64encode(downlink).decode('utf-8')
        }
        resp = Response(response=json.dumps(answer), 
                        status=200, 
                        mimetype="application/json")
    return resp

@app.route('/chirpstack', methods=['POST'])
def get_from_chirpstack():
    import chirpstack_secrets as secret

    fromGW = request.get_json(force=True)
    print (request.environ.get('REMOTE_PORT'))
    pprint.pprint (fromGW)

    downlink = None
    if "data" in fromGW:
        payload = base64.b64decode(fromGW["data"])
        downlink = forward_data(payload)

        print (fromGW["fPort"])
    if downlink != None:
        answer = {
            "deviceQueueItem": {
		            "data": base64.b64encode(downlink).decode('utf-8'),
                    "fPort": fromGW["fPort"],
            }
        }
        pprint.pprint (answer)
        device = binascii.hexlify(base64.b64decode(fromGW["devEUI"])).decode()
        downlink_url = secret.server+'/api/devices/'+device+'/queue'
        print (downlink_url)
        headers = {
            "content-type": "application/json",
            "grpc-metadata-authorization" : "Bearer "+ secret.key
        }
        print (headers)
        x = requests.post(downlink_url, data = json.dumps(answer), headers=headers)

        print(x) 


    resp = Response(status=200)         
    return resp


parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", 
                    action="store_true",
                    help="show uplink and downlink messages")

args = parser.parse_args()
verbose = args.verbose


app.run(host="0.0.0.0", port=defPort)



