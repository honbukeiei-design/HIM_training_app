from __future__ import annotations

import time
import streamlit as st
from utils.db import get_results, get_bookmarks, save_result
from utils.quiz import load_questions, choices_from_row, correct_choice
from utils.analysis import weak_questions

st.set_page_config(page_title="復習モード", page_icon="🔁", layout="wide")
st.title("🔁 復習モード")

questions = load_questions()
results = get_results()
bookmarks = get_bookmarks()

mode = st.radio("復習対象", ["間違えた問題", "あとで復習に登録した問題"], horizontal=True)

if mode == "間違えた問題":
    weak = weak_questions(results)
    ids = weak["question_id"].tolist() if not weak.empty else []
else:
    ids = bookmarks["question_id"].tolist() if not bookmarks.empty else []

review_df = questions[questions["id"].isin(ids)]

if review_df.empty:
    st.success("復習対象はありません。")
    st.stop()

if "review_qid" not in st.session_state or st.session_state.review_qid not in review_df["id"].tolist():
    row = review_df.sample(1).iloc[0]
    st.session_state.review_qid = row["id"]
    st.session_state.review_started = time.time()

row = questions[questions["id"] == st.session_state.review_qid].iloc[0]
choices = choices_from_row(row)
correct = correct_choice(row)

st.caption(f"{row['field']} / {row['category']} / {row['tag']}")
st.subheader(row["question"])
selected = st.radio("選択肢", choices, index=None)

col1, col2 = st.columns(2)
with col1:
    submit = st.button("回答する", type="primary", use_container_width=True)
with col2:
    if st.button("別の復習問題へ", use_container_width=True):
        row2 = review_df.sample(1).iloc[0]
        st.session_state.review_qid = row2["id"]
        st.session_state.review_started = time.time()
        st.rerun()

if submit:
    if selected is None:
        st.warning("選択肢を選んでください。")
    else:
        ok = selected == correct
        elapsed = time.time() - st.session_state.get("review_started", time.time())
        save_result(row.to_dict(), ok, selected, correct, elapsed, mode="review")
        st.success("正解です。") if ok else st.error(f"不正解です。正解: {correct}")
        st.write(row["explanation"])
        st.info(row["review_text"])
