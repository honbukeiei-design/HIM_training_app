from __future__ import annotations

import pandas as pd


def safe_rate(series: pd.Series) -> float:
    if len(series) == 0:
        return 0.0
    return float(series.mean())


def category_summary(results: pd.DataFrame) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame(columns=["field", "category", "attempts", "accuracy"])
    g = results.groupby(["field", "category"], dropna=False)["is_correct"]
    out = g.agg(attempts="count", accuracy="mean").reset_index()
    out["accuracy"] = (out["accuracy"] * 100).round(1)
    return out.sort_values(["accuracy", "attempts"], ascending=[True, False])


def weak_questions(results: pd.DataFrame) -> pd.DataFrame:
    if results.empty:
        return pd.DataFrame(columns=["question_id", "wrong_count", "attempts", "accuracy"])
    g = results.groupby("question_id")["is_correct"]
    out = g.agg(attempts="count", accuracy="mean").reset_index()
    wrong = results[results["is_correct"] == 0].groupby("question_id").size().rename("wrong_count")
    out = out.merge(wrong, on="question_id", how="left").fillna({"wrong_count": 0})
    out["accuracy"] = (out["accuracy"] * 100).round(1)
    return out[out["wrong_count"] > 0].sort_values(["wrong_count", "accuracy"], ascending=[False, True])
