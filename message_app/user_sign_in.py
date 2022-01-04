from flask import Blueprint, request, session, redirect, url_for
from message_app.model import User
from message_app.utils import check_pw

user_sign_in = Blueprint("user_sign_in", __name__)

@user_sign_in.route("/api/signin", methods=["POST"])
def api_user_signin():
    try:
        params = request.form
        username = params.get("username", "")
        user_password_input = params.get("password", "")

        if username == "" or user_password_input == "":
            session["error"] = "Invalid login credentials. Please try again."
            raise Exception(session["error"])

        # Connect and fetch data from the users table
        user_data = User.select(username)

        # User not found
        if not user_data:
            session["error"] = "Invalid login credentials. Please try again."
            raise Exception(session["error"])

        user_password_hash = user_data.password_hash

        if check_pw(user_password_input, user_password_hash):
            session["user"] = username
            return redirect(url_for("messages"))
        else:
            session["error"] = "Invalid login credentials. Please try again."
            raise Exception(session["error"])

    except Exception as error:
        return {"Error": "Bad request. " + str(error)}, 400
