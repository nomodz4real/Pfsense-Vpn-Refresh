#!/usr/bin/python
import os, sys, json
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi

# Setting up FauxAPI
fauxapi_host='{}:{}'.format(sys.argv[1], sys.argv[2])
fauxapi_apikey=os.getenv('FAUXAPI_APIKEY')
fauxapi_apisecret=os.getenv('FAUXAPI_APISECRET')
FauxapiLib = PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=False)

# Grabbing the servername
bestserver = sys.argv[3].split("[1m")[1].split("\n")[0]

client_config = FauxapiLib.config_get('openvpn')

print("Server Found: " + bestserver)

for item in client_config["openvpn-client"]:
        item["server_addr"] = str(bestserver)
        item["description"] = str(bestserver)

FauxapiLib.config_set(client_config, 'openvpn')

FauxapiLib.config_reload()
