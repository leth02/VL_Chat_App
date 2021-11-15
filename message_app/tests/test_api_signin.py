import pytest
import requests
import json

def test_login_valid(supply_url):
	url = supply_url + "/signin" 
	data = {'username':'long','password':'12345'}
	resp = requests.post(url, data=data)
	assert resp.status_code == 200

def test_login_no_password(supply_url):
	url = supply_url + "/signin" 
	data = {'username':'long'}
	resp = requests.post(url, data=data)
	print(resp.text)
	j = json.loads(resp.text)
	assert resp.status_code == 400
	assert j['Error'] == "Bad request. Invalid username/password. Please try again.", resp.text

def test_login_no_email(supply_url):
	url = supply_url + "/signin" 
	data = {}
	resp = requests.post(url, data=data)
	j = json.loads(resp.text)
	assert resp.status_code == 400, resp.text
	assert j['Error'] == "Bad request. Invalid username/password. Please try again.", resp.text

def test_login_wrong_password(supply_url):
	url = supply_url + "/signin" 
	data = {'username': 'long', 'password': '1234'}
	resp = requests.post(url, data=data)
	j = json.loads(resp.text)
	assert resp.status_code == 400, resp.text
	assert j['Error'] == "Bad request. Invalid username/password. Please try again.", resp.text

def test_login_invalid_user(supply_url):
	url = supply_url + "/signin" 
	data = {'username': 'test', 'password': "test"}
	resp = requests.post(url, data=data)
	j = json.loads(resp.text)
	assert resp.status_code == 400, resp.text
	assert j['Error'] == "Bad request. Invalid username/password. Please try again.", resp.text
