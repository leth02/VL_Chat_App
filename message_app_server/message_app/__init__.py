import os
from time import strftime
from flask import Flask, render_template, session, redirect, url_for, request
from flask_cors import CORS
from .db.db import init_SQLAlchemy
from .send_message import socketio
from .utils import hash_pw
from .db.db import DB as db
from .logger import configure_logging, get_logger


log = get_logger(__name__)


# The function accepts a name as an argument. Leaving the name by default (app=Flask(__name__)) automatically
# includes the package name in the path for SQLALCHEMY_DATABASE_URI, which creates confusion when
# setting up the path for testing database.
def create_app(test_config=None, name=__name__):
    log.info("Initialize message app")

    app = Flask(name)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.path.join("sqlite:///", "db", 'message_app_db.sqlite3'),
        CORS_HEADERS="Content_Type",

        # Disable tracking modification of objects which requires extra memory
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # if test config is passed, make app use that config object
    if test_config:
        log.info("Process test config")
        app.config.update(test_config)

    # Configure database and websocket
    with app.app_context():
        log.info("Initialize database")
        init_SQLAlchemy()

        log.info("Initialize websocket")
        socketio.init_app(app)

    # Register Blueprints
    from . import request_message, user_sign_in, user_sign_up, send_message
    app.register_blueprint(request_message.request_messages)
    app.register_blueprint(user_sign_in.user_sign_in)
    app.register_blueprint(user_sign_up.user_sign_up)
    app.register_blueprint(send_message.send_messages)

    @app.route("/", methods=["GET"])
    def index():
        if "user" in session:
            return redirect(url_for("send_messages.messages"))
        else:
            return render_template("index.html")

    # Imitatation of Flask logging
    # @app.after_request
    # def after_request(response):
    #     timestamp = strftime("[%Y-%b-%d %H:%M")
    #     log.info("{} {} {} {} {} {}".format(timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status))

    #     return response

    # Handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
    CORS(app)

    return app
