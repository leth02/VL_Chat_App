
from __future__ import annotations
from message_app.db.db import DB as db
import json
import time
from typing import Union, List

# TODO: Optimize all models by removing the duplicated codes.
# All the models will be REFACTORED in the future for more functionalities
# and better understanding. For now, these models are good enough for
# our upcoming prototype.

# A join table for the many-to-many relationship between users and conversations tables
# For now, we don't need to create a model for this table because this table only serves
# the purpose of joining users and conversations tables (many-to-many relationship)
users_conversations = db.Table(
    "users_conversations",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("conversation_id", db.Integer, db.ForeignKey("conversations.id")),
    db.Column("seen", db.Boolean, default=False)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(120))

    def __eq__(self, other_user: User) -> bool:
        # Compare two users using its username
        return other_user.username == self.username

    # Return a json encoding of the user data
    def to_json(self) -> str:
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash
        }
        return json.dumps(data)


    #================Class Methods==================

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
        # Get an user from the database using username. Return None if the user doesn't exist
        # The method selects only one user for now, but it CAN BE IMPROVED later on.
        # TODO: Select multiple users with multiple conditions
        user = User.query.filter_by(username=username).first()
        return user

    @classmethod
    def select_all(cls) -> List:
        all_users = User.query.all()
        return all_users

    @classmethod
    def get_last_user_id(cls) -> int:
        # Get last user ID
        id = User.query.order_by(User.id.desc()).first().id
        return id

class Conversations(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.Integer, primary_key=True)
    participants = db.relationship("User", secondary=users_conversations, backref="conversations", lazy=True)
    messages = db.relationship("Messages", backref="conversations")
    created_at = db.Column(db.Float, default=time.time())
    last_message_id = db.Column(db.Integer) # This column is a foreignkey

    # Return a json encoding of the conversation data
    def to_json(self) -> str:
        data = {
            "id": self.id
        }
        return json.dumps(data)


    #================Class Methods==================
    @classmethod
    def insert(cls, new_conversation: Conversations) -> None:
        # Add a new user to the database
        db.session.add(new_conversation)
        db.session.commit()

    @classmethod
    def delete(cls, conversation_id: int) -> Union[Conversations, None]:
        # Delete and return an user from the database. Return None if the user doesn't exist
        conversation = Conversations.select(conversation_id)
        if conversation:
            db.session.delete(conversation)
            db.session.commit()
        return conversation

    @classmethod
    def select(cls, conversation_id: int) -> Union[Conversations, None]:
        # Get an user from the database using username. Return None if the user doesn't exist
        # The method selects only one user for now, but it CAN BE IMPROVED later on.
        # TODO: Select multiple users with multiple conditions
        conversation = Conversations.query.filter_by(id=conversation_id).first()
        return conversation

    @classmethod
    def get_last_conversation_id(cls) -> int:
        # Get last conversation ID
        id = Conversations.query.order_by(Conversations.id.desc()).first().id
        return id


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.String(255))
    created_at = db.Column(db.Integer, default=time.time())
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'))


    # Return a json encoding of the user data
    def to_json(self) -> str:
        data = {
            "id": self.id,
            "sender_id": self.sender_id,
            "content": self.content,
            "conversation_id": self.conversation_id
        }
        return json.dumps(data)


    #================Class Methods==================
    @classmethod
    def insert(cls, new_conversation: Messages) -> None:
        # Add a new user to the database
        db.session.add(new_conversation)
        db.session.commit()

    @classmethod
    def delete(cls, message_id: int) -> Union[Messages, None]:
        # Delete and return an user from the database. Return None if the user doesn't exist
        message = Messages.select(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
        return message

    @classmethod
    def select(cls, message_id: int) -> Union[Messages, None]:
        # Get an user from the database using username. Return None if the user doesn't exist
        # The method selects only one user for now, but it CAN BE IMPROVED later on.
        # TODO: Select multiple users with multiple conditions
        message = Messages.query.filter_by(id=message_id).first()
        return message

    @classmethod
    def get_last_message_id(cls) -> int:
        # Get last message ID
        id = Messages.query.order_by(Messages.id.desc()).first().id
        return id