
from __future__ import annotations
from message_app.db.db import DB as db
import json

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(120))
    password_salt = db.Column(db.String(120))

    def __eq__(self, __o: User) -> bool:
        # Compare two users using its username
        return __o.username == self.username

    # Return a json encoding of the user data
    def to_json(self) -> str:
        data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "password_salt": self.password_salt
        }
        return json.dumps(data)

    #
    # Insert, Delete, and Select functions
    #

    def insert(__o: User) -> None:
        # Add a new user to the database
        db.session.add(__o)
        db.session.commit()

    def delete(username: str) -> User:
        # Delete an user from the database
        user = User.select(username)
        db.session.delete(user)
        db.session.commit()

    def select(username: str) -> User:
        # Get an user from the database using username
        user = User.query.filter_by(username=username).first()
        return user
