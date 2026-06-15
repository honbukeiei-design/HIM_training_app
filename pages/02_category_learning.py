from __future__ import annotations

import streamlit as st
from utils.quiz import load_questions

st.set_page_config(page_title="分野別学習", page_icon="📚", layout="wide")
st.title("📚 分野別学習")

questions = load_questions()
field = st.selectbox("分野を選択", sorted(questions["field"].unique()))
df = questions[questions["field"] == field]

summary = df.groupby(["category", "tag"]).size().reset_index(name="問題数")
st.dataframe(summary, hide_index=True, use_container_width=True)

st.markdown("### 学習の目安")
for cat in sorted(df["category"].unique()):
    with st.expander(cat):
        tags = sorted(df[df["category"] == cat]["tag"].unique())
        st.write(" / ".join(tags))
        st.write("問題演習ページでカテゴリ・タグを指定すると、この領域だけを集中演習できます。")
