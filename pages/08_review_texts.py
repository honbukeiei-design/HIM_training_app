from __future__ import annotations

from pathlib import Path
import streamlit as st

st.set_page_config(page_title="復習テキスト", page_icon="📖", layout="wide")
st.title("📖 復習テキスト")

ROOT = Path(__file__).resolve().parents[1]
texts = {
    "基礎分野": ROOT / "texts" / "basic_review.md",
    "専門分野": ROOT / "texts" / "specialist_review.md",
    "統計・情報セキュリティ": ROOT / "texts" / "statistics_security_review.md",
}
selected = st.selectbox("テキストを選択", list(texts.keys()))
st.markdown(texts[selected].read_text(encoding="utf-8"))
