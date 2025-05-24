import os
import sys
import re
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from ocr.text_extractor import extract_date_and_store
    from ocr.document_ai_client import MIN_YEAR, MAX_YEAR, DEFAULT_YEAR
    print("Using project imports")
except ImportError:
    print("Using local implementation due to import error")
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

def create_sample_ocr_logs():
    """Create sample OCR log files if logs directory is empty"""
    logs_folder = "logs"
    
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
    
    log_files = [f for f in os.listdir(logs_folder) if f != ".gitkeep"]
    
    if not log_files:
        print("Creating sample OCR log files...")
        
        sample_data = [
            {
                "date": "2025年4月10日",
                "store": "サンプルストア",
                "content": """レシート

2025年4月10日(木) 02:15
領収書

株式会社サンプルストア
東京都渋谷区サンプル町1-2-3
TEL: 03-1234-5678

商品名          数量  単価   金額
---------------------------------
サンプル商品A    1   1,000  1,000
サンプル商品B    2     500  1,000
---------------------------------
小計                      2,000
消費税(10%)                 200
合計                      2,200

お支払い: 現金
ありがとうございました。"""
            },
            {
                "date": "2025年10月1日",
                "store": "サンプルマート",
                "content": """レシート

2025年10月1日
領収書

サンプルマート
大阪府大阪市サンプル区5-6-7
TEL: 06-9876-5432

商品名          数量  単価   金額
---------------------------------
テスト商品X     1   2,000  2,000
テスト商品Y     3     300    900
---------------------------------
小計                      2,900
消費税(10%)                 290
合計                      3,190

お支払い: クレジットカード
ありがとうございました。"""
            },
            {
                "date": "2025/4/10",
                "store": "サンプルショップ",
                "content": """レシート

2025/4/10
領収書

サンプルショップ
名古屋市サンプル区8-9-10
TEL: 052-123-4567

商品名          数量  単価   金額
---------------------------------
テスト商品P     2   1,500  3,000
テスト商品Q     1     800    800
---------------------------------
小計                      3,800
消費税(10%)                 380
合計                      4,180

お支払い: 電子マネー
ありがとうございました。"""
            },
            {
                "date": "2025/10/1",
                "store": "サンプルストア札幌",
                "content": """レシート

2025/10/1
領収書

サンプルストア札幌
北海道札幌市サンプル区11-12-13
TEL: 011-234-5678

商品名          数量  単価   金額
---------------------------------
サンプル商品M    3     600  1,800
サンプル商品N    2     450    900
---------------------------------
小計                      2,700
消費税(10%)                 270
合計                      2,970

お支払い: QRコード決済
ありがとうございました。"""
            }
        ]
        
        for i, sample in enumerate(sample_data):
            date_str = sample["date"]
            if "年" in date_str:
                year = re.search(r'(\d{4})年', date_str).group(1)
                month = re.search(r'(\d{1,2})月', date_str).group(1).zfill(2)
                day = re.search(r'(\d{1,2})日', date_str).group(1).zfill(2)
                formatted_date = f"{year}{month}{day}"
            else:
                parts = re.split(r'[/-]', date_str)
                year = parts[0]
                month = parts[1].zfill(2)
                day = parts[2].zfill(2)
                formatted_date = f"{year}{month}{day}"
            
            store = sample["store"]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            filename = f"{formatted_date}_{store}_sample{i+1}_{timestamp}.txt"
            file_path = os.path.join(logs_folder, filename)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(sample["content"])
            
            print(f"Created sample OCR log: {filename}")

def test_with_logs():
    """Test date extraction with OCR log files"""
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
        
        if is_valid_format:
            month = date[4:6]
            day = date[6:8]
            
            if month.startswith('0') and int(month) < 10:
                print("Month is correctly zero-padded")
            elif int(month) >= 10:
                print("Month is already double-digit")
            else:
                print("WARNING: Month is not zero-padded")
                
            if day.startswith('0') and int(day) < 10:
                print("Day is correctly zero-padded")
            elif int(day) >= 10:
                print("Day is already double-digit")
            else:
                print("WARNING: Day is not zero-padded")
        
        print("-" * 50)

if __name__ == "__main__":
    create_sample_ocr_logs()
    
    test_with_logs()
