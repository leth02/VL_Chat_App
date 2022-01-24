import pytest

@pytest.fixture
def sampleSignUpData():
    data = {
        "valid": {
            "username": "validUserName1",
            "password": "validPassword1",
            "confirmPassword": "validPassword1",
            "email": "validEmail@test.com"
        },
        "invalid": {
            "wrong_confirm_password": {
                "password": "wrongConfirmPassword",
                "confirmPassword": "",
                "email": "wrongConfirmPassword@gmail.com"
            },
            "taken_username": {
                "username": "username1",
                "password": "takenUserName",
                "confirmPassword": "takenUserName",
                "email": "takenUserName@gmail.com"
            }
        }
    }
    return data

class TestAPISignUp:
    def test_signup_wrong_confirm_password(self, sampleSignUpData, test_db, test_client):
        resp = test_client.post('/api/signup', data=sampleSignUpData["invalid"]["wrong_confirm_password"])
        assert resp.json["Error"] == "Bad request. Password does not match. Please try again."
        assert resp.status_code == 400

    def test_signup_taken_username(self, sampleSignUpData, test_db, test_client):
        resp = test_client.post('/api/signup', data=sampleSignUpData["invalid"]["taken_username"])
        assert resp.json["Error"] == "Bad request. Username has been taken. Please try a different username."
        assert resp.status_code == 400

    def test_valid_signup(self, sampleSignUpData, test_db, test_client):
        resp = test_client.post('/api/signup', data=sampleSignUpData["valid"])
        assert resp.status_code == 200
