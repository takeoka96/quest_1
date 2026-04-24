# 課題1：女性が活躍する企業・社会への変革を提言せよ

## プロジェクト概要

EDINETの有価証券報告書データを分析し、建設業界および日揮ホールディングスの
女性活躍状況を定量的に把握した上で、変革に向けた提言を行う。

## 成果物

- `notebooks/01_edinet_data_collection.ipynb` - データ収集・前処理
- `notebooks/02_eda_visualization.ipynb` - EDA・可視化・モデル分析
- `docs/提言書.md` - 提言書
- `docs/presentation.pptx` - プレゼンテーション資料

## 分析の流れ

1. EDINETからデータ取得（建設業142社・全業界845社）
2. 業界横断分析（建設業ワースト2位を確認）
3. クラスタリング・相関分析
4. LightGBM・SHAP・LIME分析
5. 国際比較
6. 提言策定

## 環境構築

```bash
# リポジトリのクローン
git clone [リポジトリURL]
cd quest_1

# 仮想環境の作成（Python 3.11推奨）
python -m venv .venv311
source .venv311/bin/activate

# ライブラリのインストール
pip install -r requirements.txt
```

## 使用データ

- EDINET（金融庁）有価証券報告書データ（2024年）
- 労働政策研究・研修機構「データブック国際労働比較2025」
- Global Gender Gap Report 2024（World Economic Forum）
- 日揮ホールディングス株式会社「JGC Report 2025」

## 主な分析結果

- 建設業の女性管理職比率は全30業界中ワースト2位（3.0%）
- 日揮HDは建設業内では先進グループだが絶対値は3.3%と低水準
- SHAP分析より企業規模（売上高）が最重要因子
- 国際水準（スウェーデン43.7%）と比較して約14分の1

## 注意事項

- `.env`ファイルにEDINET APIキーの設定が必要
- `data/`フォルダはGitの管理外（`.gitignore`参照）
- データ収集セルは初回のみ実行（約30分）