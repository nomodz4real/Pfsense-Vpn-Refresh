#!/usr/bin/python3
import pytest, os
os.chdir("../../")
from tasks import *

def populate_test_files_and_vars():
	with open('.pfsense_ip_and_port','w') as file:
		file.write("testip testport")
	with open('.pfsense_key_and_secret','w') as file:
		file.write("testip testport")

def test_functions():
	bestserver = populate_test_files_and_vars()
	assert set_pfsense_config(bestserver) == 0
	assert reload_pfsense() == 0