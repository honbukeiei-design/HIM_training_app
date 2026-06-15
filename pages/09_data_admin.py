from __future__ import annotations

from pathlib import Path
import streamlit as st
import pandas as pd
from utils.quiz import REQUIRED_COLUMNS, load_questions

st.set_page_config(page_title="データ管理", page_icon="🗂️", layout="wide")
st.title("🗂️ データ管理")

ROOT = Path(__file__).resolve().parents[1]
QUESTION_PATH = ROOT / "data" / "questions.csv"

st.subheader("現在の問題データ")
try:
    df = load_questions()
    st.success(f"読み込み成功: {len(df):,} 問")
    st.dataframe(df.head(50), hide_index=True, use_container_width=True)
except Exception as e:
    st.error(e)

st.subheader("CSVアップロード")
st.write("同じ列構成のCSVをアップロードすると、問題データを差し替えできます。")
uploaded = st.file_uploader("questions.csv", type=["csv"])
if uploaded is not None:
    new_df = pd.read_csv(uploaded, encoding="utf-8-sig")
    missing = [c for c in REQUIRED_COLUMNS if c not in new_df.columns]
    if missing:
        st.error(f"必要な列が不足しています: {missing}")
    else:
        st.dataframe(new_df.head(), hide_index=True, use_container_width=True)
        if st.button("このCSVで差し替える", type="primary"):
            new_df.to_csv(QUESTION_PATH, index=False, encoding="utf-8-sig")
            st.success("差し替えました。アプリを再読み込みしてください。")

st.subheader("必要な列")
st.code(",".join(REQUIRED_COLUMNS))
