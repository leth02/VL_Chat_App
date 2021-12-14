from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import requests
import json
import os
from message_app.db.db import get_db_SQLAlchemy

# The function accepts a name as an argument. Leaving the name by default (app=Flask(__name__)) automatically
# includes the package name in the path for SQLALCHEMY_DATABASE_URI, which creates confusion when
# setting up the path for testing database.
def create_app(test_config=None, name=__name__):
    app = Flask(name)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join("message_app", "db", 'message_app_db.sqlite3'), # This line is for the old use of our database. It will be removed after we change everything to SQLAlchemy.
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
        get_db_SQLAlchemy()

        # Connect to the database using sqlite3.connect()
        from message_app.db import db
        db.init_app(app)

    # ===== HTML Pages =====
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")


    @app.route("/messages", methods=["GET"])
    def messages():
        return render_template("messages.html")


    @app.route("/signup", methods=["GET"])
    def user_signup():
        return render_template("user_signup.html")


    @app.route("/signin", methods=["GET"])
    def user_signin():
        return render_template("user_signin.html")


    # ===== JSON API endpoints =====

    @app.route("/api/signup", methods=["GET"])
    def api_user_signup():
        try:
            params = request.form
            username = params.get("username", "")
            password = params.get("password", "")

            if username == "" or password == "":
                session["error"] = "Invalid username/password. Please try again."
                return redirect(url_for("user_signup"))

            # TODO connect to SQLite database and create a new account with the provided credentials
            # if successful, redirect user to the app page
            # otherwise, return JSON response containing the error

        except Exception as error:
            return {"Error": "Bad request. " + str(error)}, 400


    @app.route("/api/signin", methods=["POST"])
    def api_user_signin():
        try:
            params = request.form
            username = params.get("username", "")
            password = params.get("password", "")

            if username == "" or password == "":
                session["error"] = "Invalid username/password. Please try again."
                return redirect(url_for("user_signup"))

            # TODO connect to SQLite database and validate the provided credentials
            # if successful, redirect user to the app page
            # otherwise, return JSON response containing the error of invalid credentials

        except Exception as error:
            return {"Error": "Bad request. " + str(error)}, 400

    return app