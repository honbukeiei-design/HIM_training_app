from __future__ import annotations

import streamlit as st
import plotly.express as px
from utils.db import get_results
from utils.quiz import load_questions
from utils.analysis import category_summary, weak_questions

st.set_page_config(page_title="苦手分析", page_icon="📉", layout="wide")
st.title("📉 苦手分析")

results = get_results()
questions = load_questions()

if results.empty:
    st.info("まだ学習履歴がありません。問題演習を行うと分析できます。")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("演習回数", f"{len(results):,}")
c2.metric("正答率", f"{results['is_correct'].mean()*100:.1f}%")
c3.metric("不正解数", f"{(results['is_correct']==0).sum():,}")

st.subheader("分野・カテゴリ別正答率")
summary = category_summary(results)
fig = px.bar(summary, x="category", y="accuracy", color="field", hover_data=["attempts"], labels={"accuracy":"正答率(%)", "category":"カテゴリ"})
st.plotly_chart(fig, use_container_width=True)
st.dataframe(summary, hide_index=True, use_container_width=True)

st.subheader("苦手問題")
weak = weak_questions(results).head(30)
if weak.empty:
    st.success("苦手問題はまだありません。")
else:
    merged = weak.merge(questions[["id", "question", "field", "category", "tag", "explanation"]], left_on="question_id", right_on="id", how="left")
    st.dataframe(merged[["question_id", "field", "category", "tag", "wrong_count", "attempts", "accuracy", "question"]], hide_index=True, use_container_width=True)
