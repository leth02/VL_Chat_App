import pytest
import json
from message_app.db import query_db

# test sending request successfully
@pytest.mark.parametrize(("sender_id", "receiver_id", "status_code", "response_message"), (
    (1, 3, 200, b'Success'),
    ))
def test_sending_request(client, app, sender_id, receiver_id, status_code, response_message):

    response = client.post(f"/api/request/send/{sender_id}/{receiver_id}")
    assert response.status_code == status_code
    assert response.data == response_message

    with app.app_context():
        assert query_db(
            "select * from requests where sender_id=:sender_id and receiver_id=:receiver_id",
            {"sender_id": sender_id, "receiver_id": receiver_id},
            one=True
            ) is not None

# test sending request fail
@pytest.mark.parametrize(("sender_id", "receiver_id", "status_code", "response_message"), (
    (1, 2, 400, b'{"Error":"Bad Request.Request has already been sent"}\n'),
    (4, 5, 400, b'{"Error":"Bad Request.FOREIGN KEY constraint failed"}\n')
    ))
def test_sending_request_fail(client, app, sender_id, receiver_id, status_code, response_message):

    response = client.post(f"/api/request/send/{sender_id}/{receiver_id}")
    assert response.status_code == status_code
    assert response.data == response_message

# test accepting request successfully
def test_accepting_request(client, app):
    response = client.post("/api/request/accept/1")
    assert response.status_code == 200
    assert response.data == b'Success'

    with app.app_context():
        assert query_db(
                "select * from requests where id=:request_id",
                {"request_id": 1},
                one=True
                )["accepted"] == 1

# test accepting request fail
def test_accepting_request_fail(client, app):
    response = client.post("/api/request/reject/2")
    assert response.status_code == 400
    assert response.data == b'{"Error":"Bad Request.No request found"}\n'

# test reject request successfully
def test_rejecting_request(client, app):
    response = client.post("/api/request/reject/1")
    assert response.status_code == 200
    assert response.data == b'Success'

    with app.app_context():
        assert query_db(
                "select * from requests where id=:request_id",
                {"request_id": 1},
                one=True
                ) is None

# test rejecting request fail
def test_rejecting_request_fail(client, app):
    response = client.post("/api/request/reject/2")
    assert response.status_code == 400
    assert response.data == b'{"Error":"Bad Request.No request found"}\n'

#test get all requests successfully
@pytest.mark.parametrize(("user_id", "status_code"), (
    (1, 200),
    (2, 200),
    (3, 200)
    ))
def test_get_all_requests(client, app, user_id, status_code):
    response = client.get(f"/api/request/all/{user_id}")
    assert response.status_code == status_code
    data_retrieved = json.loads(response.data.decode('utf8'))

    with app.app_context():
        assert query_db(
                "select * from requests where receiver_id=:user_id and accepted=0",
                {"user_id": user_id}
                ) == data_retrieved

#test get all requests successfully
@pytest.mark.parametrize(("user_id", "status_code", "response_message"), (
    (4, 400, b'{"Error":"Bad Request.No user found"}\n'),
    (5, 400, b'{"Error":"Bad Request.No user found"}\n'),
    (6, 400, b'{"Error":"Bad Request.No user found"}\n')
    ))
def test_get_all_requests_fail(client, app, user_id, status_code, response_message):
    response = client.get(f"/api/request/all/{user_id}")
    assert response.status_code == status_code
    assert response.data == response_message

