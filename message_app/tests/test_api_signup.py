import pytest
import requests
import json

def test_signup_wrong_confirm_password(supply_url):
    url = supply_url + "/signup"
    data = {
        "username": "nameA",
        "password": "testPassword",
        "confirmPassword": "WrongConfirmPassword",
        "email": "test@gmail.com"
    }
    resp = requests.post(url, data)
    j = json.loads(resp.text)
    assert resp.status_code == 400
    assert j['Error'] == "Bad request. Password doesn't not match. Please try again."

def test_signup_invalid_email(supply_url):
    url = supply_url + "/signup"
    data = {
        "username": "nameA",
        "password": "passwordA",
        "confirmPassword": "passwordB",
        "email": "invalidEmailAddress"
    }
    resp = requests.post(url, data)
    j = json.loads(resp.text)
    assert resp.status_code == 400
    assert j['Error'] == "Bad request. Invalid Email. Please try a valid email."

def test_signup_taken_username(supply_url):
    url = supply_url + "/signup"
    data = {
        "username": "long",
        "password": "testPassword",
        "confirmPassword": "testPassword",
        "email": "test@gmail.com"
    }
    resp = requests.post(url, data)
    j = json.loads(resp.text)
    assert resp.status_code == 400
    assert j['Error'] == "Bad request. Username has been taken. Please try another one."