import sys
import os
sys.path.insert(0, os.getcwd())
from message_app import create_app
import pytest

@pytest.fixture
def sample_request():
	data = {
		"valid": {
            'id':0,'sender_id': 0,
            'reciever_id': 1,
            'accepted': 1,
            'requested_time': 12345343,
            'accepted_time': 12344524,
            },
        "invalid": {
            "unknow_user": {
                'id':0,
                'sender_id': 0,
                'reciever_id': 1,
                'accepted': 1,
                'requested_time': 12345343,
                'accepted_time': 12344524,
            },
            "invalid_message": {
                'id':0,
                'sender_id': 0,
                'reciever_id': 1,
                'accepted': 0,
                'requested_time': 12345343,
                'accepted_time': 12344524,
            },
		}
	}
	return data

@pytest.fixture
def sample_messages():
	data = {
		"valid": {
			'id_mesage': 0,
			'messages_content': "validPassword1",
			'time_stamps': 1234567889,
			'seen': 0,
            'sender_id': 0,
            'reciever_id': 1,
		},
		"invalid": {
			"wrong_recieve_message": {
				'id_mesage': 0,
			    'messages_content': 1235434653623,
			    'time_stamps': 1234567889,
			    'seen': 0,
                'sender_id': 0,
                'reciever_id': 1,
			},
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