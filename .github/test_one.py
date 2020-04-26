#!/usr/bin/python3
import pytest

def try_importing():
	try:
		from tasks import *
		assert "0"
	except:
		assert "1"

def test_imports():
	assert hasattr(try_importing(),"0")