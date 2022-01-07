from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Blueprint, render_template, session, redirect, url_for

send_messages = Blueprint("send_messages", __name__)
socketio = SocketIO(cors_allowed_origins='*')

@send_messages.route("/messages", methods=["GET"])
def messages():
    # data = {
    #     "username": session["username"]
    # }
    return render_template("messages.html", username=session["user"], conversation_id="test_conversation")

@socketio.on("join", namespace="/messages")
def joining(data):
    # User join a conversation

    username = data["username"]
    conversation_id = data["conversation_id"]
    join_room(conversation_id)

    # Send a message that inform new user has join the conversation
    emit("message_handler", {"message": username + " has join the conversation"}, room=conversation_id)

@socketio.on("leave", namespace="/messages")
def leaving(data):
    # User leave a conversation
    username = data["username"]
    conversation_id = data["conversation_id"]
    leave_room(conversation_id)

    # Send a message that inform an user has left the conversation
    emit("message_handler", {"message": username + "has left the conversation"})

@socketio.on('message_handler', namespace="/messages")
def message_handler(data):
    username = data["username"]
    message = data["message"]
    conversation_id = data["conversation_id"]
    emit("message_handler", {"username": username, "message": message}, room=conversation_id)
