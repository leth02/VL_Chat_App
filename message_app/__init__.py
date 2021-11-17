import sys
import os
sys.path.append(os.getcwd())
from hashlib import sha256
from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from db import db
import re


def create_app(test_config=None):
	app = Flask(__name__)

	app.config.from_mapping(
		SECRET_KEY=b'\xb0\x9a\xc9\x05\x19\xafv\x88\xfaB\xe5$\x07\x12\x10\x9e'
	)

	# if test config is passed, update app to use that config object
	if test_config:
		app.config.update(test_config)

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
			emailRegex = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"

			# Verify email
			if re.fullmatch(emailRegex, email) is None:
				session["error"] = "Invalid Email. Please try a valid email."
				raise Exception(session["error"])

			# Verify password
			if password != confirmPassword:
				session["error"] = "Password doesn't not match. Please try again."
				raise Exception(session["error"])

			if username == "" or password == "":
				session["error"] = "Invalid username/password. Please try again."
				raise Exception(session["error"])

			# Connect and fetch data from the users table
			userData = db.query_db(
				"SELECT * FROM users WHERE username=:user_name",
				{'user_name': username},
				one=True
			)

			if userData:
				session["error"] = "Username has been taken. Please try another one."
				raise Exception(session['error'])

			# Hash the password
			salt = str(os.urandom(5))
			password += salt
			h = sha256()
			h.update(bytes(password, "utf8"))
			password = h.hexdigest()

			# Add user to the database
			db.query_db("INSERT INTO users VALUES (:username, :password, :salt, :email)",
				{"username": username, "password": password, "salt": salt, "email": email}
			)
			db.get_db().commit()

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
				raise Exception(session["error"])

			# Connect and fetch data from the users table
			userData = db.query_db(
				"SELECT password, salt FROM users WHERE username=:user_name",
				{'user_name': username},
				one=True
			)

			# User not found
			if not userData:
				session["error"] = "Invalid username/password. Please try again."
				raise Exception(session["error"])

			correctPassword = userData["password"]
			salt = userData["salt"]
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

	return app