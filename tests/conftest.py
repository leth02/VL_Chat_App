import sys, os
sys.path.insert(0, os.getcwd())
from message_app import create_app
import pytest

@pytest.fixture
def sampleSignInData():
	data = {
		"valid": {'username': 'long','password': '12345','salt': r"b'\xe9a\xf2\xd7_'"},
		"invalid": {
			"wrong_password": {'username': 'long', 'password': '1234'},
			"invalid_user": {'username': 'wrong_user', 'password': "test"}
		}
	}
	return data

@pytest.fixture
def sampleSignUpData():
	data = {
		"valid": {
			"username": "validUserName",
			"password": "validPassword",
			"confirmPassword": "validPassword",
			"email": "validEmail@test.com"
		},
		"invalid": {
			"wrong_confirm_password": {
				"username": "nameA",
				"password": "testPassword",
				"confirmPassword": "WrongConfirmPassword",
				"email": "test@gmail.com"
			},
			"invalid_email": {
				"username": "nameA",
				"password": "passwordA",
				"confirmPassword": "passwordB",
				"email": "invalidEmailAddress"
			},
			"taken_username": {
				"username": "long",
				"password": "testPassword",
				"confirmPassword": "testPassword",
				"email": "test@gmail.com"
			}
		}
	}
	return data

@pytest.fixture
def client():
	app = create_app({
		"TESTING": True
	})
	with app.test_client() as test_client:
		with app.app_context():
			yield test_client