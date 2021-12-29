import pytest
from message_app.model import User
from sqlalchemy.exc import IntegrityError
import json

class TestUserModel:
    # Test for insertion, selection, and deletion of User model.
    # Adding a valid user to the users table. The table is empty, so the user is expected to have an id of 1
    # after being added to the database.
    # After successfully adding the new user, we delete that user.
    # Selection is already included in the User.delete() function, so we don't have to
    # create a test for it.
    def test_basic_commands(self, test_db):
        test_user = User(username="test1", email="test1@test.com", password_hash="password_hash_1", password_salt="password_salt_1")

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
        test_user1 = User(username="test", email="test1@test.com", password_hash="password_hash_1", password_salt="password_salt_1")
        test_user2 = User(username="test", email="test2@test.com", password_hash="password_hash_1", password_salt="password_salt_1")
        User.insert(test_user1)

        with pytest.raises(IntegrityError):
            assert User.insert(test_user2)

    # Test adding a duplicated email
    # The test adds two users with duplicated email to users table. It is supposed to raise an Integrity Error
    def test_invalid_email(self, test_db):
        test_user1 = User(username="test1", email="test@test.com", password_hash="password_hash_1", password_salt="password_salt_1")
        test_user2 = User(username="test2", email="test@test.com", password_hash="password_hash_1", password_salt="password_salt_1")
        User.insert(test_user1)

        with pytest.raises(IntegrityError):
            assert User.insert(test_user2)

    # Test Json
    # Add a new user to the database. Select that user using the username, then compare the to_json of both user
    def test_user_to_json(self, test_db):
        test_user = User(username="test1", email="test1@test.com", password_hash="password_hash_1", password_salt="password_salt_1")
        User.insert(test_user)
        test_data = {
            "id": User.get_last_user_id(),
            "username": "test1",
            "email": "test1@test.com",
            "password_hash": "password_hash_1",
            "password_salt": "password_salt_1"
        }
        assert json.loads(test_user.to_json()) == test_data
