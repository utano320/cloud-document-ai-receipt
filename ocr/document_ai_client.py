# ocr/document_ai_client.py

from google.cloud import documentai_v1 as documentai
import os
import json

# 環境変数に認証情報JSONファイルのパスをセット
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "keys/service-account.json"

# 設定ファイルを読む
with open("config/settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)

PROJECT_ID = settings["project_id"]
LOCATION = settings["location"]
PROCESSOR_ID = settings["processor_id"]

def analyze_receipt(file_path: str) -> str:
    """
    レシート画像をDocument AIに送り、解析結果のテキストを返す
    """
    client = documentai.DocumentProcessorServiceClient()

    with open(file_path, "rb") as image_file:
        image_content = image_file.read()

    name = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"

    document = {"content": image_content, "mime_type": "image/jpeg"}

    request = {"name": name, "raw_document": document}

    result = client.process_document(request=request)

    document = result.document

    return document.text
