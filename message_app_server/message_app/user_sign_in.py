from flask import Blueprint, jsonify, request, session, redirect, url_for, render_template
from message_app.model import User
from message_app.utils import check_pw

user_sign_in = Blueprint("user_sign_in", __name__)

@user_sign_in.route("/signin", methods=["GET"])
def user_signin():
    # If a session exists, redirect to message page
    if "user" in session:
        return redirect(url_for("send_messages.messages"))
    else:
        return render_template("user_signin.html")

@user_sign_in.route("/api/signin", methods=["POST"])
def api_user_signin():
    try:
        params = request.get_json(force=True)
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
            session["user"] = (user_data.id, username)
            payload = {
                "status": "Successful",
                "sessionCookie": "",
                "currentUserID": user_data.id
            }
            return jsonify(payload), 200
        else:
            session["error"] = "Invalid login credentials. Please try again."
            raise Exception(session["error"])

    except Exception as error:
        return jsonify({"error": "Bad request. " + str(error)}), 400


@user_sign_in.route('/api/logout', methods=["POST"])
def api_user_logout():
    session.clear()

    return redirect(url_for("user_sign_in.user_signin"))