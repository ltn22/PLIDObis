# Pygate
Pygate with chirpstack gateway bridge

This repository aims at providing the tools necesary to create a LoRaWAN Gateway using the chirptack platform

## Hardware Needed

* Raspberry Pi 3.0 with SD Card (> 8GB) (if chirpstack-gateway-bridge at the gateway side)
* PyGate avec PoE (if powered / Ethernet conection)
* WiPy, LoPy4 or GPy (tested with LoPy4)
* LoRa Antenna

## Software Requirements

* Chripstack Gateway Bridge
* Pycom firmware (for PyGate and WiPy / LoPy4 / GPy)
* Pymakr plugin in Atom or VS Code 

## Install

There are two options to set up our Pygate LoRa Gateway, we can either let the chirpstack stack (application and network servers, as well as the chirpstack geteway bridge) on a single site or we can implement the chirpstack gateway bridge on a raspberry pi. 
For the former, we shall follow the first 5 steps, and for the latter all the steps.

### 1. Atom and Pymakr

1.1 Install the correspondin version of atom, tested with v 1.54: ` https://github.com/atom/atom/releases/tag/v1.54.0` 

1.2 Install atom by downloading `atom-amd64.deb` and write in the command line: ` sudo dpkg -i atom-amd64.deb ` 

1.3 Open atom and add the module ` Pymakr`

### 2. Pycom firmware

To update the firmware we need to install the Firmware Updater Tool : 

2.1. Download and install from : [Pycom](https://software.pycom.io/downloads/linux-1.16.5.html) 
      `sudo dpkg -i pycom-fwtool-1.16.5-bionic-amd64.deb`

2.2. Insert the module (WiPy / LoPy4 / GPy) and the PoE Ethernet into the Pygate 

2.3. Attach the antenna to the Pygate (make sure there is nothig attached to the module)

2.4. Run the Firmware tool with ` pycom-fwtool ` on a linux terminal with the pygate connected through an USB type C 

2.5. Select the corresponding port, usually ` ttyACM0 `, you may need to open the ports with `sudo chmod a+rw /dev/ttyACM*`

2.6. Select on type ` pygate ` and make sure not to select the Pybytes options

2.7. If everithing goes well, we are good to go.

### 3. Create a ` config.json ` file as the one in this repository

3.1 Modify: 

3.1.1. Line 202 : ` "gateway_ID": "XXXXXXXXXXXXXXXX" ` put the GW identifier, you can generate a random ID when adding a new gateway on the chirpstack application server.

3.1.2. Line 203 : ` "server_address": "outils.plido.net", ` put the corresponding domain or IP of the network server, or `localhost` if the chirpstack-gateway-bridge is installed in the raspberry pi.

3.1.3. We could also put multiple servers, the pygate will forward all the messages to each one of the servers.

3.1.3. Upload it to the pycom module.

### 4. Create a ` main.py ` file as the one in this repository

4.1 Configure the internet connection, it can either be wifi or ethernet.

4.1.2. For the wifi conection, put the coresponding values on line 32: `wlan.connect(ssid='XXXX', auth=(WLAN.WPA2, "XXXX")) `

4.1.1. For the ethernet conection, make sure the line `from network import ETH` is uncommented.

4.1.2. For the ethernet conection, uncomment lines 42 to 52.

4.2 Upload `main.py` and reboot the module, if everithing goes ok, our Pygate is ready to send and receive LoRaWAN packets to the network server

### 5. Configure and send LoRaWAN packets on a pycom End Device.

5.1 Simply get the `join-plido.py` and put it into a pycom lopy module + extension board from `https://github.com/MarinoMtz/Roaming-ED`

### 6. Install the chirpstack gateway bridge on a Raspberry Pi.

In order to add more capabilities at the gateway side, another way to connect our pygate to the chirpstack stack, is to use a Raspberry pi and to create an MQTT broker on it. By doing that, we add a control layer that allow us to filter traffic at the gateway level. It is also helpful since it can also be configured to secure the conection with the LNS using TLS


