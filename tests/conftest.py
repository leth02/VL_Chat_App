import pytest
import os
import sys
import tempfile

from message_app import create_app
from message_app.db.db import DB as db

# Name of the testing database
TEST_DB = os.path.join("test_message_app_db.sqlite3")

# The database URI that should be used for the connection.
TEST_DB_URI = os.path.join("sqlite:///", TEST_DB)
from message_app.db.db import get_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    data_sql = f.read().decode("utf8")

@pytest.fixture
def app():
    # create a temporary database's path in memory.
    # db_fd is file descriptor and db_path is database path
    # this line will be removed in the future after we have request message model
    # and use database file on disk for testing
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DB_URI,
        'DATABASE': db_path, # this line will be removed like db_df, db_path
    }, __name__)

    with app.app_context():
        get_db().executescript(data_sql) # this line will be removed like db_df, db_path
        yield app

    # close and delete database file and path after the test is over
    # these lines will be removed like db_db, db_path
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def test_db(app):
    def tear_down():
        # This function drops all the tables, removes the current connection, and deletes the temporary database file.
        db.drop_all()
        db.session.remove()
        os.remove(os.path.join("tests", TEST_DB))

    # Attach the application to SQLAlchemy
    db.init_app(app)

    # Creates a testing database and all tables for that database.
    db.create_all()

    yield db
    tear_down()

@pytest.fixture
def test_client(app):
    return app.test_client()
## test for check conversation_id or not 
def check_conversation():
	data = {
		"valid": {
            "valid_1" : {'id': 1, 'participants': 'sturekev', 'last_message_id': 1},
            "valid_2" : {'id': 2, 'participants': 'sturekev', 'last_message_id': 1},
            "valid_3" : {'id': 3, 'participants': 'sturekev', 'last_message_id': 1},
        },
		"invalid": {
			"wrong_conversation_id": {'id': 0, 'participants': 'sturekev', 'last_message_id': 1},
			"invalid_last_message_id": {'id': '3W', 'participants': 'sturekev', 'last_message_id': '1'}
		}
	}
	return data

@pytest.fixture
def test_save_messages():
	data = {
		"valid": {
			'valid_1': {
                'id': 0, 'conversation_id': 0, 'sender_id': 0,'reciever_id': 1,
                'content': "welcome to VL chat app" , 'seen': 0, 'timestamp': 1234566,
            },
            'valid_2': {
                'id': 1, 'conversation_id': 1, 'sender_id': 0,'reciever_id': 1,
                'content': "welcome to VL chat app" , 'seen': 0, 'timestamp': 1234566,
            },
		},
		"invalid": {
			'seen': {
                'id': 1, 'conversation_id': 1, 'sender_id': 0,'reciever_id': 1,
                'content': "welcome to VL chat app" , 'seen': 0, 'timestamp': 1234566,
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
## test for single collumn fail on messages table

 
@pytest.fixture
def test_runner(app):
    return app.test_cli_runner()
