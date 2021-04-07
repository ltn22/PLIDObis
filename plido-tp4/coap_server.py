#!/usr/bin/env python3

# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

"""This is a usage example of aiocoap that demonstrates how to implement a
simple server. See the "Usage Examples" section in the aiocoap documentation
for some more information."""

import datetime
import time
import logging
import binascii
import pprint
import asyncio

import aiocoap.resource as resource
import aiocoap

import cbor2 as cbor
import config_bbt #secret keys 
import beebotte



bbt = beebotte.BBT(config_bbt.API_KEY, config_bbt.SECRET_KEY)

def to_bbt(channel, res_name, msg, factor=1, period=10, epoch=None):
    global bbt

    prev_value = 0
    data_list = []
    if epoch:
        back_time = epoch
    else:
        back_time = time.mktime(datetime.datetime.now().timetuple())
    
    back_time -= len(msg)*period

    for e in msg:
        prev_value += e
        
        back_time += period

        data_list.append({"resource": res_name,
                          "data" : prev_value*factor,
                          "ts": back_time*1000} )

    pprint.pprint (data_list)
    
    bbt.writeBulk(channel, data_list)

class generic_sensor(resource.PathCapable):

    async def render(self, request):
        print ("render", request.opt.uri_path)
        devEUI = request.opt.uri_path[0]
        measurement = request.opt.uri_path[1]

        print (devEUI, measurement)

        ct = request.opt.content_format or \
                aiocoap.numbers.media_types_rev['text/plain']

        if ct == aiocoap.numbers.media_types_rev['text/plain']:
            print ("text:", request.payload)
        elif ct == aiocoap.numbers.media_types_rev['application/cbor']:
            print ("cbor:", cbor.loads(request.payload))
            to_bbt(devEUI, measurement, cbor.loads(request.payload), period=60, factor=0.01)
        else:
            print ("Unknown format")
            return aiocoap.Message(code=aiocoap.UNSUPPORTED_MEDIA_TYPE)
        return aiocoap.Message(code=aiocoap.CHANGED)


    async def needs_blockwise_assembly(self, request):
        return False
        
class temperature(resource.Resource):
    async def render_post(self, request):

        ct = request.opt.content_format or \
                aiocoap.numbers.media_types_rev['text/plain']

        if ct == aiocoap.numbers.media_types_rev['text/plain']:
            print ("text:", request.payload)
        elif ct == aiocoap.numbers.media_types_rev['application/cbor']:
            print ("cbor:", cbor.loads(request.payload))
            to_bbt("capteurs", "temperature", cbor.loads(request.payload), period=60, factor=0.01)
        else:
            print ("Unknown format")
            return aiocoap.Message(code=aiocoap.UNSUPPORTED_MEDIA_TYPE)
        return aiocoap.Message(code=aiocoap.CHANGED)

class pressure(resource.Resource):
    async def render_post(self, request):

        print (">>>>", binascii.hexlify(request.payload))

        ct = request.opt.content_format or \
                aiocoap.numbers.media_types_rev['text/plain']

        if ct == aiocoap.numbers.media_types_rev['text/plain']:
            print ("text:", request.payload)
        elif ct == aiocoap.numbers.media_types_rev['application/cbor']:
            print ("cbor:", cbor.loads(request.payload))
            to_bbt("capteurs", "pressure", cbor.loads(request.payload), period=1, factor=0.01)
        else:
            print ("Unknown format")
            return aiocoap.Message(code=aiocoap.UNSUPPORTED_MEDIA_TYPE)
        return aiocoap.Message(code=aiocoap.CHANGED)

class humidity(resource.Resource):
    async def render_post(self, request):

        ct = request.opt.content_format or \
                aiocoap.numbers.media_types_rev['text/plain']

        if ct == aiocoap.numbers.media_types_rev['text/plain']:
            print ("text:", request.payload)
        elif ct == aiocoap.numbers.media_types_rev['application/cbor']:
            print ("cbor:", cbor.loads(request.payload))
            to_bbt("capteurs", "humidity", cbor.loads(request.payload), period=60, factor=1)

        else:
            print ("Unknown format")
            return aiocoap.Message(code=aiocoap.UNSUPPORTED_MEDIA_TYPE)
        return aiocoap.Message(code=aiocoap.CHANGED)

# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(['temperature'], temperature())
    root.add_resource(['pressure'], pressure())
    root.add_resource(['humidity'], humidity())
    root.add_resource(['proxy'], generic_sensor())
    

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
