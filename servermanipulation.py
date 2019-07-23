#!/usr/bin/python
import json
import sys

with open('bestserverfound','r') as file:
	bestserver = file.readline()

print("Server Found: " + bestserver.split("[1m")[1])

with open('client.json', 'r') as file:
	json_data = json.load(file)
	for item in json_data["openvpn-client"]:
		#print(item["server_addr"])
		item["server_addr"] = str(bestserver.split("[1m")[1].split("\n")[0])
		item["description"] = str(bestserver.split("[1m")[1].split("\n")[0])
		#print(item["server_addr"])
with open('autooutput.json','w') as file:
	json.dump(json_data, file, indent=2)