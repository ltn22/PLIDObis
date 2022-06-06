import struct
import binascii
import sys

upython = (sys.implementation.name == "micropython")

if upython:
    pass
###

type_name = ["CON", "NON", "ACK", "RST"]
CON = 0
NON = 1
ACK = 2
RST = 3

code_name = ["EMPTY", "GET", "POST", "PUT", "DELETE"]

EMPTY = 0
GET = 1
POST = 2
PUT = 3
DELETE = 4

####

Uri_path = 11
Uri_query = 15
Content_format = 12
No_Response = 258

option_name = {
    Uri_path       : ["Uri-path", str],
    Uri_query      : ["Uri-query", str],
    Content_format : ["Content-format", int],
    No_Response    : ["No-Response", int]
}

Content_format_text = 0
Content_format_JSON = 50
Content_format_CBOR = 60

###

default_mid = 1


class Message:

    """
    class CoAP for client and server
    """

    def __init__( self, buf = b'' ):
        self.buffer = buf
        self.option = 0

    def new_header ( self, type = CON, code = EMPTY, token = None, mid = None, midSize = 16 ):

        global default_mid

        if mid is None:
            mid = default_mid
            default_mid = ( default_mid + 1 ) % ( 1 << midSize )
            if ( default_mid == 0 ): default_mid = 1  # mid = 0 may be ack with a random number

        self.buffer = bytearray()

        tkl = 0
        if token:
            for i in range(0,8):
                if token & (0xFF << 8*i) != 0x00:
                    tkl = i+1

        assert (tkl < 8)

        # First 32 bit word
        byte = ( ( 0x01 ) << 6 ) | ( type << 4 ) | tkl  # need to compute token length

        self.buffer = struct.pack ( '!BBH', byte, code, mid)

        for i in range(0, tkl):
            v = (token & (0xFF << 8*(tkl-i-1)))
            v >>=(8*(tkl-i-1))

            self.buffer += struct.pack('B', v)
# In some cases the Message ID size must be limited to a smaller number of bits
# To allow rule selection, especially with MSB the size must be controlled


    def __add_option_TL ( self, T, L ):
        delta = T - self.option
        self.option = T


        if ( delta < 13 ) and ( L < 13 ) is True:
            self.buffer += struct.pack( 'B', ( delta << 4 ) | L )
        else:
            if delta < 13:
                c_delta = delta
            elif delta > 12 and delta < 269:
                c_delta = 13
                delta -= 13
            else:
                print("not done")

            if L < 13:
                c_L = L
            elif L < 269:
                c_L = 13
                L -= 13
            else:
                print ("not done")

            self.buffer += struct.pack( 'B', ( c_delta << 4 ) | c_L )
            if c_delta == 13:
                self.buffer += struct.pack( 'B', delta )
            if c_L == 13:
                self.buffer += struct.pack( 'B', L )



    def add_option (self, opt, value=None):
        if opt < self.option:
            raise ValueError("Option number {} is not increasing".format(value))

        if value is None:
            self.__add_option_TL (opt, 0)
        elif type(value) == str:
            self.__add_option_TL (opt, len(value))
            if upython:
                self.buffer += bytearray(value)
            else:
                self.buffer += bytearray(value, encoding="utf-8")
        elif type(value) == int:
            opt_l = 0
            ba = b''
            while value != 0:
                opt_l += 1
                ba = struct.pack('B', value & 0xFF) + ba
                value >>= 8
            self.__add_option_TL(opt, opt_l)
            self.buffer += ba
        else:
            raise ValueError ("add_option: unknow type {}".format(type(value)))


    def add_option_query( self, query = '' ):
        self.__add_option_TL( 15, len( query ) )
        self.buffer += query

    def add_payload(self, payload=b""):
        if type(payload) == str:
            if upython:
                pload = bytearray(payload)
            else: # python3
                pload = bytearray(payload, encoding="utf-8")
        elif type(payload) == bytes:
            pload = payload
        else:
            raise ValueError("Unknown payload format {}".format(type(payload)))

        if len(payload) > 0:
            self.buffer += struct.pack( 'B', 0xFF )
            self.buffer += pload
        else:
            print ("Warning: Empty payload")



    def to_byte( self ):
        return self.buffer


    def get_tkl(self):
        return self.buffer[0] & 0b00001111

    def get_type ( self ):
        return( ( self.buffer[0] & 0x30 ) >> 4 )

    def get_mid( self ):
        return self.buffer[2] << 8 | self.buffer[3]

    def get_code( self ):
        return self.buffer[1]

    def dump(self, hexa=False):
        if hexa:
            print (binascii.hexlify(self.buffer))

        code = self.get_code()
        clas = code >> 5
        detail = code & 0b00011111
        if clas == 0:
            c_name = code_name[code]
        else:
            c_name = '{0:x}.{1:02X}'.format(clas, detail)

        print ("{0:4} 0x{1:04X} {2:6s}".format(
            type_name[self.get_type()],
            self.get_mid(), c_name
            ), end="")

        buf_ptr = 4

        tkl = self.get_tkl()
        if tkl > 0:
            print ("T=", end="")
            for i in range (0, tkl):
                print ("{:02X}".format(self.buffer[buf_ptr]), end="")
                buf_ptr += 1

        print()
        coap_option = 0
        while buf_ptr < len(self.buffer):
            if self.buffer[buf_ptr] == 0xFF:
                print ("---CONTENT")
                buf_ptr += 1
                print ("hex:", binascii.hexlify(self.buffer[buf_ptr:]))
                print ("txt:", str(self.buffer[buf_ptr:]))

                return

            tlv = self.buffer[buf_ptr]
            delta_option = tlv >> 4
            length_option = tlv & 0b00001111
            buf_ptr +=1

            if delta_option == 13:
                delta_option = self.buffer[buf_ptr]+13
                buf_ptr += 1

            coap_option += delta_option
            if coap_option in option_name:
                if option_name[coap_option][1] == int:
                    decoded = 0
                    for v in self.buffer[buf_ptr:buf_ptr+length_option]:
                        decoded <<= 8
                        decoded += v
                else:
                    decoded = option_name[coap_option][1](
                        self.buffer[buf_ptr:buf_ptr+length_option])
                print (">",
                option_name[coap_option][0],
                ":", decoded)

            buf_ptr += length_option

def send_ack(s, dest, coap):
    import time

    if not coap.get_type() in [CON, NON]:
        raise ValueError ("Not a CON or NON message")

    c_mid = coap.get_mid()
    timeout = 2
    attempts = 1

    while True:
        s.sendto (coap.to_byte(), dest)

        if coap.get_type() == NON:
            return None

        s.settimeout(10)
        try:
            resp,addr = s.recvfrom(2000)
            answer = Message(resp)
            if answer.get_mid() == c_mid:
                return answer
        except:
            print ("timeout", timeout, attempts)
            time.sleep (timeout)
            timeout *= 2
            attempts +=1
            if attempts > 4:
                raise ValueError("Too many attempts")

def get_msg(s, filter=None, timeout=2):
    s.settimeout(timeout)
    try:
        m, d = s.recvfrom(2000)
        if not filter or filter == d:
            return Message(m)
        else:
            return None
    except:
        return None

if __name__ == "__main__":
    coap = Message()

    coap.new_header(token=0x1122334455)
    coap.dump()
