import pytest
import json
from message_app.db.db import query_db

# test sending request successfully
@pytest.mark.parametrize(("sender_id", "receiver_id", "request_time", "status_code", "response_message"), (
    (1000, 1002, 123456, 200, b'Success'),
    ))
def test_sending_request(test_client, app, sender_id, receiver_id, request_time, status_code, response_message):

    response = test_client.post(f"/api/request/send/{sender_id}/{receiver_id}/{request_time}")
    assert response.status_code == status_code
    assert response.data == response_message

    with app.app_context():
        assert query_db(
            "select * from conversation_request where initiator_id=:sender_id and receiver_id=:receiver_id",
            {"sender_id": sender_id, "receiver_id": receiver_id},
            one=True
            ) is not None

# test sending request fail
@pytest.mark.parametrize(("sender_id", "receiver_id", "request_time", "status_code", "response_message"), (
    (1000, 1001, 123456, 400, b'{"Error":"Bad Request.Request has already been sent"}\n'),
    (1001, 1005, 123456, 400, b'{"Error":"Bad Request.FOREIGN KEY constraint failed"}\n')
    ))
def test_sending_request_fail(test_client, app, sender_id, receiver_id, request_time, status_code, response_message):

    response = test_client.post(f"/api/request/send/{sender_id}/{receiver_id}/{request_time}")
    assert response.status_code == status_code
    assert response.data == response_message

# test accepting request successfully
def test_accepting_request(test_client, app):
    response = test_client.post("/api/request/accept/1001/123456")
    assert response.status_code == 200
    assert response.data == b'Success'

    with app.app_context():
        assert query_db(
                "select * from conversation_request where id=:request_id",
                {"request_id": 1001},
                one=True
                )["accepted"] == 1

# test accepting request fail
def test_accepting_request_fail(test_client, app):
    response = test_client.post("/api/request/accept/1002/123456")
    assert response.status_code == 400
    assert response.data == b'{"Error":"Bad Request.No request found"}\n'

# test reject request successfully
def test_rejecting_request(test_client, app):
    response = test_client.post("/api/request/reject/1001")
    assert response.status_code == 200
    assert response.data == b'Success'

    with app.app_context():
        assert query_db(
                "select * from conversation_request where id=:request_id",
                {"request_id": 1001},
                one=True
                )["accepted"] == 0

# test rejecting request fail
def test_rejecting_request_fail(test_client, app):
    response = test_client.post("/api/request/reject/1002")
    assert response.status_code == 400
    assert response.data == b'{"Error":"Bad Request.No request found"}\n'

#test get all requests successfully
@pytest.mark.parametrize(("user_id", "status_code"), (
    (1000, 200),
    (1001, 200),
    (1002, 200)
    ))
def test_get_all_requests(test_client, app, user_id, status_code):
    response = test_client.get(f"/api/request/all/{user_id}")
    assert response.status_code == status_code
    data_retrieved = json.loads(response.data.decode('utf8'))

    with app.app_context():
        assert query_db(
                "select * from conversation_request where receiver_id=:user_id and accepted=0",
                {"user_id": user_id}
                ) == data_retrieved

#test get all requests successfully
@pytest.mark.parametrize(("user_id", "status_code", "response_message"), (
    (1004, 400, b'{"Error":"Bad Request.No user found"}\n'),
    (1005, 400, b'{"Error":"Bad Request.No user found"}\n'),
    (1006, 400, b'{"Error":"Bad Request.No user found"}\n')
    ))
def test_get_all_requests_fail(test_client, app, user_id, status_code, response_message):
    response = test_client.get(f"/api/request/all/{user_id}")
    assert response.status_code == status_code
    assert response.data == response_message

