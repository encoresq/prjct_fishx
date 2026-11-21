import bcrypt
import os
import sqlite3
from PyQt6.QtGui import QImageReader
from config import base_path


def get_user_id(login):
    with sqlite3.connect(base_path("projectFish.db")) as con:
        cur = con.cursor()

        query = """SELECT user_id FROM users WHERE user_login = ?;"""

        id = cur.execute(query, (login,)).fetchone()

    return id[0]


def user_registration(login, password):
    password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password, salt).decode("utf-8")

    try:
        with sqlite3.connect(base_path("projectFish.db")) as con:
            cur = con.cursor()
            query = """INSERT INTO users (user_login, user_pass) VALUES (?, ?)"""
            cur.execute(query, (login, hash_password))

            return cur.lastrowid
    except sqlite3.IntegrityError:
        return None


def check_user_registration(login, password):
    with sqlite3.connect(base_path("projectFish.db")) as con:
        cur = con.cursor()

        query = """SELECT user_login, user_pass FROM users WHERE user_login = ?;"""
        res = cur.execute(query, (login,)).fetchone()

        if not res:
            return False

        db_hash = res[1]

        entered_password_bytes = password.encode("utf-8")
        db_hash_bytes = db_hash.encode("utf-8")

        if bcrypt.checkpw(entered_password_bytes, db_hash_bytes):
            return True

        return False


def is_safe_image(file_path: str, max_size_mb: int = 15):
    if not os.path.isfile(file_path):
        return False

    file_size = os.path.getsize(file_path)
    if file_size > max_size_mb * 1024 * 1024:
        return False

    reader = QImageReader(file_path)
    reader.setDecideFormatFromContent(True)

    if not reader.canRead():
        return False

    allowed_formats = [b"jpeg", b"jpg", b"png"]
    detected_format = reader.format().data().lower()

    if detected_format not in allowed_formats:
        return False

    return True
