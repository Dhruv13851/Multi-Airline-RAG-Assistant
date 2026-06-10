import sqlite3
from pathlib import Path


class SQLiteManager:

    def __init__(
        self,
        db_path: str = "D:/PrivacyPolicy-Bot/data/memory.db"
    ):
        self.db_path = db_path

        Path(
            self.db_path
        ).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._initialize_database()

    def _initialize_database(self):

        with sqlite3.connect(
            self.db_path
        ) as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (

                    id INTEGER PRIMARY KEY AUTOINCREMENT,

                    session_id TEXT NOT NULL,

                    role TEXT NOT NULL,

                    content TEXT NOT NULL,

                    created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            conn.commit()

    def get_connection(self):

        return sqlite3.connect(
            self.db_path
        )