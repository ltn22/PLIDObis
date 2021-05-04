#!/bin/sh
#
# install mongodb
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.4 main" | tee "/etc/apt/sources.list.d/mongodb-org-4.4.list"
apt-get update
apt-get install -y mongodb-org
# Java
apt install -y default-jre
#
apt install -y python3-pip
python3.9 -m pip install pymodbus termcolor flask requests cbor2 beebotte pymongo numpy matplotlib
