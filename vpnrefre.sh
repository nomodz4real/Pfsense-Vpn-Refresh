#!/bin/bash

# Grab the path of the script's directory
path=`pwd`

#Installing nordvpn-server-find if directory not found. 
#Hopefully I can convert to the website calls like in dejablues scripts
if [ ! -d $path/nordvpn-server-find ]
then
	git clone https://github.com/mrzool/nordvpn-server-find.git
fi

# Export the key and secret used by the api to your local system at runtime
export FAUXAPI_APIKEY=`cat $path/.pfsense_key_and_secret | cut -d " " -f 1`
export FAUXAPI_APISECRET=`cat $path/.pfsense_key_and_secret | cut -d " " -f 2`

# Grab the ip and port for the pfSense server
pfSense_ip_address=`cat $path/.pfsense_ip_and_port | cut -d " " -f 1`
pfSense_port=`cat $path/.pfsense_ip_and_port | cut -d " " -f 2`

# Some abstraction of the firewalls password which is used for the ssh login
pfsensepass=`cat $path/.pfsensepassfile`

# Find the US server with the least load using https://github.com/mrzool/nordvpn-server-find
bestserverfound=`$path/nordvpn-server-find/nordvpn-server-find -l US -c 10 -n 1 | grep .nordvpn.com | cut -d " " -f 1`

# Update the server to the one found by nordvpn-server-find
$path/tasks.py $pfSense_ip_address $pfSense_port $bestserverfound

echo "Done!"