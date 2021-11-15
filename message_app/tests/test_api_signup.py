import sqlite3

conn = sqlite3.connect("VL_MESSAGES.db")

c = conn.cursor()

c.execute(f"SELECT * FROM users WHERE username=23")
userData = c.fetchone()
print(userData)
conn.commit()
conn.close()