from hashlib import sha256
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
        DATABASE=os.path.join("message_app", "db", 'message_app_db.sqlite3'), # This line is for the old use of our database. It WILL BE REMOVED after we change everything to SQLAlchemy.
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

    #================Registering Blueprints==================
    from . import request_message
    app.register_blueprint(request_message.request_messages)

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


    @app.route("/signin", methods=["GET", "POST"])
    def user_signin():
        return render_template("user_signin.html")

    # ===== JSON API endpoints =====

    @app.route("/api/signup", methods=["POST"])
    def api_user_signup():
        try:
            params = request.form
            username = params.get("username", "")
            password = params.get("password", "")
            email = params.get("email", "")

            if username == "" or password == "":
                session["error"] = "Invalid username/password. Please try again."
                return redirect(url_for("user_signup"))

            # Connect to the db
            db_name = "VL_MESSAGES.db"
            conn = sqlite3.connect(db_name)
            c = conn.cursor()

            # Create table users if not exist
            c.execute("""CREATE TABLE IF NOT EXISTS users (
                username text NOT NULL PRIMARY KEY,
                password text NOT NULL,
                salt text,
                email text
                )"""
            )

            #  Verify whether username is taken or not
            c.execute("SELECT * FROM users WHERE username=:user_name", {'user_name': username})
            userData = c.fetchone()
            if userData:
                session["error"] = "Username has been taken. Please try another one."
                return redirect(url_for("user_signup"))

            # Hash the password
            salt = os.urandom(5)
            password += str(salt)
            h = sha256()
            h.update(bytes(password, "utf8"))
            password = h.hexdigest()

            # Add user to the database
            c.execute(f"INSERT INTO users VALUES (:username, :password, :salt, :email)", {"username": username, "password": password, "salt": salt, "email": email})
            conn.commit()
            c.close()

            return redirect(url_for("index"))

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

            # Connect and fetch data from the users table
            db_name = "VL_MESSAGES.db"
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
            with conn:
                c.execute("SELECT password, salt FROM users WHERE username=:user_name", {'user_name': username})
                userData = c.fetchone()
            c.close()

            # User not found
            if not userData:
                session["error"] = "Invalid username/password. Please try again."
                return redirect(url_for("user_signup"))

            correctPassword = userData[0]
            salt = userData[1]
            password = password + str(salt)

            # Hash the password
            h = sha256()
            h.update(bytes(password, "utf8"))
            password = h.hexdigest()

            if password == correctPassword:
                return redirect(url_for("index"))
            else:
                session["error"] = "Invalid username/password. Please try again."
                return redirect(url_for("user_signup"))

        except Exception as error:
            return {"Error": "Bad request. " + str(error)}, 400

    return app
