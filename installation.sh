#!/bin/sh
#
# install mongodb
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.4 main" | tee "/etc/apt/sources.list.d/mongodb-org-4.4.list"
apt-get update
apt-get install -y mongodb-org
apt-get install -y ntp
wget https://ci.eclipse.org/leshan/job/leshan/lastSuccessfulBuild/artifact/leshan-client-demo.jar -P lwm2m
wget https://ci.eclipse.org/leshan/job/leshan/lastSuccessfulBuild/artifact/leshan-server-demo.jar -P lwm2m
# Java
apt install -y default-jre
#
# Python3.5 will be used for emulated networks (modbus), Python3.9 will be used for IoT
apt install -y python3-pip
python3.9 -m pip install pymodbus termcolor twisted flask requests cbor2 beebotte kpn_senml psutil pymongo numpy matplotlib
python3 -m pip install pymodbus termcolor twisted
