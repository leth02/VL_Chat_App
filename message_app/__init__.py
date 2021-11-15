from flask import Flask
from config import KEY


def create_app(test_config=None):
    app = Flask(__name__)

    # if test config is passed, update app to use that config object
    if test_config:
        app.config.update(test_config)

    return app

app = create_app(
    {'SECRET_KEY' : KEY}
)

from message_app import routes