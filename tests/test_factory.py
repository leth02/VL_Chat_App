from message_app import create_app

def test_config():
    assert not create_app().testing
    assert create_app(__name__, {'TESTING': True}).testing
