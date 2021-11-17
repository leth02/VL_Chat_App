
import sqlite3

conn = sqlite3.connect("db/VL_MESSAGES.db")
c = conn.cursor()
c.execute("SELECT password, salt FROM users WHERE username=:username", {"username": "long"})
print(c.fetchall()[0])