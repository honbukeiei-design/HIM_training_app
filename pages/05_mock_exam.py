from __future__ import annotations

import random
import time
import streamlit as st
from utils.quiz import load_questions, choices_from_row, correct_choice
from utils.db import save_result

st.set_page_config(page_title="模試モード", page_icon="⏱️", layout="wide")
st.title("⏱️ 模試モード")

questions = load_questions()
field = st.selectbox("模試分野", sorted(questions["field"].unique()))
num = st.slider("出題数", min_value=10, max_value=60, value=30, step=10)

pool = questions[questions["field"] == field]
if len(pool) < num:
    st.warning("選択分野の問題数が不足しています。")
    st.stop()

if st.button("模試を開始", type="primary"):
    st.session_state.exam_ids = pool.sample(num)["id"].tolist()
    st.session_state.exam_started = time.time()
    st.session_state.exam_submitted = False

if "exam_ids" not in st.session_state:
    st.info("開始ボタンを押すと模試が始まります。")
    st.stop()

exam_df = questions[questions["id"].isin(st.session_state.exam_ids)].reset_index(drop=True)
answers = {}
with st.form("exam_form"):
    for i, row in exam_df.iterrows():
        st.markdown(f"### Q{i+1}. {row['question']}")
        answers[row["id"]] = st.radio("選択肢", choices_from_row(row), key=f"exam_{row['id']}", index=None)
    submitted = st.form_submit_button("採点する", type="primary")

if submitted:
    correct_count = 0
    elapsed = time.time() - st.session_state.get("exam_started", time.time())
    for _, row in exam_df.iterrows():
        selected = answers[row["id"]]
        correct = correct_choice(row)
        ok = selected == correct
        correct_count += int(ok)
        save_result(row.to_dict(), ok, selected or "未回答", correct, elapsed / max(len(exam_df), 1), mode="mock_exam")
    rate = correct_count / len(exam_df) * 100
    st.session_state.exam_submitted = True
    st.success(f"採点完了: {correct_count}/{len(exam_df)} 問 正解（{rate:.1f}%）")
    st.write("目安: 70%以上で合格圏、80%以上で安定圏として復習計画を立ててください。")
    with st.expander("解説を表示"):
        for i, row in exam_df.iterrows():
            st.markdown(f"**Q{i+1}. {row['question']}**")
            st.write(f"正解: {correct_choice(row)}")
            st.write(row["explanation"])
