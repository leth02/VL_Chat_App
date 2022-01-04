
from __future__ import annotations
from message_app.db.db import DB as db
import json
from typing import Union, List

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
