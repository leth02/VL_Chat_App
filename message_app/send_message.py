from flask_socketio import SocketIO, emit
from flask import Blueprint, render_template

send_messages = Blueprint("send_messages", __name__)
socketio = SocketIO(cors_allowed_origins='*')

@send_messages.route("/messages", methods=["GET"])
def messages():
    return render_template("messages.html")

@socketio.on('message_handle', namespace="/messages")
def message_handle(msg):
    emit("message_handle", msg, broadcast=True)
