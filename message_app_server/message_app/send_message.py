import os
import time
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Blueprint, render_template, session, request, jsonify
from message_app.model import Messages, Conversations, User
from message_app.db.db import DB
from PIL import Image

send_messages = Blueprint("send_messages", __name__)

# whitelist 'http://localhost:5000' to keep old WebSocket works. It will be deleted after we finish migrating
socketio = SocketIO(cors_allowed_origins=['http://localhost:3000', 'http://localhost:5000'])

# # Define the amount of time a user can be active/inactive on the frontend
# before we actually update their status on the server
LAST_ACTIVE_INTERVAL = 10 * 60 * 1000 # 600000 milliseconds or 10 minutes
IMAGE_STORAGE_PATH = os.path.join("message_app", "static", "user_images")
THUMBNAIL_MAX_SIZE = (100, 100)

@send_messages.route("/messages", methods=["GET"])
def messages():
    # Get conversations of the current user
    current_user = session["user"][1]
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

@send_messages.route("/api/get_message", methods=["POST"])
def api_get_message():
    # Get message using its id
    try:
        message_id = request.get_json(force=True)["messageID"]
        last_message = Messages.select(message_id)

        # Message not found:
        if not last_message:
            session["error"] = "Invalid message_id."
            raise Exception(session["error"])
        else:
            sender = User.select(user_id=last_message.sender_id)
            return_value = {
                "sender_name": sender.username,
                "content": last_message.content
            }
            return jsonify(return_value), 200

    except Exception as error:
        return {"Error": "Bad request. " + str(error)}, 400

@send_messages.route("/api/messages/get_ten_messages/<int:conversation_id>", methods=["GET"])
@send_messages.route("/api/messages/get_ten_messages/<int:conversation_id>/<int:cursor>", methods=["GET"])
def get_ten_messages(conversation_id, cursor=None):
    # query 11 messages starting from cursor. If numbers of messages return < 11,
    # there is no more message to fetch next time
    try:
        messages = Messages.getMessages(conversation_id, 11, cursor)
        messages_to_json = {}

        if len(messages) < 11:
            messages_to_json = {
                    "messages": messages,
                    "next_cursor": None
                    }
        else:
            messages_to_json = {
                    "messages": messages[0:(len(messages) - 1)],
                    "next_cursor": messages[len(messages) - 1]["id"]
                    }

        return jsonify(messages_to_json), 200

    except Exception as error:
        return {"Error": "Bad Request" + str(error)}, 400

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

# A socket that checks if a user is typing
@socketio.on("typing", namespace="/messages")
def is_typing(data):
    emit("typing", data, broadcast=True, include_self=False)

# A socket that handles sending/receiving messages
@socketio.on("message_handler_server", namespace="/messages")
def message_handler(data):
    # The data is a dictionary with six keys:
    # "username": The username of the sender
    # "message": The content of the message
    # "conversation_id": The current conversation's id
    # "timestamp": The time that user sent this image
    # "image": The image as a binary file. Value = None if the message doesn't have any attachment
    # "image_name": The name of the image. Value = "" if the message doesn't have any attachment
    username = data["username"]
    message = data["message"]
    conversation_id = data["conversation_id"]
    created_at = data["created_at"]
    attachment_name = ""
    image = None

    if ("image" in data.keys()):
        image_name = data["image_name"]
        image = data["image"]
        attachment_name = str(created_at) + username + image_name # Lower the chance of having duplicated image file
        image_path = os.path.join(IMAGE_STORAGE_PATH, "regular_" + attachment_name)
        # Store the regular image to the system
        with open(image_path, "wb") as f:
            f.write(image)

        # Resize the image
        resized_image = Image.open(image_path)
        resized_image.thumbnail(THUMBNAIL_MAX_SIZE)

        # Store resized version to the system
        resized_path = os.path.join(IMAGE_STORAGE_PATH, "thumbnail_" + attachment_name)
        resized_image.save(resized_path)

        image_data = {
            "regular_source": os.path.join("static", "user_images", "regular_" + attachment_name).replace("\\", "&#47;").replace(" ", "&#32;"), # Replace escape character with their codes
            "thumbnail_source": os.path.join("static", "user_images", "thumbnail_" + attachment_name).replace("\\", "&#47;").replace(" ", "&#32;"), # Replace escape character with their codes
            "width": resized_image.width,
            "height": resized_image.height,
        }

    # Update the database
    user_id = User.select(username).id
    conversation = Conversations.select(conversation_id)
    new_message = Messages(sender_id=user_id, content=message, created_at=created_at, conversation_id=conversation_id, attachment_name=attachment_name)
    Messages.insert(new_message)
    conversation.last_message_id = new_message.id # Manually set the last_message_id for now
    DB.session.commit()

    # Return data
    return_data = {
        "id": new_message.id,
        "conversation_id": conversation_id,
        "username": username,
        "message": message,
        "created_at": created_at
    }

    if image:
        return_data.update(image_data)

    emit("message_handler_client", return_data, room=conversation_id)

# A socket that updates user's last_active_time
@socketio.on("last_active", namespace="/messages")
def last_active(data):
    username = data["username"]
    last_active_time = data["last_active_time"]
    current_user = User.select(username)
    current_user.last_active_time = last_active_time
    DB.session.commit()
