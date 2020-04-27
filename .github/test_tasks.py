#!/usr/bin/python3
import pytest, os
os.chdir("/home/runner/work/Pfsense-Vpn-Refresh/Pfsense-Vpn-Refresh")
from tasks import *

def test_functions():
	assert set_pfsense_config(bestserver) == 1
	assert reload_pfsense() == 1