#!/usr/bin/python
import os, sys, json, inspect
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi

# config
fauxapi_host='{}:{}'.format(sys.argv[1], sys.argv[2])
fauxapi_apikey=os.getenv('FAUXAPI_APIKEY')
fauxapi_apisecret=os.getenv('FAUXAPI_APISECRET')

FauxapiLib = PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=False)


if sys.argv[3] == "get":
	client_config = FauxapiLib.config_get('openvpn')
	print(json.dumps(
	    client_config
	))
elif sys.argv[3] == "set":
	with open('autooutput.json','r') as file:
		json_data = json.load(file)
		FauxapiLib.config_set(json_data, 'openvpn')

	FauxapiLib.config_reload()