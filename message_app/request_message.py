from flask import Blueprint, render_template, jsonify, session
from message_app.model import *
from message_app.db.db import DB as db

request_messages = Blueprint("request_messages", __name__)

@request_messages.route("/api/request/send/<int:sender_id>/<int:receiver_id>/<int:request_time>", methods=["POST"])
def send_request(sender_id, receiver_id, request_time):
    try:
        request_data = ConversationRequest.get_request_by_users(sender_id, receiver_id)
        if request_data:
            raise Exception("Request has already been sent")

        new_request = ConversationRequest(
                initiator_id=sender_id,
                receiver_id=receiver_id,
                request_time=request_time
                )

        ConversationRequest.insert(new_request)
        return "Success", 200
    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400

@request_messages.route("/api/request/accept/<int:request_id>/<int:accepted_time>", methods=["POST"])
def accept_request(request_id, accepted_time):
    try:
        request_data = ConversationRequest.get_request_by_id(request_id)
        if not request_data:
            raise Exception("No request found")

        request_data.accept(accepted_time)
        return "Success", 200
    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400

@request_messages.route("/api/request/reject/<int:request_id>", methods=["POST"])
def reject_request(request_id):
    try:
        request_data = ConversationRequest.get_request_by_id(request_id)

        if not request_data:
            raise Exception("No request found")

        request_data.reject()

        return "Success", 200

    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400

@request_messages.route("/api/request/all/<int:user_id>", methods=["GET"])
def get_all_requests(user_id):
    try:
        user_data = User.query.filter(User.id == user_id).first()
        if not user_data:
            raise Exception("No user found")

        request_data = ConversationRequest.get_all_requests(user_data.id)

        return jsonify(request_data), 200

    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400

@request_messages.route("/api/request/get_people/<int:user_id>", methods=["GET"])
def get_people(user_id):
    # get all users except user_id
    try:
        data = User.find_people(user_id)

        return jsonify(data), 200

    except Exception as error:
        return {"Error": "Bad request." + str(error)}, 400

@request_messages.route("/request/people", methods=["GET"])
def render_people():
    if "user" in session:
        return render_template("people_list.html", user=session["user"])
    else:
        return render_template("index.html")

