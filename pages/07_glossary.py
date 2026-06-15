from __future__ import annotations

import streamlit as st
from utils.quiz import load_glossary

st.set_page_config(page_title="用語集", page_icon="🔎", layout="wide")
st.title("🔎 用語集")

glossary = load_glossary()
keyword = st.text_input("キーワード検索")
field = st.selectbox("分野", ["すべて"] + sorted(glossary["field"].dropna().unique().tolist()))

df = glossary.copy()
if field != "すべて":
    df = df[df["field"] == field]
if keyword:
    mask = df.apply(lambda r: keyword.lower() in " ".join(map(str, r.values)).lower(), axis=1)
    df = df[mask]

st.dataframe(df, hide_index=True, use_container_width=True)
