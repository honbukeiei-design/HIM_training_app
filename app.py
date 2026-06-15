from __future__ import annotations

import streamlit as st
import pandas as pd
from utils.db import init_db, get_results
from utils.quiz import load_questions

st.set_page_config(
    page_title="診療情報管理士 資格支援アプリ",
    page_icon="📘",
    layout="wide",
)

init_db()

st.title("📘 診療情報管理士 資格支援アプリ")
st.caption("公式出題範囲に準拠したオリジナル問題版 / GitHub・Streamlit Cloud 公開対応")

try:
    questions = load_questions()
except Exception as e:
    st.error(f"問題データの読み込みに失敗しました: {e}")
    st.stop()

results = get_results()

c1, c2, c3, c4 = st.columns(4)
c1.metric("収録問題数", f"{len(questions):,} 問")
c2.metric("学習履歴", f"{len(results):,} 回")
if len(results):
    c3.metric("全体正答率", f"{results['is_correct'].mean()*100:.1f}%")
    today = pd.Timestamp.now().date().isoformat()
    today_count = results[results["timestamp"].str.startswith(today)].shape[0]
    c4.metric("今日の演習", f"{today_count:,} 問")
else:
    c3.metric("全体正答率", "- %")
    c4.metric("今日の演習", "0 問")

st.divider()

left, right = st.columns([1.2, 1])
with left:
    st.subheader("このアプリでできること")
    st.markdown(
        """
        - 基礎分野・専門分野の問題演習
        - 分野タグ別の集中学習
        - 間違えた問題の復習
        - 模試形式での実力確認
        - 苦手分野の分析
        - 用語集・復習テキストによる確認
        - CSV差し替えによる問題追加
        """
    )

with right:
    st.subheader("収録分野")
    field_counts = questions.groupby("field").size().reset_index(name="問題数")
    st.dataframe(field_counts, hide_index=True, use_container_width=True)

st.info(
    "このアプリは診療情報管理士認定試験の公式問題を転載せず、公開可能性に配慮したオリジナル問題で構成しています。"
)
