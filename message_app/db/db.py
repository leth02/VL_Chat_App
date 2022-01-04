import sqlite3
import os
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

# Create an SQLAlchemy instance that is used throughout the application. As we create a Flask instance
# dynamically by using factory pattern, we cannot pass it here (DB = SQLAlchemy(app)) because the app
# instance has not existed. Inside the factory function to create a Flask app instance, we need to call
# init_SQLAlchemy function which in turns will call DB.init_app(current_app) to initialize the use of
# the app with this database setup and call DB.create_all() to create the tables.
DB = SQLAlchemy()

# Initialize the database
def init_SQLAlchemy() -> None:
    DB.init_app(current_app)
    DB.create_all()

# Connect to the database
# This function returns a database connection, which is used to execute the commands read from the file.
# The g name stands for “global”, but that is referring to the data being global within a context.
# The data on g is lost after the context ends. Flask provides the g object for this purpose.
# g is a simple namespace object that has the same lifetime as an application context.
# db is an attribute of object g. We will store the connection to our database to g.db
# This function is for the old use of the database. It will be removed after we change to SQLAlchemy
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Enable validating foreign_keys
        g.db.execute("PRAGMA foreign_keys = ON;")
        g.db.row_factory = make_dicts

    return g.db


# Close the database connection
# We close the connection to our database and remove it from the g object
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# Run a query
# When we pass variable parts to the SQL statement, we will avoid directly adding them
# to the SQL statement with string formatting because this makes it possible to attack
# the application using SQL Injections. Instead, we will pass in arguments as a dictionary
# The parameter one is used for fetching the first row.
def query_db(query: str, args={}, one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def make_dicts(cursor, row):
    """convert the retrieved data into dictionary with key is column name"""
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# Init a new database if the database doesn't exist.
# open_resource() opens a file relative to the flaskr package, which is useful since you won’t necessarily
# know where that location is when deploying the application later.
def init_db():
    db = get_db()
    path_to_schema = os.path.join("db", 'message-app.sql')
    with current_app.open_resource(path_to_schema) as f:
        db.executescript(f.read().decode('utf8'))


# Register the close_db function with the application instance
def init_app(app):
    app.teardown_appcontext(close_db) # This line will be removed after changing to SQLAlchemy
