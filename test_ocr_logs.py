import os
import sys
import re
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

MIN_YEAR = 2000
MAX_YEAR = 2030
DEFAULT_YEAR = 2023

date_patterns = [
    r"(\d{4}[/-]\d{1,2}[/-]\d{1,2})",
    r"(\d{2}[/-]\d{1,2}[/-]\d{1,2})",
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)",
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)",  # with weekday in parentheses
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)\s*\d{1,2}:\d{2}",  # with weekday and time
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)\s*\d{1,2}:\d{2}[^0-9]*"  # with weekday, time and trailing chars
]

def extract_date_and_store(text):
    """
    OCRテキストから日付と店名を抽出する
    (Simplified version without external dependencies)
    """
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

    store = "未取得"  # デフォルト値を「未取得」に設定
    
    lines = text.splitlines()
    for line in lines:
        line_stripped = line.strip()
        if line_stripped and 2 <= len(line_stripped) <= 30 and not re.search(r"\d", line_stripped):
            store = line_stripped
            break

    return date, store

def test_with_sample_data():
    """Test date extraction with sample OCR data"""
    sample_file = "sample_ocr_data.txt"
    
    if not os.path.exists(sample_file):
        print(f"Error: Sample file {sample_file} not found.")
        return
    
    with open(sample_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    receipts = content.split("---")
    
    print("Testing date extraction with sample OCR data...")
    print("-" * 50)
    
    for i, receipt in enumerate(receipts):
        if not receipt.strip():
            continue
            
        print(f"Receipt #{i+1}:")
        print(receipt[:100] + "..." if len(receipt) > 100 else receipt)
        
        date, store = extract_date_and_store(receipt)
        
        is_valid_format = len(date) == 8 and date.isdigit()
        
        print(f"Extracted date: {date}")
        print(f"Extracted store: {store}")
        print(f"Is date in YYYYMMDD format: {'Yes' if is_valid_format else 'No'}")
        
        if is_valid_format:
            year = date[:4]
            month = date[4:6]
            day = date[6:8]
            print(f"Formatted date: {year}-{month}-{day}")
        
        print("-" * 50)

def test_with_logs():
    """Test date extraction with actual OCR log files"""
    logs_folder = "logs"
    
    if not os.path.exists(logs_folder) or not os.path.isdir(logs_folder):
        print(f"Error: Logs folder {logs_folder} not found.")
        return
    
    log_files = [f for f in os.listdir(logs_folder) if f.endswith(".txt") and f != ".gitkeep"]
    
    if not log_files:
        print(f"No log files found in {logs_folder}.")
        return
    
    print("Testing date extraction with OCR log files...")
    print("-" * 50)
    
    for log_file in log_files:
        log_path = os.path.join(logs_folder, log_file)
        
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        print(f"Log file: {log_file}")
        print(content[:100] + "..." if len(content) > 100 else content)
        
        date, store = extract_date_and_store(content)
        
        is_valid_format = len(date) == 8 and date.isdigit()
        
        print(f"Extracted date: {date}")
        print(f"Extracted store: {store}")
        print(f"Is date in YYYYMMDD format: {'Yes' if is_valid_format else 'No'}")
        
        if is_valid_format:
            year = date[:4]
            month = date[4:6]
            day = date[6:8]
            print(f"Formatted date: {year}-{month}-{day}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_with_sample_data()
    
    test_with_logs()
