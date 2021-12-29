from flask import Blueprint, request, session, redirect, url_for
from message_app.utils import hashing
from message_app.model import User
<<<<<<< HEAD
import re
=======
>>>>>>> 6847dd4a1d06c917fff9a2d9e4caf1b6048d27ba

user_sign_up = Blueprint("user_sign_up", __name__)

@user_sign_up.route("/api/signup", methods=["POST"])
def api_user_signup():
    try:
        params = request.form
        username = params.get("username", "")
        password = params.get("password", "")
        confirmPassword = params.get("confirmPassword", "")
        email = params.get("email", "")

        # Verify password
        if password != confirmPassword:
            session["error"] = "Password does not match. Please try again."
            raise Exception(session["error"])

        # Verify username
        user_data = User.select(username)
        if user_data is not None:
            # Username taken
            session["error"] = "Username has been taken. Please try a different username."
            raise Exception(session["error"])
        else:
            # Hash the password
            password, salt = hashing(password)
            new_user = User(username=username, email=email, password_hash=password, password_salt=salt)

            # Add user to the database
            User.insert(new_user)

            # Create a session for this user
            session["user"] = username

        return redirect(url_for("index"))

    except Exception as error:
        return {"Error": "Bad request. " + str(error)}, 400
