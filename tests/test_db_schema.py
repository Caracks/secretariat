import sqlite3

from core import database


def test_init_db_creates_blocked_chats_table(monkeypatch, tmp_path):
    database_path = tmp_path / "test.db"

    monkeypatch.setattr(
        database.Settings,
        "db_path",
        str(database_path),
    )

    database.init_db()

    with sqlite3.connect(database_path) as conn:
        row = conn.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'blocked_chats'
            """
        ).fetchone()

    assert row is not None