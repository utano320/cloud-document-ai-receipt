# ocr/text_extractor.py

import re
from ocr.document_ai_client import MIN_YEAR, MAX_YEAR, DEFAULT_YEAR

def extract_date_and_store(text: str):
    """
    OCRテキストから日付と店名を抽出する
    """

    # --- 日付を抽出 ---
    date_patterns = [
        r"(\d{4}[/-]\d{1,2}[/-]\d{1,2})",
        r"(\d{2}[/-]\d{1,2}[/-]\d{1,2})",
        r"(\d{4}年\d{1,2}月\d{1,2}日)"
    ]

    all_dates = []

    for pattern in date_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
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
    store = None
    lines = text.splitlines()
    for line in lines:
        if 2 <= len(line.strip()) <= 30 and not re.search(r"\d", line):
            store = line.strip()
            break

    return date, store
