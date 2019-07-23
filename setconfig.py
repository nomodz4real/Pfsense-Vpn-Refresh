#!/usr/bin/python
import os, sys, json, inspect
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi

# config
fauxapi_host='{}:{}'.format(sys.argv[1], sys.argv[2])
fauxapi_apikey=os.getenv('FAUXAPI_APIKEY')
fauxapi_apisecret=os.getenv('FAUXAPI_APISECRET')

FauxapiLib = PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=False)

with open('autooutput.json','r') as file:
	json_data = json.load(file)
	FauxapiLib.config_set(json_data, 'openvpn')

FauxapiLib.config_reload()