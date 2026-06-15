from __future__ import annotations

import random
import time
import streamlit as st
from utils.quiz import load_questions, choices_from_row, correct_choice
from utils.db import save_result, add_bookmark

st.set_page_config(page_title="問題演習", page_icon="📝", layout="wide")
st.title("📝 問題演習")

questions = load_questions()

with st.sidebar:
    st.header("出題条件")
    field = st.selectbox("分野", ["すべて"] + sorted(questions["field"].dropna().unique().tolist()))
    df = questions if field == "すべて" else questions[questions["field"] == field]
    category = st.selectbox("カテゴリ", ["すべて"] + sorted(df["category"].dropna().unique().tolist()))
    if category != "すべて":
        df = df[df["category"] == category]
    tag = st.selectbox("タグ", ["すべて"] + sorted(df["tag"].dropna().unique().tolist()))
    if tag != "すべて":
        df = df[df["tag"] == tag]
    difficulty = st.multiselect("難易度", sorted(df["difficulty"].dropna().unique().tolist()), default=sorted(df["difficulty"].dropna().unique().tolist()))
    if difficulty:
        df = df[df["difficulty"].isin(difficulty)]

if df.empty:
    st.warning("条件に合う問題がありません。")
    st.stop()

if "practice_qid" not in st.session_state or st.session_state.get("practice_pool_key") != str((field, category, tag, difficulty)):
    row = df.sample(1).iloc[0]
    st.session_state.practice_qid = row["id"]
    st.session_state.practice_started = time.time()
    st.session_state.practice_pool_key = str((field, category, tag, difficulty))

row = questions[questions["id"] == st.session_state.practice_qid].iloc[0]
choices = choices_from_row(row)
correct = correct_choice(row)

st.caption(f"{row['field']} / {row['category']} / {row['tag']} / 難易度 {row['difficulty']}")
st.subheader(row["question"])
selected = st.radio("選択肢", choices, index=None)

col1, col2, col3 = st.columns([1,1,1])
with col1:
    submit = st.button("回答する", type="primary", use_container_width=True)
with col2:
    if st.button("あとで復習", use_container_width=True):
        add_bookmark(str(row["id"]))
        st.success("復習リストに追加しました。")
with col3:
    if st.button("次の問題", use_container_width=True):
        next_row = df.sample(1).iloc[0]
        st.session_state.practice_qid = next_row["id"]
        st.session_state.practice_started = time.time()
        st.rerun()

if submit:
    if selected is None:
        st.warning("選択肢を選んでください。")
    else:
        elapsed = time.time() - st.session_state.get("practice_started", time.time())
        ok = selected == correct
        save_result(row.to_dict(), ok, selected, correct, elapsed, mode="practice")
        if ok:
            st.success("正解です。")
        else:
            st.error(f"不正解です。正解: {correct}")
        st.markdown("### 解説")
        st.write(row["explanation"])
        st.markdown("### 復習ポイント")
        st.info(row["review_text"])
        st.caption(f"出典・根拠: {row['source_name']} / {row['source_detail']} / オリジナル問題: {row['is_original']} / 改変: {row['is_modified']}")
