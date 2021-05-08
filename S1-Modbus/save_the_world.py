from pymodbus.client.sync import ModbusTcpClient # import modbus for Primary


# open connection with gateway at the specified address
client = ModbusTcpClient('127.0.0.1', port=5020)
client.connect()


# send a request to write a coil at register address 1 on unti 12 
client.write_coil(address=1, value=True, unit=12)

# send a request to read 1 coil at register address 1 on unit 12
result = client.read_coils(address=1,count=1, unit=12)

# dislay the result
print(result.bits[0])

# finished, close the TCP connection with the gateway. 
client.close()
