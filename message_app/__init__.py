from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import requests
import json
import os


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, "db", 'message_app_db.sqlite3'),
    )

    # if test config is passed, update app to use that config object
    if test_config:
        app.config.update(test_config)

    # connect to the database
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