import pytest
import os
import sys

from message_app import create_app
from message_app.db.db import DB as db

# Name of the testing database
TEST_DB = os.path.join("test_message_app_db.sqlite3")

# The database URI that should be used for the connection.
TEST_DB_URI = os.path.join("sqlite:///", TEST_DB)

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DB_URI
    }, __name__)

    with app.app_context():
        yield app

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