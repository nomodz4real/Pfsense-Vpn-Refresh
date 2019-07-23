#!/bin/bash
# Bash script to refresh the vpn client for outbound traffic on Michael
# Created by Anthony Malone (antmmalone@gmail.com)
#
# Version 1.0 - Initial Release [Jul. 22, 2019]

# Export the key and secret for the api on Michael
export FAUXAPI_APIKEY=key
export FAUXAPI_APISECRET=secret

# Some abstraction of firewalls password
pfsensepass=`cat /scriptsubdirectory/.pfsensepassfile`

# Find the US server with the least load using https://github.com/mrzool/nordvpn-server-find
/scriptsubdirectory/nordvpn-server-find/nordvpn-server-find -l US -c 10 -n 1 | grep .nordvpn.com | cut -d " " -f 1 > bestserverfound

# Get the config and write it to a file
/scriptsubdirectory/getconfig.py 192.168.1.1 468 | jq . > client.json

# Edit the grabbed config file
/scriptsubdirectory/servermanipulation.py

# Write the config to Michael and reload the config
/scriptsubdirectory/setconfig.py 192.168.1.1 468 | jq .

# Reload the openvpn service on Michael
echo -e """8\recho \"<?php include('openvpn.inc'); openvpn_resync_all();?>\" | php -q\rexit\r0\r""" | sshpass -p $pfsensepass ssh admin@192.168.1.1 &>> /dev/null

# Cleanup
rm bestserverfound client.json autooutput.json

echo "Done!"
