
from __future__ import annotations
from message_app.db.db import DB as db
import json
import time
from typing import Union, List
from sqlalchemy import func, desc, asc, not_, and_
from sqlalchemy.sql import label

# A join table for the many-to-many relationship between users and conversations tables.
# Create a model for this table is unnecessary.
users_conversations = db.Table(
    "users_conversations",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("conversation_id", db.Integer, db.ForeignKey("conversations.id")),
    db.Column("seen", db.Boolean, default=False)
)

# SQLAlchemy model for users table
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(120))

    # create one-to-many relationships with ConversationRequest model
    # backref: declear reference property for ConversationRequest's instances.
    # We can then call instance_example.initiator/instance.example.receiver to get
    # the initiator/receiver of that instance_example.
    initiators = db.relationship("ConversationRequest", backref="initiator", foreign_keys="ConversationRequest.initiator_id")
    receivers = db.relationship("ConversationRequest", backref="receiver", foreign_keys="ConversationRequest.receiver_id")

    def __eq__(self, other_user: User) -> bool:
        # Compare two users using its username
        return other_user.username == self.username


    def to_json(self) -> str:
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash
        }
        return json.dumps(data)


    @classmethod
    def insert(cls, new_user: User) -> None:
        # Add a new user to the database
        db.session.add(new_user)
        db.session.commit()

    @classmethod
    def delete(cls, username: str) -> Union[User, None]:
        # Delete and return an user from the database. Return None if the user doesn't exist
        user = User.select(username)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user

    @classmethod
    def select(cls, username: str) -> Union[User, None]:
        user = User.query.filter_by(username=username).first()
        return user

    @classmethod
    def select_v2(cls, filter_option: dict):
        """Allow querying users with more filter options"""
        pass

    @classmethod
    def select_all(cls) -> List:
        # TODO: This method should be deprecated when add Channel
        all_users = User.query.all()
        return all_users

    @classmethod
    def get_last_user_id(cls) -> int:
        id = User.query.order_by(User.id.desc()).first().id
        return id

    @classmethod
    def find_people(cls, user_id: str) -> List:
        # query all requests that send to user_id
        sub_query = db.session.query(
                ConversationRequest,
                label("latest_request", func.max(ConversationRequest.request_time))
                ).filter(ConversationRequest.receiver_id == user_id).group_by(ConversationRequest.initiator_id).subquery()

        #query all users that send request to user_id
        sender_query = db.session.query(
                User.id,
                User.username,
                sub_query.c.id,
                sub_query.c.initiator_id,
                sub_query.c.receiver_id,
                sub_query.c.status,
                sub_query.c.request_time
                ).join(sub_query, User.id == sub_query.c.initiator_id).order_by(asc(User.id)).all()

        # query all request that user_id send
        sub_query_2 = db.session.query(
                ConversationRequest,
                label("latest_request", func.max(ConversationRequest.request_time))
                ).filter(ConversationRequest.initiator_id == user_id).group_by(ConversationRequest.receiver_id).subquery()

        #query all users that receive request from user_id
        receiver_query = db.session.query(
                User.id,
                User.username,
                sub_query_2.c.id,
                sub_query_2.c.initiator_id,
                sub_query_2.c.receiver_id,
                sub_query_2.c.status,
                sub_query_2.c.request_time
                ).join(sub_query_2, User.id == sub_query_2.c.receiver_id).order_by(asc(User.id)).all()

        all_request_users = sender_query + receiver_query
        dic = {}
        request_users_id = []

        # filter conversation request between user_id with another, choose the
        # request that has latest request_time
        for i in all_request_users:
            is_receiver = i[0] == i[4]
            key = tuple(sorted([i[3], i[4]]))

            if i[0] not in request_users_id:
                request_users_id.append(i[0])

            if key not in dic:
                dic[key] = {
                        "user_id": i[0],
                        "username": i[1],
                        "request_id": i[2],
                        "request_status": i[5],
                        "request_time": i[6],
                        "is_sender": not is_receiver,
                        "is_receiver": is_receiver
                        }
            else:
                if dic[key]["request_time"] < i[6]:
                    dic[key] = {
                            "user_id": i[0],
                            "username": i[1],
                            "request_id": i[2],
                            "request_status": i[5],
                            "request_time": i[6],
                            "is_sender": not is_receiver,
                            "is_receiver": is_receiver
                            }

        result = list(dic.values())

        # query all the users that do not have any request to/from user_id
        no_request_users = db.session.query(User.id, User.username).filter(
                and_(
                    not_(User.id.in_(request_users_id)),
                    User.id != user_id
                    )
                ).all()

        for i in no_request_users:
            result.append({
                "user_id": i[0],
                "username": i[1],
                "request_id": None,
                "request_status": None,
                "request_time": None,
                "is_sender": None,
                "is_receiver": None
                })

        return result

class Conversations(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    participants = db.relationship("User", secondary=users_conversations, backref="conversations", lazy=True)
    messages = db.relationship("Messages", backref="conversations")
    created_at = db.Column(db.Float, default=time.time())
    last_message_id = db.Column(db.Integer) # This column is a foreignkey


    def to_json(self) -> str:
        data = {
            "id": self.id
        }
        return json.dumps(data)


    @classmethod
    def insert(cls, new_conversation: Conversations) -> None:
        # Add a new user to the database
        db.session.add(new_conversation)
        db.session.commit()

    @classmethod
    def delete(cls, conversation_id: int) -> Union[Conversations, None]:
        conversation = Conversations.select(conversation_id)
        if conversation:
            db.session.delete(conversation)
            db.session.commit()
        return conversation

    @classmethod
    def select(cls, conversation_id: int) -> Union[Conversations, None]:
        conversation = Conversations.query.filter_by(id=conversation_id).first()
        return conversation

    @classmethod
    def select_v2(cls, filter_option: dict):
        """Allow querying conversations with more filter options"""
        pass

    @classmethod
    def get_last_conversation_id(cls) -> int:
        id = Conversations.query.order_by(Conversations.id.desc()).first().id
        return id


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(255))
    created_at = db.Column(db.Integer, default=time.time())
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))


    def to_json(self) -> str:
        data = {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": self.content,
            "conversation_id": self.conversation_id
        }
        return json.dumps(data)


    @classmethod
    def insert(cls, new_conversation: Messages) -> None:
        db.session.add(new_conversation)
        db.session.commit()

    @classmethod
    def delete(cls, message_id: int) -> Union[Messages, None]:
        message = Messages.select(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
        return message

    @classmethod
    def select(cls, message_id: int) -> Union[Messages, None]:
        message = Messages.query.filter_by(id=message_id).first()
        return message

    @classmethod
    def select_v2(cls, filter_option: dict):
        """Allow querying messages with more filter options"""
        pass

    @classmethod
    def get_last_message_id(cls) -> int:
        id = Messages.query.order_by(Messages.id.desc()).first().id
        return id


# SQLAlchemy model for conversation_request table
class ConversationRequest(db.Model):
    __tablename__ = 'conversation_request'
    id = db.Column(db.Integer, primary_key=True)
    initiator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String, nullable=False, default="pending") # 3 status: pending, accepted, rejected
    request_time = db.Column(db.Integer, nullable=False)
    accepted_time = db.Column(db.Integer)

    def __eq__(self, other_request: ConversationRequest) -> bool:
        # Compare two users using its username
        return other_request.id == self.id

    def to_json(self) -> str:
        data = {
            "id": self.id,
            "initiator_id": self.initiator_id,
            "receiver_id": self.receiver_id,
            "status": self.status,
            "request_time": self.request_time,
            "accepted_time": self.accepted_time
        }
        return json.dumps(data)

    def accept(self, time: int) -> None:
        self.status = "accepted"
        self.accepted_time = time
        db.session.commit()

    def reject(self) -> None:
        self.status = "rejected"
        db.session.commit()


    @classmethod
    def get_all_requests(cls, receiver_id: int) -> List:
        """Return conversation requests sent to a user"""
        all_requests = ConversationRequest.query.filter(
                ConversationRequest.receiver_id == receiver_id,
                ConversationRequest.status == "pending"
                ).order_by(ConversationRequest.id.asc()).all()

        all_requests_list = []

        for request in all_requests:
            all_requests_list.append({
                    "id": request.id,
                    "initiator_id": request.initiator_id,
                    "receiver_id": request.receiver_id,
                    "status": request.status,
                    "request_time": request.request_time,
                    "accepted_time": request.accepted_time
                })
        return all_requests_list

    @classmethod
    def get_request_by_users(cls, initiator_id: int, receiver_id: int) -> Union[ConversationRequest, None]:
        """Return latest pending conversation request between two users"""
        request = ConversationRequest.query.filter(
                ConversationRequest.initiator_id == initiator_id,
                ConversationRequest.receiver_id == receiver_id,
                ConversationRequest.status == "pending"
                ).first()
        return request

    @classmethod
    def get_request_by_id(cls, request_id: int) -> Union[ConversationRequest, None]:
        request = ConversationRequest.query.filter(
                ConversationRequest.id == request_id,
                ConversationRequest.status == "pending"
                ).first()
        return request

    @classmethod
    def insert(cls, new_request: ConversationRequest) -> None:
        db.session.add(new_request)
        db.session.commit()
