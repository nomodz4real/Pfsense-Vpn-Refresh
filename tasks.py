#!/usr/bin/python3
import os, sys, json
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi

def grab_fields_from_file(filename,option):
	# Grab working path to make sure we actually find the files, I plan to enforce a location
	# for this script at some point but that's a whole project unto itself
	full_file_path = os.getcwd() + "/" + filename
	with open(filename,'r') as file:
		if option == "ip" or option == "key":
			result = file.read().split(" ")
		else:
			return "Invalid Request"
	stripped_list = []
	for i in result:
		stripped_list.append(i.strip())
	return stripped_list 

def build_faux_api_connection():
	# First some URL formatting that I worked on to allow for custom port numbers in your 
	# pfsense server's web configurator URL
	fauxapi_host='{}:{}'.format(grab_fields_from_file(".pfsense_ip_and_port","ip")[0],grab_fields_from_file(".pfsense_ip_and_port","ip")[1])
	# Grab the key and secret from the user created file
	fauxapi_apikey = grab_fields_from_file(".pfsense_key_and_secret","key")[0]
	fauxapi_apisecret = grab_fields_from_file(".pfsense_key_and_secret","key")[1]
	# Return callable function to interact with pfsense server
	return PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=False)

def get_pfsense_config():
	client_config = build_faux_api_connection().config_get('openvpn')
	return client_config

def set_pfsense_config(bestserver):
	client_config = get_pfsense_config()
	for item in client_config["openvpn-client"]:
		item["server_addr"] = str(bestserver)
		item["description"] = str(bestserver)
	try:
		build_faux_api_connection().config_set(client_config, 'openvpn')
		return 0
	except:
		return 1

def reload_pfsense():
	try:
		build_faux_api_connection().config_reload()
		return 0
	except:
		return 1

bestserver = sys.argv[1].split("[1m")[1].split("\n")[0]
print("Server Found: " + bestserver)
set_pfsense_config(bestserver)
reload_pfsense()