import sqlite3
from datetime import time

# con = sqlite3.connect("../instance/database.db")
con = sqlite3.connect("instance/database.db")
cur = con.cursor()

classes = [
    (
        1,
        "1234",
        "作業系統",
        "陳烈武",
        "資電104",
        "6,7",
    ),
    (
        2,
        "9487",
        "微處理機實習",
        "王益文",
        "資電234",
        "2,3,4",
    ),
    (
        3,
        "5566",
        "微處理機",
        "王益文",
        "資電404",
        "7,8",
    ),
    (
        4,
        "4321",
        "軟體工程",
        "許懷中",
        "資電330",
        "6,7,8",
    ),
    (
        5,
        "1111",
        "資料科學實務",
        "許懷中",
        "紀207",
        "3,4",
    ),
]
cur.executemany(

    "INSERT INTO classes VALUES (?, ?, ?, ?, ?)", classes
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
