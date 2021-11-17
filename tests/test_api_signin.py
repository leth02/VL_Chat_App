import pytest
import os
from db import db

def test_login_valid(sampleSignInData, client, mocker):
	mocker.patch("db.db.query_db", return_value = {"password": "9bb4acdd315eefe2ab3ef7bd25c17f4a092f426ed2a97898a6e1c0014875cdf7", "salt": r"b'\xe9a\xf2\xd7_'"})
	resp = client.post('/api/signin', data = sampleSignInData["valid"])
	assert resp.status_code == 302

def test_login_wrong_password(sampleSignInData, client, mocker):
	mocker.patch("db.db.query_db", return_value = {"password": "9bb4acdd315eefe2ab3ef7bd25c17f4a092f426ed2a97898a6e1c0014875cdf7", "salt": r"b'\xe9a\xf2\xd7_'"})
	resp = client.post('/api/signin', data = sampleSignInData["invalid"]["wrong_password"])
	assert resp.json["Error"] == "Bad request. Invalid username/password. Please try again."
	assert resp.status_code == 400

def test_login_invalid_username(sampleSignInData, client, mocker):
	mocker.patch("db.db.query_db", return_value = {"password": "9bb4acdd315eefe2ab3ef7bd25c17f4a092f426ed2a97898a6e1c0014875cdf7", "salt": r"b'\xe9a\xf2\xd7_'"})
	resp = client.post('/api/signin', data = sampleSignInData["invalid"]["invalid_user"])
	assert resp.json["Error"] == "Bad request. Invalid username/password. Please try again."
	assert resp.status_code == 400