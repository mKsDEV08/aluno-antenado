import csv
from cs50 import SQL

db = SQL("sqlite:///manage-users/users.db")


def consume_ids():
    rows = db.execute("SELECT id FROM users;")
    ids = []

    for row in rows:
        ids.append(row['id'])

    return ids

print(consume_ids())
