import pytest
import os
import tempfile
import time

from message_app import create_app
from message_app.db.db import init_SQLAlchemy, DB as db
from message_app.model import User, Messages, Conversations, ConversationRequest
from message_app.utils import hash_pw

# Name of the testing database
TEST_DB = os.path.join("test_message_app_db.sqlite3")

# The database URI that should be used for the connection.
TEST_DB_URI = os.path.join("sqlite:///", TEST_DB)

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': TEST_DB_URI,
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

    # Initialize test database
    init_SQLAlchemy()

    #============= Populate testing data =======================

    # User
    password_hash_1 = hash_pw("password_hash_1")
    password_hash_2 = hash_pw("password_hash_2")
    password_hash_3 = hash_pw("password_hash_3")
    user1 = User(username="username1", email="email1@test.com", password_hash=password_hash_1)
    user2 = User(username="username2", email="email2@test.com", password_hash=password_hash_2)
    user3 = User(username="username3", email="email3@test.com", password_hash=password_hash_3)
    User.insert(user1)
    User.insert(user2)
    User.insert(user3)

    # Conversations
    conv1 = Conversations()
    conv2 = Conversations()
    Conversations.insert(conv1)
    Conversations.insert(conv2)
    conv1.participants.append(user1)
    conv1.participants.append(user2)
    conv2.participants.append(user1)
    conv2.participants.append(user3)

    # Messages
    m1 = Messages(content="user1 sends a message to conversation1")
    Messages.insert(m1)
    m1.sender_id = user1.id
    conv1.messages.append(m1)

    m2 = Messages(content="user2 sends a message to conversation1")
    Messages.insert(m2)
    m2.sender_id = user2.id
    conv1.messages.append(m2)

    # After updating all the foreign ID, an explicitly commit is needed to unlock the database.
    db.session.commit()

    # Populate testing data for request_conversation table
    ConversationRequest.insert(ConversationRequest(
        initiator_id=1,
        receiver_id=2,
        request_time=12345678
        ))
    ConversationRequest.insert(ConversationRequest(
        initiator_id=3,
        receiver_id=2,
        accepted=1,
        request_time=12345678
        ))

    yield db
    tear_down()

@pytest.fixture
def test_client(app):
    return app.test_client()


@pytest.fixture
def test_runner(app):
    return app.test_cli_runner()

