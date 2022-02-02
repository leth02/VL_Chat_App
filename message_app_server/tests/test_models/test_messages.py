import time
from message_app.model import Messages
import json

class TestMessagesModel:
    # Test for insertion, selection, and deletion of Messages model.
    # Adding a valid message to the messages table.
    # After successfully adding the new message, we delete that message.
    # Selection is already included in the Messages.delete() function, so we don't have to
    # create a test for it.
    def test_basic_commands(self, test_db):
        m = Messages(content="user3 sends a message to conversation2")

        # Add the message to the database
        Messages.insert(m)

        assert m.id == Messages.get_last_message_id()

        # Delete the same message from the database
        deleted_message = Messages.delete(m.id)

        assert m.id == Messages.get_last_message_id() + 1
        assert deleted_message.id == m.id

        # deleted_message should be None, for it has already been deleted
        deleted_user = Messages.delete(m.id)
        assert deleted_user == None

    # Test Json
    def test_message_to_json(self, test_db):
        m = Messages.select(1)
        test_data = {
            "id": 1,
            "sender_id": 1,
            "content": "user1 sends a message to conversation1",
            "conversation_id": 1
        }
        assert json.loads(m.to_json()) == test_data

    def test_get_messages(self, test_db):
        # test get one message without cursor
        messages = Messages.get_messages(1, 1, None)
        assert len(messages) == 1
        assert messages[0]["id"] == 2

        # test get 1 message with cursor
        messages = Messages.get_messages(1, 1, 1)
        assert len(messages) == 1
        assert messages[0]["id"] == 1

        # test get many messages
        messages = Messages.get_messages(1, 2, None)
        assert len(messages) == 2

