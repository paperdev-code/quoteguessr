from typing import Tuple, Optional
import sqlite3
import random

class Database():
    # Single instance object
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.db: sqlite3.Connection

    def init(self, path_to_db) -> None:
        self.db = sqlite3.connect(path_to_db)
        cur = self.db.cursor()
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                speaker INTEGER NOT NULL,
                recipient INTEGER,
                quote TEXT NOT NULL)
            """);

    def saveQuote(self, speaker: int, recipient: Optional[int], quote: str) -> None:
        columns = "speaker, quote" if recipient is None else "speaker, recipient, quote"
        values = f"{speaker}, \"{quote}\"" if recipient is None else f"{speaker}, {recipient}, \"{quote}\"";
        cur = self.db.cursor()
        cur.execute(f"INSERT INTO quotes ({columns}) VALUES ({values})")
        self.db.commit()

    def randomQuote(self) -> Tuple[int, Optional[int], str]:
        count = self.countQuotes()
        cur = self.db.cursor()
        offset = random.randint(1, count - 1)
        cur.execute(f"SELECT speaker, recipient, quote FROM quotes LIMIT 1 OFFSET {offset}")
        row = cur.fetchone()
        return (row[0], row[1], row[2])

    def countQuotes(self) -> int:
        cur = self.db.cursor()
        cur.execute("SELECT COUNT(*) FROM quotes")
        return cur.fetchone()[0]
