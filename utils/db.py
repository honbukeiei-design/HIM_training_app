from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_DIR = ROOT / "db"
DB_PATH = DB_DIR / "study.db"


def get_conn() -> sqlite3.Connection:
    DB_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id TEXT NOT NULL,
                field TEXT,
                category TEXT,
                tag TEXT,
                difficulty INTEGER,
                is_correct INTEGER NOT NULL,
                selected_choice TEXT,
                correct_choice TEXT,
                elapsed_seconds REAL,
                mode TEXT DEFAULT 'practice',
                timestamp TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bookmarks (
                question_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_result(row: dict, is_correct: bool, selected_choice: str, correct_choice: str, elapsed_seconds: float | None = None, mode: str = "practice") -> None:
    init_db()
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO results
            (question_id, field, category, tag, difficulty, is_correct, selected_choice, correct_choice, elapsed_seconds, mode, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(row.get("id", "")),
                row.get("field", ""),
                row.get("category", ""),
                row.get("tag", ""),
                int(row.get("difficulty", 1)) if str(row.get("difficulty", "")).isdigit() else None,
                1 if is_correct else 0,
                selected_choice,
                correct_choice,
                elapsed_seconds,
                mode,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()


def get_results() -> pd.DataFrame:
    init_db()
    with get_conn() as conn:
        df = pd.read_sql_query("SELECT * FROM results ORDER BY timestamp DESC", conn)
    return df


def add_bookmark(question_id: str) -> None:
    init_db()
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO bookmarks (question_id, created_at) VALUES (?, ?)",
            (question_id, datetime.now().isoformat(timespec="seconds")),
        )
        conn.commit()


def remove_bookmark(question_id: str) -> None:
    init_db()
    with get_conn() as conn:
        conn.execute("DELETE FROM bookmarks WHERE question_id = ?", (question_id,))
        conn.commit()


def get_bookmarks() -> pd.DataFrame:
    init_db()
    with get_conn() as conn:
        return pd.read_sql_query("SELECT * FROM bookmarks ORDER BY created_at DESC", conn)


def reset_history() -> None:
    init_db()
    with get_conn() as conn:
        conn.execute("DELETE FROM results")
        conn.execute("DELETE FROM bookmarks")
        conn.commit()
