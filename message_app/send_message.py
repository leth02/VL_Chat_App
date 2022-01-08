from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Blueprint, render_template, session, redirect, url_for
from message_app.model import Messages, Conversations, User

send_messages = Blueprint("send_messages", __name__)
socketio = SocketIO(cors_allowed_origins='*')

@send_messages.route("/messages", methods=["GET"])
def messages():
    # Info of all other users who accepted the conversation request of the current user
    user1 = User.select("1").username
    user2 = User.select("2").username
    user3 = User.select("3").username
    users = [user1, user2, user3]

    return render_template("messages.html", username=session["user"], conversation_id=None, users=users)

# An event for joinning a conversation
@socketio.on("join", namespace="/messages")
def joining(data):
    username = data["username"]
    conversation_id = data["conversation_id"]
    join_room(conversation_id)

    # Send a message that inform new user has join the conversation
    emit("message_handler", {"username": username, "message": " has join the conversation"}, room=conversation_id)

# An event for leaving a conversation
@socketio.on("leave", namespace="/messages")
def leaving(data):
    username = data["username"]
    conversation_id = data["conversation_id"]
    leave_room(conversation_id)

    # Send a message that inform an user has left the conversation
    emit("message_handler", {"username": username, "message": "has left the conversation"}, room=conversation_id)

# An event that handles sending/receiving messages
@socketio.on('message_handler', namespace="/messages")
def message_handler(data):
    username = data["username"]
    message = data["message"]
    conversation_id = data["conversation_id"]
    created_at = data["created_at"]

    # Store message to the database
    user_id = User.select(username).id
    Messages.insert(Messages(sender_id=user_id, content=message, created_at=created_at, conversation_id=conversation_id))

    emit("message_handler", {"username": username, "message": message}, room=conversation_id)
