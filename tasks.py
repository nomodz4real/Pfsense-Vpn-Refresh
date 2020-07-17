#!/usr/bin/python3
import os,sys,json
import requests
from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi

def populate_test_files_and_vars():
	if os.path.isfile('.pfsense_ip_and_port') and os.path.isfile('.pfsense_key_and_secret'):
		return 2
	else:
		try:	
			with open('.pfsense_ip_and_port','w') as file:
				file.write("pfsenseserverip pfsesnseserverlisteningport")
			with open('.pfsense_key_and_secret','w') as file:
				file.write("pfsensefauxapikey pfsensefauxapisecret")
			print("\n#####################################################################\nGenerated sample config files:\n.pfsense_ip_and_port\n.pfsense_key_and_secret\n\nPlease refer to README.txt for instructions on what\nto place in these files for proper function\n#####################################################################")
			return 0
		except:
			return 1

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
	try:
		return PfsenseFauxapi(fauxapi_host, fauxapi_apikey, fauxapi_apisecret, debug=False)
	except:
		return 1

def get_pfsense_config():
	try:
		client_config = build_faux_api_connection().config_get('openvpn')
		return client_config
	except:
		return 1

def set_pfsense_config(bestserver):
	client_config = get_pfsense_config()
	try:
		for item in client_config["openvpn-client"]:
			item["server_addr"] = str(bestserver)
			item["description"] = str(bestserver)
		build_faux_api_connection().config_set(client_config, 'openvpn')
	except:
		return 1

def reload_pfsense():
	try:
		build_faux_api_connection().config_reload()
		return 0
	except:
		return 1

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

populate_test_files_and_vars()
bestserver = get_server()
print("\nServer Found: " + bestserver)
if os.path.isdir('/var/log/'):
    with open('/var/log/vpnrefresh','a') as file:
        file.write("\n\nServer Found: " + bestserver)
set_pfsense_config(bestserver)
reload_pfsense()
print("\nDone!")
