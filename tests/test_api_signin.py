import pytest

from message_app.utils import HASHING_PACKAGE

class TestAPISignIn:
	def test_valid_signin(self, sampleSignInData, test_db, test_client, mocker):
		for key in sampleSignInData["valid"].keys():
			valid_user = sampleSignInData["valid"][key]
			mocker.patch("message_app.user_sign_in.hashing", return_value=HASHING_PACKAGE(valid_user["password_hash"], valid_user["password_salt"]))
			resp = test_client.post('/api/signin', data={"username": valid_user["username"], "password": valid_user["password_hash"]})
			assert resp.status_code == 302

	def test_signin_wrong_password(self, sampleSignInData, test_db, test_client, mocker):
		wrongPassword = sampleSignInData["invalid"]["wrong_password"]
		mocker.patch("message_app.user_sign_in.hashing", return_value=HASHING_PACKAGE(wrongPassword["password_hash"], wrongPassword["password_salt"]))
		resp = test_client.post('/api/signin', data={"username": wrongPassword["username"], "password": wrongPassword["password_hash"]})
		assert resp.json["Error"] == "Bad request. Invalid login credentials. Please try again."
		assert resp.status_code == 400

	def test_signin_invalid_username(self, sampleSignInData, test_db, test_client):
		invalid_user = sampleSignInData["invalid"]["invalid_user"]
		resp = test_client.post('/api/signin', data={"username": invalid_user["username"], "password": invalid_user["password_hash"]})
		assert resp.json["Error"] == "Bad request. Invalid login credentials. Please try again."
		assert resp.status_code == 400
