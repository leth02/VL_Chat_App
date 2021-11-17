import pytest

def test_valid_signup(sampleSignUpData, client):
	resp = client.post('/api/signup', data = sampleSignUpData["valid"])
	assert resp.status_code == 302

def test_signup_wrong_confirm_password(sampleSignUpData, client):
	resp = client.post('/api/signup', data = sampleSignUpData["invalid"]["wrong_confirm_password"])
	assert resp.json["Error"] == "Bad request. Password doesn't not match. Please try again."
	assert resp.status_code == 400

def test_signup_invalid_email(sampleSignUpData, client):
	resp = client.post('/api/signup', data = sampleSignUpData["invalid"]["invalid_email"])
	assert resp.json["Error"] == "Bad request. Invalid Email. Please try a valid email."
	assert resp.status_code == 400

def test_signup_taken_username(sampleSignUpData, client):
	resp = client.post('/api/signup', data = sampleSignUpData["invalid"]["taken_username"])
	assert resp.json["Error"] == "Bad request. Username has been taken. Please try another one."
	assert resp.status_code == 400