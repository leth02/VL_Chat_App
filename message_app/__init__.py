import os
from time import strftime

from flask import Flask, render_template, session, redirect, url_for, request

from .db.db import init_SQLAlchemy
from .send_message import socketio
# Import for real-time testing purpose and will be DELETED before deployment.
from .model import User, Messages, Conversations
from .utils import hash_pw
from .db.db import DB as db
from .logger import configure_logging, get_logger


log = get_logger(__name__)

# we configure the logging level and format
# configure_logging()


# The function accepts a name as an argument. Leaving the name by default (app=Flask(__name__)) automatically
# includes the package name in the path for SQLALCHEMY_DATABASE_URI, which creates confusion when
# setting up the path for testing database.
def create_app(test_config=None, name=__name__):
    log.info("Initialize message app")

    app = Flask(name)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.path.join("sqlite:///", "db", 'message_app_db.sqlite3'),

        # If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals.
        # The default is None, which enables tracking but issues a warning that it will
        # be disabled by default in the future. This requires extra memory and should be disabled if not needed.
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # if test config is passed, update app to use that config object
    if test_config:
        log.info("Process test config")
        app.config.update(test_config)

    # Create a connection to the database
    with app.app_context():
        # Connect to the database using SQLAlchemy
        log.info("Initialize database")
        init_SQLAlchemy()

        # ================Test Data=============================
        # Some data for real-time testing purpose and will be DELETED before deployment.
        # Delete the current database or comment out this part if there is any conflict
        # Uncomment this part for real-time testing
        if not test_config:
            try:
                # User
                password_hash_1 = hash_pw("1")
                password_hash_2 = hash_pw("2")
                password_hash_3 = hash_pw("3")
                user1 = User(username="user1", email="email11@test.com", password_hash=password_hash_1)
                user2 = User(username="user2", email="email22@test.com", password_hash=password_hash_2)
                user3 = User(username="user3", email="email33@test.com", password_hash=password_hash_3)
                User.insert(user1)
                User.insert(user2)
                User.insert(user3)

                # Conversations
                conv1 = Conversations()
                conv2 = Conversations()
                Conversations.insert(conv1)
                Conversations.insert(conv2)
                conv1.participants.append(user1)
                conv1.participants.append(user2)
                conv2.participants.append(user1)
                conv2.participants.append(user3)

                # Messages
                m1 = Messages(content="user1 sends a message to conversation1")
                Messages.insert(m1)
                m1.sender_id = user1.id
                conv1.messages.append(m1)

                m2 = Messages(content="user2 sends a message to conversation1")
                Messages.insert(m2)
                m2.sender_id = user2.id
                conv1.messages.append(m2)

                # An explicitly commit unlocks the database.
                db.session.commit()
            except:
                pass
        #===============END OF THE TEST DATA =================

        # SocketIO
        log.info("Initialize websocket")
        socketio.init_app(app)

    #================Registering Blueprints==================
    from . import request_message, user_sign_in, user_sign_up, send_message
    app.register_blueprint(request_message.request_messages)
    app.register_blueprint(user_sign_in.user_sign_in)
    app.register_blueprint(user_sign_up.user_sign_up)
    app.register_blueprint(send_message.send_messages)

    # ===== HTML Pages =====
    @app.route("/", methods=["GET"])
    def index():
        # If a session exists, redirect to message page
        if "user" in session:
            return redirect(url_for("send_messages.messages"))
        else:
            return render_template("index.html")

    @app.after_request
    def after_request(response):
        timestamp = strftime("[%Y-%b-%d %H:%M")
        log.info("{} {} {} {} {} {}".format(timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status))

        return response

    return app
