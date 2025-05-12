# main.py

from ocr.document_ai_client import analyze_receipt
from ocr.text_extractor import extract_date_and_store
import os
import shutil
import json
from datetime import datetime

settings_path = "config/settings.json"
with open(settings_path, "r", encoding="utf-8") as f:
    settings = json.load(f)

# パス設定
RECEIPT_FOLDER = settings.get("receipt_folder", "receipts/")
RENAMED_FOLDER = settings.get("renamed_receipt_folder", "renamed_receipts/")
LOGS_FOLDER = settings.get("logs_folder", "logs/")
FIXED_FOLDER = os.path.join(RECEIPT_FOLDER, "fixed/")

os.makedirs(RENAMED_FOLDER, exist_ok=True)
os.makedirs(LOGS_FOLDER, exist_ok=True)
os.makedirs(FIXED_FOLDER, exist_ok=True)

# ファイルを順番に処理
for filename in os.listdir(RECEIPT_FOLDER):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        file_path = os.path.join(RECEIPT_FOLDER, filename)
        print(f"処理中: {file_path}...")

        try:
            # OCR実行
            text = analyze_receipt(file_path)

            # 日付・店名抽出
            date, store = extract_date_and_store(text)

            safe_store = store.replace(" ", "_").replace("/", "_").replace("\\", "_")
            new_filename_base = f"{date}_{safe_store}"
            new_filename = f"{new_filename_base}.jpg"
            new_path = os.path.join(RENAMED_FOLDER, new_filename)

            safe_store = store.replace(" ", "_").replace("/", "_").replace("\\", "_")
            new_filename_base = f"{date}_{safe_store}"
            new_filename = f"{new_filename_base}.jpg"
            new_path = os.path.join(RENAMED_FOLDER, new_filename)

            # 画像ファイルコピーしてリネーム
            shutil.copy(file_path, new_path)
            
            fixed_path = os.path.join(FIXED_FOLDER, filename)
            shutil.move(file_path, fixed_path)

            # OCR結果をlogsに保存
            now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = f"{new_filename_base}_{now_str}.txt"
            log_path = os.path.join(LOGS_FOLDER, log_filename)

            with open(log_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"✅ {new_filename} にリネーム & OCR結果保存しました！ 元ファイルは {fixed_path} に移動しました。")

        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
