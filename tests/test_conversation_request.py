import pytest
from message_app.model import *
from sqlalchemy.exc import IntegrityError
import json

class TestConversationRequestModel:
    # Test insert new conversation request to database
    def test_insert(self, test_db):
        test_request = ConversationRequest(
                initiator_id=1,
                receiver_id=3,
                request_time=12345678
                )

        # Add the request to the database
        ConversationRequest.insert(test_request)
        last_request = ConversationRequest.query.order_by(ConversationRequest.id.desc()).first()

        assert test_request.id == last_request.id

    # Test insert new conversation request without request_time -> raise error
    def test_no_request_time(self, test_db):
        test_request = ConversationRequest(
                initiator_id=1,
                receiver_id=3,
                )

        with pytest.raises(IntegrityError):
            assert ConversationRequest.insert(test_request)

    # Test convert request to json
    def test_request_to_json(self, test_db):
        test_request = ConversationRequest(
                initiator_id=1,
                receiver_id=3,
                request_time=12345678
                )
        ConversationRequest.insert(test_request)

        last_request = ConversationRequest.query.order_by(ConversationRequest.id.desc()).first()
        test_data = {
            "id": last_request.id,
            "initiator_id": last_request.initiator_id,
            "receiver_id": last_request.receiver_id,
            "accepted": last_request.accepted,
            "request_time": last_request.request_time,
            "accepted_time": last_request.accepted_time
        }
        assert json.loads(test_request.to_json()) == test_data

    # Test get all conversation requests of a specific users
    def test_get_all_requests(self, test_db):
        test_receiver = User.select("username2")
        test_initiator = User.select("username1")
        test_requests = ConversationRequest.get_all_requests(test_receiver.id)

        test_data = [{
            "id": 1,
            "initiator_id": test_initiator.id,
            "receiver_id": test_receiver.id,
            "accepted": 0,
            "request_time": 12345678,
            "accepted_time": None
            }]

        assert test_requests == test_data

    # test get request with specific initiator and receiver
    def test_get_request_by_users(self, test_db):
        test_receiver = User.select("username2")
        test_initiator = User.select("username1")
        test_request = ConversationRequest.get_request_by_users(test_initiator.id, test_receiver.id)

        assert test_request.id == 1

        # no request found -> return None
        test_request2 = ConversationRequest.get_request_by_users(1000, 10001)

        assert test_request2 == None

    # test get request by id
    def test_get_request_by_id(self, test_db):
        test_request = ConversationRequest.get_request_by_id(1)
        assert test_request.id == 1
        assert test_request.initiator_id == 1
        assert test_request.receiver_id == 2

        # no request found -> return None
        test_request2 = ConversationRequest.get_request_by_id(1000)
        assert test_request2 == None

    # test accept conversation request
    def test_accept(self, test_db):
        test_request = ConversationRequest.get_request_by_id(1)
        ConversationRequest.accept(test_request, 1234566789)

        assert test_request.accepted == 1

    # test reject conversation request
    def test_reject(self, test_db):
        test_request = ConversationRequest.get_request_by_id(1)
        ConversationRequest.reject(test_request)

        assert test_request.accepted == 2

