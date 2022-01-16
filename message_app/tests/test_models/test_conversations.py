import pytest
from message_app.model import Conversations
from sqlalchemy.exc import IntegrityError
import json

class TestUserModel:
    # Test for insertion, selection, and deletion of Conversations model.
    # Adding a valid conversation to the conversations table. The table is empty, so the conversation is expected to have an id of 1
    # after being added to the database.
    # After successfully adding the new conversation, we delete that conversation.
    # Selection is already included in the Conversations.delete() function, so we don't have to
    # create a test for it.
    def test_basic_commands(self, test_db):
        conv3 = Conversations()

        # Add the conversation to the database
        Conversations.insert(conv3)

        assert conv3.id == Conversations.get_last_conversation_id()

        # Delete the same conversation from the database
        deleted_conv = Conversations.delete(conv3.id)

        assert conv3.id == Conversations.get_last_conversation_id() + 1
        assert deleted_conv.id == conv3.id

        # deleted_conv should be None, for it has already been deleted
        deleted_conv = Conversations.delete(conv3.id)
        assert deleted_conv == None


    # Test Json
    def test_conversation_to_json(self, test_db):
        conv = Conversations.select(1)
        test_data = {
            "id": 1
        }
        assert json.loads(conv.to_json()) == test_data
