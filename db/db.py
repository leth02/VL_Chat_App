import sqlite3
import os
from flask import g, current_app

# Sources:
# https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/
# https://flask.palletsprojects.com/en/2.0.x/tutorial/database/

DATABASE = os.path.join("db", "VL_MESSAGES.db")

# Connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Close the connection
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Convert the selected rows into dictionary
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# Run a query
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Init db if data doesn't exist
def init_db():
    with current_app.app_context():
        db = get_db()
        with current_app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()