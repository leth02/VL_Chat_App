from flask import Blueprint, request, session, redirect, url_for
from message_app.utils import hashing
from message_app.model import User
from hashlib import sha256

user_sign_up = Blueprint("user_sign_up", __name__)

@user_sign_up.route("/api/signup", methods=["POST"])
def api_user_signup():
    try:
        params = request.form
        username = params.get("username", "")
        password = params.get("password", "")
        email = params.get("email", "")

        if username == "" or password == "":
            session["error"] = "Invalid username/password. Please try again."
            return redirect(url_for("user_signup"))

        # Verify validity of the username
        user_data = User.select(username)
        if user_data is not None:
            # Username taken
            session["error"] = "Username has been taken. Please try a different username"
            return redirect(url_for("user_signup"))
        else:
            # Hash the password
            password, salt = hashing(password)
            new_user = User(username=username, email=email, password_hash=password, password_salt=salt)

            # Add user to the database
            User.insert(new_user)

        return redirect(url_for("index"))

    except Exception as error:
        return {"Error": "Bad request. " + str(error)}, 400