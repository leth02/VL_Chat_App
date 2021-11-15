from flask import Blueprint, request, session, redirect, url_for
from message_app.model import User
from hashlib import sha256

from message_app.utils import hashing

user_sign_in = Blueprint("user_sign_in", __name__)

@user_sign_in.route("/api/signin", methods=["POST"])
def api_user_signin():
    try:
        params = request.form
        username = params.get("username", "")
        input_password = params.get("password", "")

        if username == "" or input_password == "":
            session["error"] = "Invalid login credentials. Please try again."
            return redirect(url_for("user_signin"))

        # Connect and fetch data from the users table
        user_data = User.select(username)

        # User not found
        if not user_data:
            session["error"] = "Invalid login credentials. Please try again."
            return redirect(url_for("user_signin"))

        user_password = user_data.password_hash
        salt = user_data.password_salt

        # Hash the password
        password = hashing(input_password, salt).password_hash

        if password == user_password:
            return redirect(url_for("messages"))
        else:
            session["error"] = "Invalid login credentials. Please try again."
            return redirect(url_for("user_signin"))

    except Exception as error:
        return {"Error": "Bad request. " + str(error)}, 400

