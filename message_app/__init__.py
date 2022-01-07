from flask import Flask, render_template, session, redirect, url_for
import os
from message_app.db.db import init_SQLAlchemy

# The function accepts a name as an argument. Leaving the name by default (app=Flask(__name__)) automatically
# includes the package name in the path for SQLALCHEMY_DATABASE_URI, which creates confusion when
# setting up the path for testing database.
def create_app(test_config=None, name=__name__):
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
        app.config.update(test_config)

    # Create a connection to the database
    with app.app_context():
        # Connect to the database using SQLAlchemy
        init_SQLAlchemy()

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
            return redirect(url_for("send_message.messages"))
        else:
            return render_template("index.html")

    return app
