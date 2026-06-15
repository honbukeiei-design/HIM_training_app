from __future__ import annotations

import pandas as pd
import streamlit as st
import plotly.express as px
from utils.db import get_results, reset_history

st.set_page_config(page_title="統計ダッシュボード", page_icon="📊", layout="wide")
st.title("📊 統計ダッシュボード")

results = get_results()
if results.empty:
    st.info("まだ学習履歴がありません。")
    st.stop()

results["date"] = pd.to_datetime(results["timestamp"]).dt.date

daily = results.groupby("date").agg(attempts=("id", "count"), accuracy=("is_correct", "mean")).reset_index()
daily["accuracy"] = daily["accuracy"] * 100

fig1 = px.line(daily, x="date", y="attempts", markers=True, labels={"date":"日付", "attempts":"演習数"})
st.plotly_chart(fig1, use_container_width=True)
fig2 = px.line(daily, x="date", y="accuracy", markers=True, labels={"date":"日付", "accuracy":"正答率(%)"})
st.plotly_chart(fig2, use_container_width=True)

st.subheader("学習履歴")
st.dataframe(results, hide_index=True, use_container_width=True)

with st.expander("履歴をリセット"):
    st.warning("リセットすると学習履歴とブックマークが削除されます。")
    if st.button("リセットする"):
        reset_history()
        st.success("リセットしました。")
        st.rerun()
