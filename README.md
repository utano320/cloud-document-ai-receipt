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

## 環境準備

### Python 　の依存パッケージをインストール

```
pip install google-cloud-documentai
pip install google-auth
```

### 必要なファイルの配置

- `config/settings_default.json` をコピーして `config/settings.json`を作成し、プロジェクト ID、プロセッサー ID をセット
- `keys/service-account.json` としてサービスアカウントの認証キーを配置
- `receipts`ディレクトリ配下に元データとなるレシートの画像ファイルを配置

## ディレクトリ構成

```
cloud-document-ai-receipt/
│
├── config/                # 設定ファイル
│   └── settings.json
│
├── keys/                  # サービスアカウントの認証キー(JSONファイル)
│   └── service-account.json
│
├── logs/                  # ログファイル
│
├── ocr/                   # OCR処理に関するモジュール
│   ├── document_ai_client.py  # Document AIとやり取りするコード
│   └── text_extractor.py      # テキストから日付・店名を抽出するコード
│
├── receipts/              # スキャンした元レシート画像たち
│
├── renamed_receipts/      # リネーム後のレシート画像たち
│
├── main.py                # メインの実行スクリプト
│
├── requirements.txt       # 必要なPythonライブラリ一覧
│
└── README.md              # 使い方メモ
```

## 実行

`python main.py`
