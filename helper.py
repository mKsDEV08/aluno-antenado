from cs50 import SQL

db = SQL("sqlite:///manage-users/aluno-antenado.db")


def consume_ids():
    rows = db.execute("SELECT id FROM users;")
    ids = []

    for row in rows:
        ids.append(row['id'])

    return ids

def consume_news():
    news_db = db.execute("SELECT new FROM news")
    news = []

    for new in news_db:
        news.append(new['new'])

    return news