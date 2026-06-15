# 診療情報管理士 資格支援アプリ

公式出題範囲に準拠したオリジナル問題版の Streamlit アプリです。

## 特徴

- オリジナル問題 1,000問
- 用語集 300語
- 基礎分野・専門分野対応
- 問題演習
- 分野別学習
- 苦手分析
- 復習モード
- 模試モード
- 統計ダッシュボード
- CSVアップロード管理
- 出典と利用条件ページ

## 文字化け対策

Streamlit Cloud や GitHub の環境差による文字化けを避けるため、Python ファイル名はすべて英数字にしています。
画面表示は日本語です。

## ローカル起動

```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub / Streamlit Cloud

1. このフォルダを GitHub リポジトリへアップロード
2. Streamlit Cloud でリポジトリを選択
3. Main file path に `app.py` を指定
4. Deploy

## データ形式

`data/questions.csv` を差し替えることで問題を追加できます。
UTF-8 with BOM で保存すると Excel でも扱いやすくなります。

必要列:

```text
id,field,category,tag,difficulty,question,c1,c2,c3,c4,answer,explanation,review_text,source_name,source_detail,source_url,is_original,is_modified
```

## 著作権・利用上の注意

本アプリの同梱問題は、診療情報管理士認定試験の公式問題本文を転載せず、出題範囲を参考に独自作成したオリジナル問題です。

GitHub等で公開する場合は、以下を避けてください。

- 公式試験問題の全文転載
- 公式練習問題の転載
- 有料教材本文・図表・設問の転載
- 許諾のない院内資料の公開

院内限定利用で独自教材を追加する場合も、権利関係と公開範囲を確認してください。
