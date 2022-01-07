from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Blueprint, render_template, session, redirect, url_for

send_messages = Blueprint("send_messages", __name__, url_prefix="/messages")
socketio = SocketIO(cors_allowed_origins='*')

@send_messages.route("/", methods=["GET"])
def messages():
    if "user" not in session:
        return redirect(url_for("user_sign_in.user_signin"))
    else:
        data = {
            "username": session["username"]
        }
        return render_template("messages.html", username=session["username"])

@socketio.on('message_handle', namespace="/messages")
def message_handle(data):
    emit("message_handle", data, broadcast=True)
