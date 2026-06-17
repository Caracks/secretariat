import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("/app/ai-orchestrator/storage/bot.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE,
                group_id TEXT,
                sender_name TEXT,
                sender_id TEXT,
                direction TEXT NOT NULL,
                text TEXT,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS processed_messages (
                message_id TEXT PRIMARY KEY,
                processed_at TEXT NOT NULL
            )
        """)

        conn.commit()


def is_processed(message_id: str) -> bool:
    if not message_id:
        return False

    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT 1 FROM processed_messages WHERE message_id = ?",
            (message_id,)
        )
        return cursor.fetchone() is not None


def mark_processed(message_id: str):
    if not message_id:
        return

    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO processed_messages (message_id, processed_at)
            VALUES (?, ?)
            """,
            (message_id, datetime.utcnow().isoformat())
        )
        conn.commit()


def save_message(
    message_id: str,
    group_id: str,
    sender_name: str,
    sender_id: str,
    direction: str,
    text: str
):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT OR IGNORE INTO messages (
                message_id,
                group_id,
                sender_name,
                sender_id,
                direction,
                text,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                message_id,
                group_id,
                sender_name,
                sender_id,
                direction,
                text,
                datetime.utcnow().isoformat()
            )
        )
        conn.commit()
