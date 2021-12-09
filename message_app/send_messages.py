from typing import Any
from flask import Blueprint, render_template, jsonify, request
from flask.helpers import send_file, url_for
from werkzeug.utils import redirect
from . import db
import message_app

send_messages = Blueprint("send_messages", __name__)

@send_messages.route("/api/send_messages>", methods=["POST"])
def check_save_messages():
    """This check if converstaion request has been accepted or not. then save it to the database"""

    try:
        params = request.form
        sender_id = params.get("sender_id","")
        receiver_id = params.get("reciever","")
        message_content = params.get("message_content","")
        time_stamp = params.get("time_stamp","")

        #Handle error of wrong type messages
        # if not int(sender_id):
        #     raise Exception("")
        # if not int(receiver_id):
        #     raise Exception ("")
        # if not str(message_content):
        #     raise Exception ("")
        # if not int(time_stamp):
        #     raise Exception ("")

        check_conversation_request = db.query_db(
                "SELECT * FROM requests WHERE sender_id=:sender_id AND receiver_id=:receiver_id",
                {"sender_id": sender_id, "receiver_id": receiver_id},
                one=  True
            )

        #Check if the conversation has been created it yet
        if not check_conversation_request:
            raise Exception ("You should send the request first")
        # save the the message to all message
        db.query_db(
                "INSERT INTO all_messages (sender_id, receiver_id, messages_content, time_stamps) VALUES (:sender_id, :receiver_id, message_content, time_stamp)",
                {"sender_id": sender_id, "receiver_id": receiver_id, "message_content": message_content, "time_stamp": time_stamp}
            )
        db.get_db().commit()
        return "Success", 200
    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400

    

# @send_messages.route("/api/request/send/<int:sender_id>/<int:receiver_id>/<str:message_content>/<int:time_stamp>", methods=["POST"])
# def check_conversation_request(sender_id: int, receiver_id: int, message_content: str, time_stamp: int) -> Any: 
#     #This function also use to save the messages to database
#     try:
#         send_message = db.query_db(
#                 "SELECT * FROM requests WHERE sender_id=:sender_id AND receiver_id=:receiver_id",
#                 {"sender_id": sender_id, "receiver_id": receiver_id},
#                 one=True
#                 )
#         if not send_message:
#             raise Exception ("You should send the request first")
#         db.query_db(
#                 "INSERT INTO all_messages (sender_id, receiver_id, messages_content, time_stamps) VALUES (:sender_id, :receiver_id, message_content, time_stamp)",
#                 {"sender_id": sender_id, "receiver_id": receiver_id, "message_content": message_content, "time_stamp": time_stamp}
#                 )
#         db.get_db().commit()
#         send_message_package = [sender_id, message_content, time_stamp]
#         return redirect(url_for(endpoint= receiver_id,values= send_message_package))
#     except Exception as error:
#         return {"Error": "Bad Request." + str(error)}, 400