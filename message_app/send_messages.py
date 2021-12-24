from typing import Any
from flask import Blueprint, render_template, jsonify, request
from flask.helpers import send_file, url_for
from werkzeug.utils import redirect
from . import db
import message_app
from flask_sse import sse 
send_messages = Blueprint("send_messages", __name__)

@send_messages.route("/api/send_messages>", methods=["POST"])
def check_save_messages():
    """This check if converstaion request has been accepted or not. then save it to the database"""

    try:
        params = request.form
        sender_id = params.get("sender_id", "")
        receiver_id = params.get("reciever_id", "")
        message_content = params.get("content", "")
        time_stamp = params.get("time_stamp", "")
        converstation_id = params.get("converstation", "")


        #Handle error of wrong type messages
        if not int(sender_id):
            raise Exception (400)
        if not int(receiver_id):
            raise Exception (400)
        if not str(message_content):
            raise Exception (400)
        if not int(time_stamp):
            raise Exception (400)
        if not int(converstation_id):
            raise Exception (400)
        

        check_conversation_request = db.query_db(
                "SELECT * FROM conversation WHERE id=: conversation_id",
                {"id": converstation_id}
            )

        #Check if the conversation has been created it yet
        if not check_conversation_request:
            raise Exception ("You should send the conversation request first")
        # save the the message to all message
        db.query_db(
                "INSERT INTO messages (conversation_id, sender_id, receiver_id, content, time_stamps) VALUES (:conversation_id, :sender_id, :receiver_id, :message_content,:seen, :time_stamp)",
                {"conversation_id": converstation_id, "sender_id": sender_id, "receiver_id": receiver_id, "message_content": message_content, "seen": 0, "time_stamp": time_stamp}
            )
        db.get_db().commit()
        #update latest message id to conversation
        get_latest_message_id= db.query_db(
                "SELECT id FROM messages WHERE content=:content",
                {"content": message_content}
            )
        db.query_db(
            "INSERT INTO conversations (conversation_id, last_message_id) VALUES (:conversation_id, :last_message_id)",
                {"conversation_id": converstation_id, "last_message_id": get_latest_message_id}
            )   

        return "Sended", 200
    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400