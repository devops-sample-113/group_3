import sqlite3
from werkzeug.security import generate_password_hash

# con = sqlite3.connect("../instance/database.db")
con = sqlite3.connect("instance/database.db")
cur = con.cursor()

students = [
    (
        1,
        "D1158787",
        "褚翊喨",
        generate_password_hash("123456"),
    ),
    (
        2,
        "D1158429",
        "王定偉",
        generate_password_hash("123456"),
    ),
    (
        3,
        "D1158801",
        "陳宗佑",
        generate_password_hash("123456"),
    ),
    (
        4,
        "D1158459",
        "馮柏瑋",
        generate_password_hash("123456"),
    ),
    (
        5,
        "D1158623",
        "莊智凱",
        generate_password_hash("123456"),
    ),
]
cur.executemany(
    "INSERT INTO students VALUES(?, ?, ?, ?)", students
)
con.commit()
