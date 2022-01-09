from os import name
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Blueprint, render_template, session, redirect, url_for
from message_app.model import Messages, Conversations, User
from message_app.db.db import DB as db

send_messages = Blueprint("send_messages", __name__)
socketio = SocketIO(cors_allowed_origins='*')

@send_messages.route("/messages", methods=["GET"])
def messages():
    # Get all conversations from an user
    # TODO: Show other usernames instead of conversations' ids on the frontend
    current_user = session["user"]
    conversations = User.select(current_user).conversations
    return render_template("messages.html", username=current_user, conversation_id=0, conversations=conversations)

# An socket for joinning a conversation
@socketio.on("join", namespace="/messages")
def joining(data):
    username = data["username"]
    conversation_id = data["conversation_id"]

    join_room(conversation_id)

    # Send a message that inform new user has join the conversation
    emit("message_handler_client", {"username": username, "conversation_id": conversation_id, "join": True}, room=conversation_id)

# A socket for leaving a conversation
@socketio.on("leave", namespace="/messages")
def leaving(data):
    username = data["username"]
    conversation_id = data["conversation_id"]
    leave_room(conversation_id)

    # Send a message that inform an user has left the conversation
    emit("message_handler_client", {"username": username, "conversation_id": conversation_id, "join": False}, room=conversation_id)

# A socket that checks if an user is typing
@socketio.on("typing", namespace="/messages")
def is_typing(data):
    emit("typing", {"username": data["username"]}, broadcast=True, include_self=False)

# A socket that handles sending/receiving messages
@socketio.on("message_handler_server", namespace="/messages")
def message_handler(data):
    username = data["username"]
    message = data["message"]
    conversation_id = data["conversation_id"]
    created_at = data["created_at"]

    # Update the database
    user_id = User.select(username).id
    conversation = Conversations.select(conversation_id)
    new_message = Messages(sender_id=user_id, content=message, created_at=created_at, conversation_id=conversation_id)
    Messages.insert(new_message)
    conversation.last_message_id = new_message.id # Manually set the last_message_id for now
    db.session.commit()
    data["id"] = new_message.id

    emit("message_handler_client", data, room=conversation_id)
