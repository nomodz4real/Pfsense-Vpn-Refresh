#!/usr/bin/python3
import pytest,os
os.chdir("../")
from tasks import *

def test_functions():
	assert set_pfsense_config(bestserver) == 1
	assert reload_pfsense() == 1