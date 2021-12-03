import pytest
import os
import tempfile

from message_app import create_app
<<<<<<< HEAD
from message_app.db.db import DB as db

# Name of the testing database
TEST_DB = os.path.join("test_message_app_db.sqlite3")

# The database URI that should be used for the connection.
TEST_DB_URI = os.path.join("sqlite:///", TEST_DB)
from message_app.db.db import get_db

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    data_sql = f.read().decode("utf8")
=======
from message_app.db.db import init_db
>>>>>>> ff1e16a (update test_api_login)

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


@pytest.fixture
def test_runner(app):
    return app.test_cli_runner()


@pytest.fixture
def sampleSignInData():
	data = {
		"valid":{
			"valid_1": {'username': 'username1', 'password_hash': 'password_hash_1', 'salt': 'password_salt_1'},
			"valid_2": {'username': 'username2', 'password_hash': 'password_hash_2', 'salt': 'password_salt_2'},
			"valid_3": {'username': 'username3', 'password_hash': 'password_hash_3', 'salt': 'password_salt_3'},
		},
		
		"invalid": {
			"wrong_password": {'username': 'username1', 'password': "wrongPassword"},
			"invalid_user": {'username': 'wrong_user', 'password': "test"}
		}
	}
	return data

@pytest.fixture
def sampleSignUpData():
	data = {
		"valid": {
			"username": "validUserName1",
			"password": "validPassword1",
			"confirmPassword": "validPassword1",
			"email": "validEmail@test.com"
		},
		"invalid": {
			"wrong_confirm_password": {
				"username": "wrongConfirmPassword",
				"password": "wrongConfirmPassword",
				"confirmPassword": "",
				"email": "wrongConfirmPassword@gmail.com"
			},
			"invalid_email": {
				"username": "invalidEmailAddress",
				"password": "invalidEmailAddress",
				"confirmPassword": "invalidEmailAddress",
				"email": "invalidEmailAddress"
			},
			"taken_username": {
				"username": "username1",
				"password": "takenUserName",
				"confirmPassword": "takenUserName",
				"email": "takenUserName@gmail.com"
			}
		}
	}
	return data