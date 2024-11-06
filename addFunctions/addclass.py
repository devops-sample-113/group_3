import sqlite3
from datetime import time

# con = sqlite3.connect("../instance/database.db")
con = sqlite3.connect("instance/database.db")
cur = con.cursor()

classes = [
    (
        1,
        "作業系統",
        "陳烈武",
        "資電104",
        "13:10",
        "15:00",
    ),
    (
        2,
        "微處理機實習",
        "王益文",
        "資電234",
        "09:10",
        "12:00",
    ),
    (
        3,
        "微處理機",
        "王益文",
        "資電404",
        "14:10",
        "16:00",
    ),
    (
        4,
        "軟體工程",
        "許懷中",
        "資電330",
        "13:10",
        "16:00",
    ),
    (
        5,
        "資料科學實務",
        "許懷中",
        "紀207",
        "10:10",
        "12:00",
    ),
]
cur.executemany(
    "INSERT INTO classes VALUES (?, ?, ?, ?, ?, ?)", classes
)

enrollments = [
    (1, 1, 1),
    (2, 1, 2),
    (3, 2, 3),
    (4, 3, 4),
    (5, 3, 5),
]
cur.executemany(
    "INSERT INTO enrollments VALUES (?, ?, ?)", enrollments
)
con.commit()
