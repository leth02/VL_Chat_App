import pytest

def test_login_valid(sampleSignInData, client, mocker):
	for key in sampleSignInData["valid"].keys():
		validUser = sampleSignInData["valid"][key]
		mocker.patch("message_app.db.query_db", return_value={"password_hash": validUser["password_hash"], "salt": validUser["salt"]})
		mocker.patch("message_app.hashing", return_value=validUser["password_hash"])
		resp = client.post('/api/signin', data={"username": validUser["username"], "password": validUser["password_hash"]})
		assert resp.status_code == 302

def test_login_wrong_password(sampleSignInData, client, mocker):
	wrongPassword = sampleSignInData["invalid"]["wrong_password"]
	validUser = sampleSignInData["valid"]["valid_1"]
	mocker.patch("message_app.query_db", return_value={"password_hash": validUser["password_hash"], "salt": validUser["salt"]})
	mocker.patch("message_app.hashing", return_value=wrongPassword["password"])
	resp = client.post('/api/signin', data={"username": wrongPassword["username"], "password": wrongPassword["password"]})
	assert resp.json["Error"] == "Bad request. Invalid username/password. Please try again."
	assert resp.status_code == 400

def test_login_invalid_username(sampleSignInData, client, mocker):
	wrongPassword = sampleSignInData["invalid"]["invalid_user"]
	mocker.patch("message_app.query_db", return_value={})
	resp = client.post('/api/signin', data={"username": wrongPassword["username"], "password": wrongPassword["password"]})
	assert resp.json["Error"] == "Bad request. Invalid username. Please try again."
	assert resp.status_code == 400
