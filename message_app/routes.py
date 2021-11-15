from hashlib import sha256
from message_app import app
from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import requests
import json
import os
import sqlite3
import re

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
        confirmPassword = params.get("confirmPassword", "")
        email = params.get("email", "")
        emailRegex = "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        
        # Verify email
        if re.fullmatch(emailRegex, email) is None:
            print("abcd")
            session["error"] = "Invalid Email. Please try a valid email."
            raise Exception(session["error"])

        # Verify password
        if password != confirmPassword:
            session["error"] = "Password doesn't not match. Please try again."
            raise Exception(session["error"])

        if username == "" or password == "":
            session["error"] = "Invalid username/password. Please try again."
            raise Exception(session["error"])

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
            raise Exception(session['error'])

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
        print(username, password)

        if username == "" or password == "":
            session["error"] = "Invalid username/password. Please try again."
            raise Exception(session["error"])

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
            raise Exception(session["error"])

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
            raise Exception(session["error"])

    except Exception as error:
        return {"Error": "Bad request. " + str(error)}, 400