import pytest
import json

class TestApiSendingRequest:
    # test sending request successfully
    @pytest.mark.parametrize(("sender_id", "receiver_id", "request_time", "status_code", "response_message"), (
        (2, 3, 123456, 200, b'Success'),
        ))
    def test_sending_request(self, test_client, test_db, sender_id, receiver_id, request_time, status_code, response_message):

        response = test_client.post(f"/api/request/send/{sender_id}/{receiver_id}/{request_time}")
        assert response.status_code == status_code
        assert response.data == response_message

    # test sending request fail
    def test_sending_request_fail(self, test_client, test_db):

        response = test_client.post(f"/api/request/send/1/2/123456")
        assert response.status_code == 400
        assert response.data == b'{"Error":"Bad Request.Request has already been sent"}\n'

    # test accepting request successfully
    def test_accepting_request(self, test_client, test_db):
        response = test_client.post("/api/request/accept/1/2/123456")
        assert response.status_code == 200
        assert response.data == b'Success'


    # test accepting request fail
    def test_accepting_request_fail(self, test_client, test_db):
        response = test_client.post("/api/request/accept/1002/1003/123456")
        assert response.status_code == 400
        assert response.data == b'{"Error":"Bad Request.No request found"}\n'

    # test reject request successfully
    def test_rejecting_request(self, test_client, test_db):
        response = test_client.post("/api/request/reject/1/2")
        assert response.status_code == 200
        assert response.data == b'Success'

    # test cancel request successfully
    def test_canceling_request(self, test_client, test_db):
        response = test_client.post("/api/request/cancel/1/2")
        assert response.status_code == 200
        assert response.data == b'Success'

    #test get all requests successfully
    @pytest.mark.parametrize(("user_id", "status_code", "result_length"), (
        (2, 200, 1),
        (3, 200, 0)
        ))
    def test_get_all_requests(self, test_client, test_db, user_id, status_code, result_length):
        response = test_client.get(f"/api/request/all/{user_id}")
        assert response.status_code == status_code
        data_retrieved = json.loads(response.data.decode('utf8'))
        assert len(data_retrieved) == result_length

    #test get all requests successfully
    @pytest.mark.parametrize(("user_id", "status_code", "response_message"), (
        (1004, 400, b'{"Error":"Bad Request.No user found"}\n'),
        (1005, 400, b'{"Error":"Bad Request.No user found"}\n'),
        (1006, 400, b'{"Error":"Bad Request.No user found"}\n')
        ))
    def test_get_all_requests_fail(self, test_client, test_db, user_id, status_code, response_message):
        response = test_client.get(f"/api/request/all/{user_id}")
        assert response.status_code == status_code
        assert response.data == response_message

    # test get all people api
    def test_get_people(self, test_client, test_db):
        response = test_client.get("/api/request/get_people/2")
        assert response.status_code == 200
        assert len(json.loads(response.data)) == 2

