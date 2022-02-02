import mimetypes
import os
import time
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Blueprint, session, request, jsonify, send_from_directory
from message_app.model import Messages, Conversations, User
from message_app.db.db import DB
from PIL import Image

send_messages = Blueprint("send_messages", __name__)

# whitelist 'http://localhost:5000' to keep old WebSocket works. It will be deleted after we finish migrating
socketio = SocketIO(cors_allowed_origins=['http://localhost:3000', 'http://localhost:5000'])

# # Define the amount of time a user can be active/inactive on the frontend
# before we actually update their status on the server
LAST_ACTIVE_INTERVAL = 10 * 60 * 1000 # 600000 milliseconds or 10 minutes
IMAGE_STORAGE_PATH = os.path.join("message_app", "user_images_storage")
THUMBNAIL_MAX_SIZE = (100, 100)

@send_messages.route("/api/get_image/<string:image_name>", methods=["GET"])
def api_get_image(image_name):
    return send_from_directory("user_images_storage", image_name)

@send_messages.route("/api/get_conversations/<int:user_id>", methods=["GET"])
def api_get_conversations(user_id):
    # Get conversations of the current user
    current_user = User.select(user_id=user_id)
    conversations = current_user.conversations
    available_conversations = []
    for conv in conversations:
        # receiver_name works for a group having only 2 people.
        # TODO: Implement receiver_name for a group having more than 2 people
        participants = conv.participants
        if participants[0].username == current_user.username:
            receiver_name = participants[1].username
            last_active_time = participants[1].last_active_time
        else:
            receiver_name = participants[0].username
            last_active_time = participants[0].last_active_time
        conv_id = conv.id

        status = "active" if (time.time() * 1000 - last_active_time < LAST_ACTIVE_INTERVAL) else "away"
        payload = {
            "lastMessageID": conv.last_message_id,
            "otherParticipantStatus": status,
            "conversationTitle": receiver_name,
            "conversationID": str(conv_id)
        }
        available_conversations.append(payload)

    return jsonify({"conversations": available_conversations}), 200

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
            payload = {
                "sender_name": sender.username,
                "content": last_message.content
            }
            return jsonify(payload), 200

    except Exception as error:
        return {"Error": "Bad request. " + str(error)}, 400

@send_messages.route("/api/messages/get_ten_messages/<int:conversation_id>", methods=["GET"])
@send_messages.route("/api/messages/get_ten_messages/<int:conversation_id>/<int:cursor>", methods=["GET"])
def get_ten_messages(conversation_id, cursor=None):
    # query 11 messages starting from cursor. If numbers of messages return < 11,
    # there is no more message to fetch next time
    try:
        messages = Messages.get_messages(conversation_id, 11, cursor)

        # if the message contains an image, add image data to the message's payload
        for m in messages:
            if m["attachment_name"] != "":
                m.update({
                    "has_attachment": True,
                    "thumbnail_name": "thumbnail_" + m["attachment_name"],
                    "regular_name": "regular_" + m["attachment_name"]
                })
            else:
                m["has_attachment"] = False

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
@socketio.on("join_conversation", namespace="/messages")
def join_conversation(data):
    old_conversation_id = data["oldConversationID"]
    new_conversation_id = data["newConversationID"]

    # if the user is currently in a conversation, leave that conversation.
    if (old_conversation_id):
        leave_room(old_conversation_id)

    join_room(new_conversation_id)

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
    # "senderID": The ID of the sender
    # "content": The content of the message
    # "conversationID": The current conversation's id
    # "createdAt": The message's sent time
    # "image": The image as a binary file. Value is None if the message doesn't have any attachment
    # "imageName": The name of the image. Value is "" if the message doesn't have any attachment
    sender_id = data["senderID"]
    message = data["content"]
    conversation_id = data["conversationID"]
    created_at = data["createdAt"]
    attachment_name = ""
    image = None

    if ("image" in data.keys()):
        image_name = data["imageName"]
        image = data["image"]
        attachment_name = str(created_at) + str(sender_id) + image_name # This is the image's id
        image_path = os.path.join(IMAGE_STORAGE_PATH, "regular_" + attachment_name)
        # Store the regular image to the system
        with open(image_path, "wb") as f:
            f.write(image)

        # Resize the image
        image_thumbnail = Image.open(image_path)
        image_thumbnail.thumbnail(THUMBNAIL_MAX_SIZE)

        # Store resized version to the system
        thumbnail_path = os.path.join(IMAGE_STORAGE_PATH, "thumbnail_" + attachment_name)
        image_thumbnail.save(thumbnail_path)

        image_data = {
            "regular_name": "regular_" + attachment_name,
            "thumbnail_name": "thumbnail_" + attachment_name,
            "has_attachment": True
        }

    # Update the database
    conversation = Conversations.select(conversation_id)
    new_message = Messages(sender_id=sender_id, content=message, created_at=created_at, conversation_id=conversation_id, attachment_name=attachment_name)
    Messages.insert(new_message)
    conversation.last_message_id = new_message.id # Manually set the last_message_id for now
    DB.session.commit()

    # Get sender_name
    sender_name = User.select(user_id=sender_id).username

    # Return data
    payload = {
        "id": new_message.id,
        "sender_id": sender_id,
        "sender_name": sender_name,
        "content": message,
        "created_at": created_at,
        "has_attachment": False
    }

    if image:
        payload.update(image_data)

    emit("updateLastMessageID", {"conversation_id": conversation_id, "last_message_id": new_message.id}, room=conversation_id)
    emit("messageHandlerClient", payload, room=conversation_id)

# A socket that updates user's last_active_time
@socketio.on("last_active", namespace="/messages")
def last_active(data):
    username = data["username"]
    last_active_time = data["last_active_time"]
    current_user = User.select(username)
    current_user.last_active_time = last_active_time
    DB.session.commit()
