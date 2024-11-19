import sqlite3
from datetime import time

# con = sqlite3.connect("../instance/database.db")
con = sqlite3.connect("instance/database.db")
cur = con.cursor()

courses = [
    (
        1,
        "1428",
        "作業系統",
        "陳烈武",
        "資電104",
        "四",
        "6,7",
        3,
        "https://ilearntools.fcu.edu.tw/W320104/W320104_SyllabusFullVer.aspx?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicHVibGljIiwibGFuZyI6ImNodCIsImNvdXJzZUlkIjoiMTEzMUNFMDcxMzQxNjcxMDAwMSIsImNvdXJzZUtleSI6eyJ5bXNfeWVhciI6MTEzLCJ5bXNfc21lc3RlciI6MSwiY2xzX2lkIjoiQ0UwNzEzNCIsInN1Yl9pZCI6IjE2NzEwIiwic2NyX2R1cCI6IjAwMSJ9LCJzeXNUeXBlIjpudWxsLCJ1bml0IjpudWxsLCJyb2xlIjpudWxsLCJleHAiOjE3MzE5NDM3NzZ9.YS-LGZqtyuvacP837VLqzt9w_MhB7f0-Oz_khvZGqwk#!/fullVer/cht",
        4,
    ),
    (
        2,
        "1430",
        "微處理機實習",
        "王益文",
        "資電234",
        "一",
        "2,3,4",
        1,
        "https://ilearntools.fcu.edu.tw/W320104/W320104_SyllabusFullVer.aspx?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicHVibGljIiwibGFuZyI6ImNodCIsImNvdXJzZUlkIjoiMTEzMUNFMDcxMzQ2MDYwMTAwMSIsImNvdXJzZUtleSI6eyJ5bXNfeWVhciI6MTEzLCJ5bXNfc21lc3RlciI6MSwiY2xzX2lkIjoiQ0UwNzEzNCIsInN1Yl9pZCI6IjYwNjAxIiwic2NyX2R1cCI6IjAwMSJ9LCJzeXNUeXBlIjpudWxsLCJ1bml0IjpudWxsLCJyb2xlIjpudWxsLCJleHAiOjE3MzE5NDM4Njl9.hikShazJUMBFO6jAz-kA32dhUI0otuntg0W2a9jOKsY#!/fullVer/cht",
        2,
    ),
    (
        3,
        "1429",
        "微處理機",
        "王益文",
        "資電404",
        "一",
        "7,8",
        3,
        "https://ilearntools.fcu.edu.tw/W320104/W320104_SyllabusFullVer.aspx?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicHVibGljIiwibGFuZyI6ImNodCIsImNvdXJzZUlkIjoiMTEzMUNFMDcxMzQ2MDYwMDAwMSIsImNvdXJzZUtleSI6eyJ5bXNfeWVhciI6MTEzLCJ5bXNfc21lc3RlciI6MSwiY2xzX2lkIjoiQ0UwNzEzNCIsInN1Yl9pZCI6IjYwNjAwIiwic2NyX2R1cCI6IjAwMSJ9LCJzeXNUeXBlIjpudWxsLCJ1bml0IjpudWxsLCJyb2xlIjpudWxsLCJleHAiOjE3MzE5NDM4Njh9.0T2f5JF2m8aWUOFCGxntzr_DRTO1ApONw3ZWWdZZVDs#!/fullVer/cht",
        2,
    ),
    (
        4,
        "1432",
        "軟體工程",
        "許懷中",
        "資電330",
        "三",
        "6,7,8",
        3,
        "https://ilearntools.fcu.edu.tw/W320104/W320104_SyllabusFullVer.aspx?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicHVibGljIiwibGFuZyI6ImNodCIsImNvdXJzZUlkIjoiMTEzMUNFMDcxMzk0NDIzMzAwMSIsImNvdXJzZUtleSI6eyJ5bXNfeWVhciI6MTEzLCJ5bXNfc21lc3RlciI6MSwiY2xzX2lkIjoiQ0UwNzEzOSIsInN1Yl9pZCI6IjQ0MjMzIiwic2NyX2R1cCI6IjAwMSJ9LCJzeXNUeXBlIjpudWxsLCJ1bml0IjpudWxsLCJyb2xlIjpudWxsLCJleHAiOjE3MzE5NDM5Nzl9.EVZuK0eDzbyF3J5fyOvKh7t9pUFuZwSo-YgVsA4S4Sw#!/fullVer/cht",
        3,
    ),
    (
        5,
        "1434",
        "資料科學實務",
        "許懷中",
        "紀207",
        "二",
        "3,4",
        3,
        "https://ilearntools.fcu.edu.tw/W320104/W320104_SyllabusFullVer.aspx?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoicHVibGljIiwibGFuZyI6ImNodCIsImNvdXJzZUlkIjoiMTEzMUNFMDcxMzk1OTQ3MjAwMSIsImNvdXJzZUtleSI6eyJ5bXNfeWVhciI6MTEzLCJ5bXNfc21lc3RlciI6MSwiY2xzX2lkIjoiQ0UwNzEzOSIsInN1Yl9pZCI6IjU5NDcyIiwic2NyX2R1cCI6IjAwMSJ9LCJzeXNUeXBlIjpudWxsLCJ1bml0IjpudWxsLCJyb2xlIjpudWxsLCJleHAiOjE3MzE5NDQwMjN9.lHL7P8f7k1m1Yoaafn9X9F_2y7dJDGjNVEPi88A24NA#!/fullVer/cht",
        1,
    ),
]
cur.executemany(
    "INSERT INTO courses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", courses
)

# enrollments = [
#     ( 1, 1),
#     ( 1, 2),
#     ( 2, 3),
#     ( 3, 4),
#     ( 3, 5),
# ]
# cur.executemany(
#     "INSERT INTO enrollments (student_id, class_id) VALUES (?, ?)", enrollments
# )

# follow = [
#     ( 1, 1),
#     ( 1, 2),
#     ( 2, 3),
#     ( 3, 4),
#     ( 3, 5),
# ]
# cur.executemany(
#     "INSERT INTO follow (student_id, class_id) VALUES (?, ?)", follow
# )

con.commit()
