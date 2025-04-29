## Google Cloud の設定

### Document AI API を有効にする

「API とサービス」→「API とサービスの有効化」にて、`Document AI API` を有効にする

### サービスアカウントと認証キーを作成する

1. 左メニューから「IAM と管理」→「サービスアカウント」
2. 「サービスアカウントを作成」ボタンを押す
3. サービスアカウント名を入力（例：「receipt-ocr-user」）
4. ロールは「Document AI User」を付与
5. 作成完了後、「鍵を作成」→「JSON」を選んでダウンロード
6. 認証キーを `keys/service-account.json` として配置

### プロセッサーの作成

1. 「Document AI」→「プロセッサギャラリー」から「Expense Parser」を選択
2. プロセッサーを作成
3. プロセッサー ID をコピーしておく

## ローカル環境（Python）の準備

```
pip install google-cloud-documentai
pip install google-auth
```

## ディレクトリ構成

```
receipt_ocr_project/
│
├── receipts/              # スキャンした元レシート画像たち
│   ├── 20250429_123456.jpg
│   ├── 20250429_789012.jpg
│   └── ...
│
├── renamed_receipts/       # リネーム後のレシート画像たち
│
├── keys/                   # サービスアカウントの認証キー(JSONファイル)
│   └── your-service-account.json
│
├── ocr/                    # OCR処理に関するモジュール
│   ├── __init__.py
│   ├── document_ai_client.py  # Document AIとやり取りするコード
│   └── text_extractor.py      # テキストから日付・店名を抽出するコード
│
├── main.py                 # メインの実行スクリプト
│
├── requirements.txt        # 必要なPythonライブラリ一覧
│
└── README.md               # 使い方メモ（あとから自分用に書けると◎）
```
