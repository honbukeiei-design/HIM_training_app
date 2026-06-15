from __future__ import annotations

import streamlit as st
from utils.quiz import load_sources

st.set_page_config(page_title="出典と利用条件", page_icon="📄", layout="wide")
st.title("📄 出典と利用条件")

st.markdown(
    """
    このアプリは、診療情報管理士認定試験の公式問題を転載せず、出題範囲を参考にしたオリジナル問題で構成しています。

    - 公式試験問題・公式練習問題・有料教材本文の無断転載はしないでください。
    - 院内限定教材を追加する場合は、権利者の許諾と公開範囲を確認してください。
    - GitHubで公開する場合は、`data/questions.csv` に著作権上問題のない問題のみを収録してください。
    """
)

sources = load_sources()
st.dataframe(sources, hide_index=True, use_container_width=True)
