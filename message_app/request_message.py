from flask import Blueprint, render_template, jsonify
from message_app.db import db

request_messages = Blueprint("request_messages", __name__)

@request_messages.route("/api/request/send/<int:sender_id>/<int:receiver_id>/<int:request_time>", methods=["POST"])
def send_request(sender_id, receiver_id, request_time):
    try:
        requestData = db.query_db(
                "SELECT * FROM conversation_request WHERE initiator_id=:sender_id AND receiver_id=:receiver_id",
                {"sender_id": sender_id, "receiver_id": receiver_id},
                one=True
                )

        if requestData:
            raise Exception("Request has already been sent")

        db.query_db(
                "INSERT INTO conversation_request (initiator_id, receiver_id, request_time, accepted) VALUES (:sender_id, :receiver_id,:request_time, :accepted)",
                {"sender_id": sender_id, "receiver_id": receiver_id, "request_time": request_time, "accepted": 0}
                )
        db.get_db().commit()

        return "Success", 200
    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400

@request_messages.route("/api/request/accept/<int:request_id>/<int:accepted_time>", methods=["POST"])
def accept_request(request_id, accepted_time):
    try:
        requestData = db.query_db(
                "SELECT * FROM conversation_request WHERE id=:request_id AND accepted=:accepted",
                {"request_id": request_id, "accepted": 0},
                one=True
                )

        if not requestData:
            raise Exception("No request found")

        db.query_db(
                "UPDATE conversation_request SET accepted=1, accepted_time=:accepted_time  WHERE id=:request_id",
                {"request_id": request_id, "accepted_time": accepted_time}
                )
        db.get_db().commit()

        return "Success", 200
    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400

@request_messages.route("/api/request/reject/<int:request_id>", methods=["POST"])
def reject_request(request_id):
    try:
        requestData = db.query_db(
                "SELECT * FROM conversation_request WHERE id=:request_id AND accepted=:accepted",
                {"request_id": request_id, "accepted": 0},
                one=True
                )

        if not requestData:
            raise Exception("No request found")

        db.query_db(
                "UPDATE conversation_request SET accepted=0 WHERE id=:request_id",
                {"request_id": request_id}
                )

        db.get_db().commit()

        return "Success", 200

    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400

@request_messages.route("/api/request/all/<int:user_id>", methods=["GET"])
def get_all_requests(user_id):
    try:
        userData = db.query_db(
                "SELECT * FROM users WHERE id=:user_id",
                {"user_id": user_id},
                one=True
                )

        if not userData:
            raise Exception("No user found")

        requestData = db.query_db(
                "SELECT * FROM conversation_request WHERE receiver_id=:user_id AND accepted=0",
                {"user_id": user_id}
                )

        return jsonify(requestData), 200

    except Exception as error:
        return {"Error": "Bad Request." + str(error)}, 400


