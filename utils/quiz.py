from __future__ import annotations

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
QUESTION_PATH = ROOT / "data" / "questions.csv"
GLOSSARY_PATH = ROOT / "data" / "glossary.csv"
SOURCE_PATH = ROOT / "data" / "source_master.csv"

REQUIRED_COLUMNS = [
    "id", "field", "category", "tag", "difficulty", "question",
    "c1", "c2", "c3", "c4", "answer", "explanation", "review_text",
    "source_name", "source_detail", "source_url", "is_original", "is_modified"
]


def load_questions() -> pd.DataFrame:
    df = pd.read_csv(QUESTION_PATH, encoding="utf-8-sig")
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"questions.csv に必要な列がありません: {missing}")
    df["difficulty"] = pd.to_numeric(df["difficulty"], errors="coerce").fillna(1).astype(int)
    df["answer"] = pd.to_numeric(df["answer"], errors="coerce").fillna(1).astype(int)
    return df


def load_glossary() -> pd.DataFrame:
    return pd.read_csv(GLOSSARY_PATH, encoding="utf-8-sig")


def load_sources() -> pd.DataFrame:
    return pd.read_csv(SOURCE_PATH, encoding="utf-8-sig")


def choices_from_row(row) -> list[str]:
    return [str(row["c1"]), str(row["c2"]), str(row["c3"]), str(row["c4"])]


def correct_choice(row) -> str:
    choices = choices_from_row(row)
    idx = int(row["answer"]) - 1
    if idx < 0 or idx >= len(choices):
        return choices[0]
    return choices[idx]
