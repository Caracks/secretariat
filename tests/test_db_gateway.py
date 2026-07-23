import sqlite3

from core.database import execute, execute_many, fetch_all, fetch_one


def create_example_table(db_path: str) -> None:
    execute(
        """
        CREATE TABLE example_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,git add core/database.py tests/test_database_gateway.py
git commit -m "refactor: add reusable SQLite database gateway"
            name TEXT NOT NULL
        )
        """,
        db_path=db_path,
    )


def test_execute_creates_and_writes_data(tmp_path):
    db_path = str(tmp_path / "database.db")
    create_example_table(db_path)

    inserted_id = execute(
        """
        INSERT INTO example_items (name)
        VALUES (?)
        """,
        ("first",),
        db_path=db_path,
    )

    assert inserted_id == 1


def test_fetch_one_returns_named_row(tmp_path):
    db_path = str(tmp_path / "database.db")
    create_example_table(db_path)

    execute(
        """
        INSERT INTO example_items (name)
        VALUES (?)
        """,
        ("first",),
        db_path=db_path,
    )

    row = fetch_one(
        """
        SELECT id, name
        FROM example_items
        WHERE id = ?
        """,
        (1,),
        db_path=db_path,
    )

    assert row is not None
    assert row["id"] == 1
    assert row["name"] == "first"


def test_fetch_one_returns_none_when_not_found(tmp_path):
    db_path = str(tmp_path / "database.db")
    create_example_table(db_path)

    row = fetch_one(
        """
        SELECT id, name
        FROM example_items
        WHERE id = ?
        """,
        (999,),
        db_path=db_path,
    )

    assert row is None


def test_fetch_all_returns_rows(tmp_path):
    db_path = str(tmp_path / "database.db")
    create_example_table(db_path)

    execute_many(
        """
        INSERT INTO example_items (name)
        VALUES (?)
        """,
        [
            ("first",),
            ("second",),
        ],
        db_path=db_path,
    )

    rows = fetch_all(
        """
        SELECT id, name
        FROM example_items
        ORDER BY id
        """,
        db_path=db_path,
    )

    assert [row["name"] for row in rows] == [
        "first",
        "second",
    ]


def test_foreign_keys_are_enabled(tmp_path):
    db_path = str(tmp_path / "database.db")

    execute(
        """
        CREATE TABLE parents (
            id INTEGER PRIMARY KEY
        )
        """,
        db_path=db_path,
    )

    execute(
        """
        CREATE TABLE children (
            id INTEGER PRIMARY KEY,
            parent_id INTEGER NOT NULL,
            FOREIGN KEY (parent_id) REFERENCES parents(id)
        )
        """,
        db_path=db_path,
    )

    try:
        execute(
            """
            INSERT INTO children (id, parent_id)
            VALUES (?, ?)
            """,
            (1, 999),
            db_path=db_path,
        )
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("Foreign key constraint was not enforced")