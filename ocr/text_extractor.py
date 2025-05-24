# ocr/text_extractor.py

import re
from ocr.document_ai_client import MIN_YEAR, MAX_YEAR, DEFAULT_YEAR
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
        r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)",
        r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)",  # with weekday in parentheses
        r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)\s*\d{1,2}:\d{2}",  # with weekday and time
        r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)\s*\d{1,2}:\d{2}[^0-9]*"  # with weekday, time and trailing chars
    ]

    all_dates = []

    for pattern in date_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            raw_date = match.group(1)
            
            if '/' in raw_date or '-' in raw_date:
                parts = re.split(r'[/-]', raw_date)
                if len(parts) == 3:
                    year = parts[0]
                    month = parts[1]
                    day = parts[2]
                    
                    if len(year) == 2:
                        year = "20" + year
                        
                    month = month.zfill(2)
                    day = day.zfill(2)
                    
                    raw_date = f"{year}{month}{day}"
            else:
                raw_date = re.sub(r"[年月]", "", raw_date)
                raw_date = raw_date.replace("日", "")
                raw_date = raw_date.replace(" ", "")
                
                year_match = re.search(r'^(\d{4})', raw_date)
                if year_match:
                    year = year_match.group(1)
                    remaining = raw_date[4:]
                    
                    if len(remaining) >= 2:
                        if len(remaining) >= 3 and remaining[1].isdigit():
                            month = remaining[:2]
                            day = remaining[2:].zfill(2)
                        else:
                            month = remaining[0].zfill(2)
                            day = remaining[1:].zfill(2)
                        
                        raw_date = f"{year}{month}{day}"

            # 6桁（yyMMdd）だったら西暦補完
            if len(raw_date) == 6:
                raw_date = "20" + raw_date

            if len(raw_date) == 8:
                yyyy = raw_date[:4]
                mm = raw_date[4:6]
                dd = raw_date[6:8]
                
                year_valid = MIN_YEAR <= int(yyyy) <= MAX_YEAR
                
                normalized_date = f"{yyyy}{mm}{dd}"
                all_dates.append((normalized_date, year_valid, mm, dd))

    date = None
    
    valid_dates = [d for d in all_dates if d[1]]
    
    if valid_dates:
        date = valid_dates[0][0]
    elif all_dates:
        first_date = all_dates[0]
        mm = first_date[2]
        dd = first_date[3]
        date = f"{DEFAULT_YEAR}{mm}{dd}"
    else:
        date = f"{DEFAULT_YEAR}0101"

    # --- 店名を抽出 ---
    store = "未取得"  # デフォルト値を「未取得」に設定
    
    if preferred_store_names:
        lines = text.splitlines()
        for line in lines:
            line = line.strip()
            for preferred_name in preferred_store_names:
                if preferred_name in line:
                    store = line
                    break
            if store != "未取得":
                break
    
    if store == "未取得":
        lines = text.splitlines()
        for line in lines:
            line_stripped = line.strip()
            if line_stripped and 2 <= len(line_stripped) <= 30 and not re.search(r"\d", line_stripped):
                is_excluded = False
                for excluded_name in excluded_store_names:
                    if excluded_name in line_stripped:
                        is_excluded = True
                        break
                if not is_excluded:
                    store = line_stripped
                    break

    return date, store
