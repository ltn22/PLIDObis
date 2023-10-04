#!/bin/sh
#

rm -f /etc/apt/source.list
echo "deb [trusted=yes] https://deb.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list
echo "deb [trusted=yes] https://deb.debian.org/debian buster-backports main contrib non-free" >> /etc/apt/sources.list
echo "deb [trusted=yes] file:///usr/share/core-repository ./" >> /etc/apt/sources.list
apt update --fix-missing --allow-unauthenticated

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
python3.9 -m pip install pymodbus==2.5.2 termcolor twisted flask requests cbor2 beebotte kpn_senml psutil pymongo numpy matplotlib
python3 -m pip install pymodbus termcolor twisted
