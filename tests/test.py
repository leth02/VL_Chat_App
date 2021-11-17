import pytest
import json

def test_login_valid(sampleData, client):
	resp = client.post('/api/signin', data = sampleData["valid"])
	assert resp.status_code == 302

def test_login_wrong_password(sampleData, client):
	resp = client.post('/api/signin', data = sampleData["invalid"]["wrong_password"])
	assert resp.json["Error"] == "Bad request. Invalid username/password. Please try again."
	assert resp.status_code == 400

def test_login_invalid_username(sampleData, client):
	resp = client.post('/api/signin', data = sampleData["invalid"]["invalid_user"])
	assert resp.json["Error"] == "Bad request. Invalid username/password. Please try again."
	assert resp.status_code == 400