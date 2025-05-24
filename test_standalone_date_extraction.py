import re
import os
import sys

MIN_YEAR = 2000
MAX_YEAR = 2030
DEFAULT_YEAR = 2023

sample_texts = [
    """
    レシート
    
    2025年4月10日(木) 02:15
    領収書
    
    株式会社サンプルストア
    東京都渋谷区サンプル町1-2-3
    TEL: 03-1234-5678
    """,
    """
    レシート
    
    2025年10月1日
    領収書
    
    サンプルマート
    大阪府大阪市サンプル区5-6-7
    TEL: 06-9876-5432
    """,
    """
    レシート
    
    2025/4/10
    領収書
    
    サンプルショップ
    名古屋市サンプル区8-9-10
    TEL: 052-123-4567
    """,
    """
    レシート
    
    2025/10/1
    領収書
    
    サンプルストア札幌
    北海道札幌市サンプル区11-12-13
    TEL: 011-234-5678
    """
]

date_patterns = [
    r"(\d{4}[/-]\d{1,2}[/-]\d{1,2})",
    r"(\d{2}[/-]\d{1,2}[/-]\d{1,2})",
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)",
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)",  # with weekday in parentheses
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)\s*\d{1,2}:\d{2}",  # with weekday and time
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)\s*\d{1,2}:\d{2}[^0-9]*"  # with weekday, time and trailing chars
]

def extract_date_current(text):
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

            if len(raw_date) == 6:
                raw_date = "20" + raw_date

            if len(raw_date) == 8:
                yyyy = raw_date[:4]
                mm = raw_date[4:6]
                dd = raw_date[6:8]
                
                year_valid = MIN_YEAR <= int(yyyy) <= MAX_YEAR
                
                normalized_date = f"{yyyy}{mm}{dd}"
                all_dates.append((normalized_date, year_valid, mm, dd))
    
    if all_dates:
        valid_dates = [d for d in all_dates if d[1]]
        if valid_dates:
            return valid_dates[0][0]
        else:
            first_date = all_dates[0]
            mm = first_date[2]
            dd = first_date[3]
            return f"{DEFAULT_YEAR}{mm}{dd}"
    else:
        return f"{DEFAULT_YEAR}0101"

def extract_date_fixed(text):
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
                    
                    normalized_date = f"{year}{month}{day}"
                    
                    year_valid = MIN_YEAR <= int(year) <= MAX_YEAR
                    all_dates.append((normalized_date, year_valid, month, day))
            else:
                year_match = re.search(r'(\d{4})年', raw_date)
                month_match = re.search(r'(\d{1,2})月', raw_date)
                day_match = re.search(r'(\d{1,2})日', raw_date)
                
                if year_match and month_match and day_match:
                    year = year_match.group(1)
                    month = month_match.group(1).zfill(2)  # ゼロ詰め
                    day = day_match.group(1).zfill(2)      # ゼロ詰め
                    
                    normalized_date = f"{year}{month}{day}"
                    
                    year_valid = MIN_YEAR <= int(year) <= MAX_YEAR
                    all_dates.append((normalized_date, year_valid, month, day))
    
    if all_dates:
        valid_dates = [d for d in all_dates if d[1]]
        if valid_dates:
            return valid_dates[0][0]
        else:
            first_date = all_dates[0]
            mm = first_date[2]
            dd = first_date[3]
            return f"{DEFAULT_YEAR}{mm}{dd}"
    else:
        return f"{DEFAULT_YEAR}0101"

print("Testing date extraction with sample OCR data...")
print("-" * 50)

for i, text in enumerate(sample_texts):
    print(f"Sample #{i+1}:")
    print(text[:100] + "..." if len(text) > 100 else text)
    
    date_current = extract_date_current(text)
    print(f"Current implementation result: {date_current}")
    if date_current:
        year = date_current[:4]
        month = date_current[4:6]
        day = date_current[6:8]
        print(f"Formatted date (current): {year}-{month}-{day}")
    
    date_fixed = extract_date_fixed(text)
    print(f"Fixed implementation result: {date_fixed}")
    if date_fixed:
        year = date_fixed[:4]
        month = date_fixed[4:6]
        day = date_fixed[6:8]
        print(f"Formatted date (fixed): {year}-{month}-{day}")
    
    print("-" * 50)

print("Test completed.")
