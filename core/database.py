import sqlite3
import os
import json
from datetime import datetime, timezone
from core.config import DB_PATH

def utc_now():
    return datetime.now(timezone.utc).isoformat()


def db_connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    with db_connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT UNIQUE,
                source TEXT NOT NULL,
                group_id TEXT,
                sender_id TEXT,
                sender_name TEXT,
                direction TEXT NOT NULL,
                text TEXT,
                raw_payload TEXT,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS outbound_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                related_message_id TEXT,
                group_id TEXT,
                text TEXT NOT NULL,
                status_code INTEGER,
                response_body TEXT,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS webhook_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event TEXT,
                ignored INTEGER NOT NULL DEFAULT 0,
                reason TEXT,
                raw_payload TEXT,
                created_at TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                source TEXT,
                created_by TEXT,
                created_at TEXT NOT NULL
            )
        """)

        conn.commit()


def is_duplicate(message_id: str) -> bool:
    with db_connect() as conn:
        row = conn.execute(
            "SELECT 1 FROM messages WHERE message_id = ? LIMIT 1",
            (message_id,)
        ).fetchone()

    return row is not None


def save_inbound_message(message_id, group_id, sender_id, sender_name, text, raw_payload):
    with db_connect() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO messages (
                message_id,
                source,
                group_id,
                sender_id,
                sender_name,
                direction,
                text,
                raw_payload,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            message_id,
            "whatsapp",
            group_id,
            sender_id,
            sender_name,
            "inbound",
            text,
            json.dumps(raw_payload, ensure_ascii=False),
            utc_now()
        ))
        conn.commit()


def save_webhook_event(event, ignored, reason, raw_payload):
    with db_connect() as conn:
        conn.execute("""
            INSERT INTO webhook_events (
                event,
                ignored,
                reason,
                raw_payload,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            event,
            1 if ignored else 0,
            reason,
            json.dumps(raw_payload, ensure_ascii=False),
            utc_now()
        ))
        conn.commit()


def create_task(title, created_by=None, raw_text=None, normalized_text=None):
    with db_connect() as conn:
        cursor = conn.execute("""
            INSERT INTO tasks (
                title,
                status,
                source,
                created_by,
                raw_text,
                normalized_text,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            title,
            "open",
            "whatsapp",
            created_by,
            raw_text,
            normalized_text,
            utc_now()
        ))

        conn.commit()

        return cursor.lastrowid

def save_outbound_message(related_message_id, group_id, text, status_code, response_body):
    with db_connect() as conn:
        conn.execute("""
            INSERT INTO outbound_messages (
                related_message_id,
                group_id,
                text,
                status_code,
                response_body,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            related_message_id,
            group_id,
            text,
            status_code,
            response_body,
            utc_now()
        ))
        conn.commit()
def create_task(title, created_by=None, raw_text=None, normalized_text=None):
    with db_connect() as conn:
        cursor = conn.execute("""
            INSERT INTO tasks (
                title,
                status,
                source,
                raw_text,
                normalized_text,
                created_by,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            "open",
            "whatsapp",
            raw_text,
            normalized_text,
            created_by,
            utc_now()
        ))

        conn.commit()
        return cursor.lastrowid


def list_open_tasks():
    with db_connect() as conn:
        rows = conn.execute("""
            SELECT
                id,
                title
            FROM tasks
            WHERE status = 'open'
            ORDER BY id DESC
        """).fetchall()

    return rows
