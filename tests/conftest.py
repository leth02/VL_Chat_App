import sys
sys.path.insert(0, 'D:\Luther\Self-Learning\Chat App\VL_Chat_App')
from message_app import create_app
from config import KEY
import pytest

@pytest.fixture
def sampleData():
	data = {
		"valid": {'username': 'long','password': '12345'},
		"invalid": {
			"wrong_password": {'username': 'long', 'password': '1234'},
			"invalid_user": {'username': 'wrong_user', 'password': "test"}
		}
	}
	return data

@pytest.fixture
def client():
	app = create_app({
		"TESTING": True,
		"SECRET_KEY": KEY
	})
	with app.test_client() as test_client:
		with app.app_context():
			yield test_client

print("asd")