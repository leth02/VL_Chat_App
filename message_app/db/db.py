import sqlite3
import os
from flask import current_app, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////message_app_db.sqlite3')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

# Connect to the database
# This function returns a database connection, which is used to execute the commands read from the file.
# The g name stands for “global”, but that is referring to the data being global within a context.
# The data on g is lost after the context ends. Flask provides the g object for this purpose.
# g is a simple namespace object that has the same lifetime as an application context.
# db is an attribute of object g. We will store the connection to our database to g.db
# The sqlite3.Row is used to convert the row data in tuple to dictionary for easier access
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# Close the database connection
# We close the connection to our database and remove it from the g object
def close_db(e=None):
    db_session.remove()
    # db = g.pop('db', None)

    # if db is not None:
    #     db.close()


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


# Init a new database if the database doesn't exist.
# open_resource() opens a file relative to the flaskr package, which is useful since you won’t necessarily
# know where that location is when deploying the application later.
def init_db():
    # db = get_db()
    import message_app.model
    Base.metadata.create_all(bind=engine)

    path_to_schema = os.path.join("db", 'message-app.sql')
    with current_app.open_resource(path_to_schema) as f:
        db.executescript(f.read().decode('utf8'))


# Register the close_db function with the application instance
def init_app(app):
    app.teardown_appcontext(close_db)