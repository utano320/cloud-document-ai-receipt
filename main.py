# main.py

from ocr.document_ai_client import analyze_receipt
from ocr.text_extractor import extract_date_and_store
import os
import shutil
import json
from datetime import datetime

# パス設定
RECEIPT_FOLDER = "receipts/"
RENAMED_FOLDER = "renamed_receipts/"
LOGS_FOLDER = "logs/"

os.makedirs(RENAMED_FOLDER, exist_ok=True)
os.makedirs(LOGS_FOLDER, exist_ok=True)

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

            if date and store:
                safe_store = store.replace(" ", "_").replace("/", "_").replace("\\", "_")
                new_filename_base = f"{date}_{safe_store}"
                new_filename = f"{new_filename_base}.jpg"
                new_path = os.path.join(RENAMED_FOLDER, new_filename)

                # 画像ファイルコピーしてリネーム
                shutil.copy(file_path, new_path)

                # OCR結果をlogsに保存
                now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                log_filename = f"{new_filename_base}_{now_str}.json"
                log_path = os.path.join(LOGS_FOLDER, log_filename)

                with open(log_path, "w", encoding="utf-8") as f:
                    json.dump({"text": text}, f, ensure_ascii=False, indent=2)

                print(f"✅ {new_filename} にリネーム & OCR結果保存しました！")

            else:
                print(f"⚠️ 日付か店名の抽出に失敗しました: {filename}")

        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
