# ocr/text_extractor.py

import re
import json
import os

def extract_date_and_store(text: str):
    """
    OCRテキストから日付と店名を抽出する
    """
    settings_path = "config/settings.json"
    preferred_store_names = []
    excluded_store_names = []
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
                preferred_store_names = settings.get("preferred_store_names", [])
                excluded_store_names = settings.get("excluded_store_names", [])
        except Exception:
            pass

    # --- 日付を抽出 ---
    date_patterns = [
        r"(\d{4}[/-]\d{1,2}[/-]\d{1,2})",
        r"(\d{2}[/-]\d{1,2}[/-]\d{1,2})",
        r"(\d{4}年\d{1,2}月\d{1,2}日)"
    ]

    date = None
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            raw_date = match.group(1)
            raw_date = re.sub(r"[/-]", "", raw_date)
            raw_date = re.sub(r"[年月]", "", raw_date)
            raw_date = raw_date.replace("日", "")

            # 6桁（yyMMdd）だったら西暦補完
            if len(raw_date) == 6:
                raw_date = "20" + raw_date

            # yyyymmdd形式にゼロ詰め
            if len(raw_date) == 8:
                yyyy = raw_date[:4]
                mm = raw_date[4:6].zfill(2)
                dd = raw_date[6:8].zfill(2)
                date = f"{yyyy}{mm}{dd}"
            break

    # --- 店名を抽出 ---
    store = "未取得"  # デフォルト値を「未取得」に設定
    
    if preferred_store_names:
        lines = text.splitlines()
        for line in lines:
            line = line.strip()
            if line in preferred_store_names:
                store = line
                break
    
    if store == "未取得":
        lines = text.splitlines()
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and 2 <= len(line_stripped) <= 30 and not re.search(r"\d", line_stripped):
                if line_stripped not in excluded_store_names:
                    store = line_stripped
                    break

    return date, store
