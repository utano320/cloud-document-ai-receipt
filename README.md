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
- レシートの入出力フォルダのパスを設定（デフォルトは `"receipt_folder": "receipts/"`, `"renamed_receipt_folder": "renamed_receipts/"`, `"logs_folder": "logs/"`）
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
├── cleanup.sh             # ログと画像ファイルのクリーンアップスクリプト
│
├── requirements.txt       # 必要なPythonライブラリ一覧
│
└── README.md              # 使い方メモ
```

## 実行

`python main.py`

## クリーンアップ

処理済みのファイルをクリーンアップするには、`cleanup.sh` スクリプトを使用します。

### 基本的な使用方法

```bash
# logsディレクトリのtxtファイルとrenamed_receiptsディレクトリの画像ファイルを削除
./cleanup.sh
```

このコマンドは以下の処理を行います：
- `logs/` ディレクトリ内の `.txt` ファイルを削除
- `renamed_receipts/` ディレクトリ内の画像ファイル (`.jpg`, `.jpeg`, `.png`) を削除
- 削除したファイル数を表示

### 全てのファイルを削除

```bash
# logsディレクトリ、renamed_receiptsディレクトリ、receiptsディレクトリの全ファイルを削除
./cleanup.sh --all
```

`--all` オプションを使用すると、上記に加えて：
- `receipts/` ディレクトリ内の画像ファイルも削除します

注意: デフォルトでは `receipts/` ディレクトリのファイルは削除されません。
