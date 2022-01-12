import time
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Blueprint, render_template, session
from message_app.model import Messages, Conversations, User
from message_app.db.db import DB

send_messages = Blueprint("send_messages", __name__)
socketio = SocketIO(cors_allowed_origins='*')

# An interval that decides user's status (ACTIVE or AWAY)
# user's last_active_time < LAST_ACTIVE_INTERVAL means the user is active and vice versa
LAST_ACTIVE_INTERVAL = 10 * 60 * 1000 # 600000 milliseconds or 10 minutes

@send_messages.route("/messages", methods=["GET"])
def messages():
    # Get all conversations from an user
    current_user = session["user"]
    conversations = User.select(current_user).conversations
    available_conversations = []
    for conv in conversations:
        # receiver_name works for a group having only 2 people.
        # TODO: Implement receiver_name for a group having more than 2 people
        participants = conv.participants
        if participants[0].username == current_user:
            receiver_name = participants[1].username
            last_active_time = participants[1].last_active_time
        else:
            receiver_name = participants[0].username
            last_active_time = participants[0].last_active_time
        conv_id = conv.id

        # time.time() * 1000 because time function in Python returns time in seconds, while JS returns time in milliseconds
        status = "active" if (time.time() * 1000 - last_active_time < LAST_ACTIVE_INTERVAL) else "away"
        data = {
            "title": receiver_name,
            "receiver_name": receiver_name,
            # "last_active_time": last_active_time, # This key shows exact how long the user has been away
            "id": str(conv_id),
            "conversation_status": status
        }
        available_conversations.append(data)

    return render_template("messages.html", username=current_user, conversation_id=0, available_conversations=available_conversations)

# ================== Sockets for Conversations Container ==========================

# Joinning a conversation
@socketio.on("join", namespace="/messages")
def joining(data):
    username = data["username"]
    conversation_id = data["conversation_id"]

    join_room(conversation_id)

    # Send a message that inform new user has join the conversation
    emit("message_handler_client", {"username": username, "conversation_id": conversation_id, "join": True}, room=conversation_id)

# Leaving a conversation
@socketio.on("leave", namespace="/messages")
def leaving(data):
    username = data["username"]
    conversation_id = data["conversation_id"]
    leave_room(conversation_id)

    # Send a message that inform an user has left the conversation
    emit("message_handler_client", {"username": username, "conversation_id": conversation_id, "join": False}, room=conversation_id)

# Updating current_user's last_active_time
@socketio.on("last_active", namespace="/messages")
def last_active(data):
    username = data["username"]
    last_active_time = data["last_active_time"]
    current_user = User.select(username)
    current_user.last_active_time = last_active_time
    DB.session.commit()

# Updating other users' status (Only work for conversation of 2 users)
@socketio.on("update_conversations_container", namespace="/messages")
def update_conversations_container(conversations):
    for c in conversations:
        receiver = User.select(c["receiver_name"])
        new_status = "active" if time.time() * 1000 - receiver.last_active_time < LAST_ACTIVE_INTERVAL else "away"
        c["conversation_status"] = new_status
    emit("update_conversations_container", conversations)


# ================== Sockets for Messages Container ==========================

# A socket that checks if an user is typing
@socketio.on("typing", namespace="/messages")
def is_typing(data):
    emit("typing", data, broadcast=True, include_self=False)

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
    DB.session.commit()
    data["id"] = new_message.id

    emit("message_handler_client", data, room=conversation_id)
