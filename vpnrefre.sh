#!/bin/bash
# Bash script to refresh the vpn client for outbound traffic on your edge firewall
# Created by Anthony Malone (antmmalone@gmail.com)
#
# Version 1.0 - Initial Release [Jul. 22, 2019]

# Export the key and secret used by the api to your local system at runtime

export FAUXAPI_APIKEY=`cat $path/.pfsense_key_and_secret | cut -d " " -f 1`
export FAUXAPI_APISECRET=`cat $path/.pfsense_key_and_secret | cut -d " " -f 2`

# Grab the path of the script
path=`pwd`

# Grab the ip and port for the pfSense server
pfSense_ip_address=`cat $path/.pfsense_ip_and_port | cut -d " " -f 1`
pfSense_port=`cat $path/.pfsense_ip_and_port | cut -d " " -f 2`

# Some abstraction of the firewalls password which is used for the ssh login
pfsensepass=`cat $path/.pfsensepassfile`

# Find the US server with the least load using https://github.com/mrzool/nordvpn-server-find
bestserverfound=`$path/nordvpn-server-find/nordvpn-server-find -l US -c 10 -n 1 | grep .nordvpn.com | cut -d " " -f 1`

# Get the config and write it to a file
$path/reachout_to_pfsense.py $pfSense_ip_address $pfSense_port get | jq . > client.json

# Edit the grabbed config file
$path/servermanipulation.py $bestserverfound

# Write the config to Michael and reload the config
$path/reachout_to_pfsense.py $pfSense_ip_address $pfSense_port set | jq .

# Reload the openvpn service on Michael
echo -e """8\recho \"<?php include('openvpn.inc'); openvpn_resync_all();?>\" | php -q\rexit\r0\r""" | sshpass -p $pfsensepass ssh admin@$pfSense_ip_address &>> /dev/null

# Cleanup
if [ -e client.json ] || [ -e autooutput.json ]
then
	rm *.json
fi

echo "Done!"
