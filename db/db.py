import sqlite3

# with sqlite3.connect("db/projectFish.db") as con:
#     cur = con.cursor()

#     query = """DELETE FROM users WHERE user_id > 8;"""

#     cur.execute(query).fetchall()

# with sqlite3.connect("db/projectFish.db") as con:
#     cur = con.cursor()

#     query = """DELETE FROM sqlite_sequence WHERE name = 'users';"""

#     cur.execute(query).fetchall()

with sqlite3.connect("db/projectFish.db") as con:
    cur = con.cursor()

    query = """DELETE FROM users WHERE user_id < 9;"""

    cur.execute(query).fetchall()