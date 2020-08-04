#!/usr/bin/python3
import os
import json
import requests
import getpass
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi
import datetime

def populate_test_files_and_vars(user):
	if user == "root":
		path = "/root/.vpnrefresh"
	else:
		path = "/home/{}/.vpnrefresh".format(user)
	if os.path.isfile('{}/.pfsense_ip_and_port'.format(path)) and os.path.isfile('{}/.pfsense_key_and_secret'.format(path)):
		return path
	else:
		try:	
			os.mkdir(path)
			with open('{}/.pfsense_ip_and_port'.format(path),'w') as file:
				file.write("<pfsenseserverip> <pfsesnseserverlisteningport>")
			with open('{}/.pfsense_key_and_secret'.format(path),'w') as file:
				file.write("<pfsensefauxapikey> <pfsensefauxapisecret>")
			print("\n#####################################################################\nGenerated sample config files:\n.pfsense_ip_and_port\n.pfsense_key_and_secret in {}\n\nPlease refer to README.txt for instructions on what\nto place in these files for proper function\n#####################################################################".format(path))
			return path
		except:
			raise Exception("Unable to write to {} directory, please ensure permissions are correct".format(path))

def grab_fields_from_file(filename,option):
	with open(filename,'r') as file:
		if option == "ip" or option == "key":
			result = file.read().split(" ")
		else:
			raise Exception("Improper option passed to grab_fields_from_file method.")
	return result

def build_faux_api_connection():
	# First some URL formatting that I worked on to allow for custom port numbers in your 
	# pfsense server's web configurator URL
	host_raw = grab_fields_from_file(".pfsense_ip_and_port","ip")
	fauxapi_host="{}:{}".format(host_raw[0],host_raw[1].strip())
	# Grab the key and secret from the user created file
	key_secret = grab_fields_from_file(".pfsense_key_and_secret","key")
	# Return callable function to interact with pfsense server
	try:
		return PfsenseFauxapi(fauxapi_host, key_secret[0], key_secret[1].strip(), debug=False)
	except:
		raise Exception("Unable to read data files to build connection to the FauxAPI instance or data found was incorrect.")

def get_pfsense_config():
	try:
		client_config = build_faux_api_connection().config_get('openvpn')
		return client_config
	except:
		raise Exception("Unable to grab the configuration data for openvpn")

def set_pfsense_config(bestserver):
	client_config = get_pfsense_config()
	try:
		for item in client_config["openvpn-client"]:
			item["server_addr"] = str(bestserver)
			item["description"] = str(bestserver)
		build_faux_api_connection().config_set(client_config, 'openvpn')
	except:
		raise Exception("Unable to set new parameters for openvpn-client configuration")

def reload_pfsense():
	try:
		build_faux_api_connection().config_reload()
		return 0
	except:
		raise Exception("Unable to reload pfsense configuration")

def grab_server_list_from_nord():
	server_list = requests.get("https://nordvpn.com/wp-admin/admin-ajax.php?action=servers_recommendations")
	return server_list.json()

# Parses the json data from the nordvpn recommended servers url to grab the servername and load
def parse_server_list(server_list):
	counter = 0
	parsed_server_list = {}
	for key in server_list:
		parsed_server_list['hostname'+str(counter)] = key['hostname']
		parsed_server_list['load'+str(counter)] = key['load']
		counter += 1 
	return parsed_server_list

# This one is a mess but it works, will have to come back to it at some point
def check_for_lowest_load(parsed_server_list):
	load_check = parsed_server_list['load0']
	best_server = parsed_server_list['hostname0']
	set_host = ""
	for load in parsed_server_list:
		if set_host == "y":
			best_server = parsed_server_list[load]
			set_host = "n"
		else:
			set_host = "n"
		if load.startswith('load'):
			if parsed_server_list[load] < load_check:
				load_check = parsed_server_list[load]
				set_host = "y"
	return best_server

def get_server():
	best_server = check_for_lowest_load(parse_server_list(grab_server_list_from_nord()))
	return best_server

user = getpass.getuser()
path = populate_test_files_and_vars(user)
os.chdir(path)
bestserver = get_server()
print("\nServer Found: " + bestserver)
try:
	with open('/var/log/vpnrefresh','a') as file:
		file.write(str(datetime.datetime.now()) + " Server Found: " + bestserver)
except:
	print("Unable to write to /var/log directory")
set_pfsense_config(bestserver)
reload_pfsense()
print("\nDone!")
