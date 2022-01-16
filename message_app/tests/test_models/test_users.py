import pytest
from message_app.model import User, ConversationRequest
from sqlalchemy.exc import IntegrityError
import json

@pytest.fixture
def sampleUserData():
    data = {
            "find_people_data": {
                "initial_data": [
                    {
                        "user_id": 1,
                        "username": "username1",
                        "request_id": 1,
                        "request_status": "pending",
                        "request_time": 12345678,
                        "is_sender": True,
                        "is_receiver": False
                        },
                    {
                        "user_id": 3,
                        "username": "username3",
                        "request_id": 2,
                        "request_status": "accepted",
                        "request_time": 12345678,
                        "is_sender": True,
                        "is_receiver": False
                        },
                    {
                        "user_id": 4,
                        "username": "username4",
                        "request_id": None,
                        "request_status": None,
                        "request_time": None,
                        "is_sender": None,
                        "is_receiver": None
                        },
                    ],
                "re_request_data": [
                    {
                        "user_id": 1,
                        "username": "username1",
                        "request_id": 3,
                        "request_status": "accepted",
                        "request_time": 123456789,
                        "is_sender": True,
                        "is_receiver": False
                        },
                    {
                        "user_id": 3,
                        "username": "username3",
                        "request_id": 2,
                        "request_status": "accepted",
                        "request_time": 12345678,
                        "is_sender": True,
                        "is_receiver": False
                        },
                    {
                        "user_id": 4,
                        "username": "username4",
                        "request_id": None,
                        "request_status": None,
                        "request_time": None,
                        "is_sender": None,
                        "is_receiver": None
                        },
                    ],
                "re_request_by_user_id_data": [
                    {
                        "user_id": 1,
                        "username": "username1",
                        "request_id": 3,
                        "request_status": "accepted",
                        "request_time": 123456789,
                        "is_sender": True,
                        "is_receiver": False
                        },
                    {
                        "user_id": 3,
                        "username": "username3",
                        "request_id": 2,
                        "request_status": "accepted",
                        "request_time": 12345678,
                        "is_sender": True,
                        "is_receiver": False
                        },
                    {
                        "user_id": 4,
                        "username": "username4",
                        "request_id": 5,
                        "request_status": "pending",
                        "request_time": 123456789,
                        "is_sender": False,
                        "is_receiver": True
                        },
                    ]
             }
            }

    return data

class TestUserModel:
    # Test for insertion, selection, and deletion of User model.
    # Adding a valid user to the users table. The table is empty, so the user is expected to have an id of 1
    # after being added to the database.
    # After successfully adding the new user, we delete that user.
    # Selection is already included in the User.delete() function, so we don't have to
    # create a test for it.
    def test_basic_commands(self, test_db):
        test_user = User(username="test1", email="test1@test.com", password_hash="password_hash_1")

        # Add the user to the database
        User.insert(test_user)

        assert test_user.id == User.get_last_user_id()

        # Delete the same user from the database
        deleted_user = User.delete(test_user.username)

        assert test_user.id == User.get_last_user_id() + 1
        assert deleted_user.id == test_user.id

        # deleted_user should be None, for it has already been deleted
        deleted_user = User.delete(test_user.username)
        assert deleted_user == None

    # Test adding a duplicated username
    # The test adds two users with duplicated username to users table. It is supposed to raise an Integrity Error
    def test_invalid_username(self, test_db):
        test_user1 = User(username="test", email="test1@test.com", password_hash="password_hash_1")
        test_user2 = User(username="test", email="test2@test.com", password_hash="password_hash_1")
        User.insert(test_user1)

        with pytest.raises(IntegrityError):
            assert User.insert(test_user2)

    # Test adding a duplicated email
    # The test adds two users with duplicated email to users table. It is supposed to raise an Integrity Error
    def test_invalid_email(self, test_db):
        test_user1 = User(username="test1", email="test@test.com", password_hash="password_hash_1")
        test_user2 = User(username="test2", email="test@test.com", password_hash="password_hash_1")
        User.insert(test_user1)

        with pytest.raises(IntegrityError):
            assert User.insert(test_user2)

    # Test Json
    # Add a new user to the database. Select that user using the username, then compare the to_json of both user
    def test_user_to_json(self, test_db):
        test_user = User(username="test1", email="test1@test.com", password_hash="password_hash_1")
        User.insert(test_user)
        test_data = {
            "id": User.get_last_user_id(),
            "username": "test1",
            "email": "test1@test.com",
            "password_hash": "password_hash_1"
        }
        assert json.loads(test_user.to_json()) == test_data

    def test_find_people(self, test_db, sampleUserData):
        # request send one time
        test_user = User(username="username4", email="email4@test.com", password_hash="pass_word_hash4")
        User.insert(test_user)

        test_people = User.find_people(2)

        assert test_people == sampleUserData["find_people_data"]["initial_data"]

        # request sended by user A was rejected, and user A send request again
        test_request = ConversationRequest.get_request_by_id(1)
        test_request.reject()
        new_test_request = ConversationRequest(
                initiator_id=1,
                receiver_id=2,
                request_time=123456789
                )
        ConversationRequest.insert(new_test_request)

        new_test_request.accept(123456799)

        test_people2 = User.find_people(2)

        assert test_people2 == sampleUserData["find_people_data"]["re_request_data"]

        # request send by user A was rejected, and user_id send request to user A
        new_test_request2 = ConversationRequest(
                initiator_id=4,
                receiver_id=2,
                request_time=12345678
                )
        ConversationRequest.insert(new_test_request2)

        new_test_request2.reject()

        re_request = ConversationRequest(
                initiator_id=2,
                receiver_id=4,
                request_time=123456789
                )
        ConversationRequest.insert(re_request)

        test_people3 = User.find_people(2)

        assert test_people3 == sampleUserData["find_people_data"]["re_request_by_user_id_data"]

