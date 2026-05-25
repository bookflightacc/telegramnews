import sqlite3

conn = sqlite3.connect("news.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS posted_news (
    url TEXT PRIMARY KEY
)
""")

conn.commit()


def already_posted(url):
    cursor.execute(
        "SELECT url FROM posted_news WHERE url=?",
        (url,)
    )

    return cursor.fetchone() is not None


def save_posted(url):
    cursor.execute(
        "INSERT OR IGNORE INTO posted_news(url) VALUES(?)",
        (url,)
    )

    conn.commit()