import re

MIN_YEAR = 2000
MAX_YEAR = 2030
DEFAULT_YEAR = 2023

test_cases = [
    "2025年4月10日",
    "2025年10月1日",
    "2025/4/10",
    "2025/10/1"
]

date_patterns = [
    r"(\d{4}[/-]\d{1,2}[/-]\d{1,2})",
    r"(\d{2}[/-]\d{1,2}[/-]\d{1,2})",
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)",
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)",  # with weekday in parentheses
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)\s*\d{1,2}:\d{2}",  # with weekday and time
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)\s*\d{1,2}:\d{2}[^0-9]*"  # with weekday, time and trailing chars
]

def extract_date(text):
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
                    
                    formatted_date = f"{year}{month}{day}"
                    all_dates.append(formatted_date)
            else:
                formatted_date = re.sub(r"[年月]", "", raw_date)
                formatted_date = formatted_date.replace("日", "")
                formatted_date = formatted_date.replace(" ", "")
                
                year_match = re.search(r'^(\d{4})', formatted_date)
                if year_match:
                    year = year_match.group(1)
                    remaining = formatted_date[4:]
                    
                    if len(remaining) >= 2:
                        if len(remaining) >= 3 and remaining[1].isdigit():
                            month = remaining[:2]
                            day = remaining[2:].zfill(2)
                        else:
                            month = remaining[0].zfill(2)
                            day = remaining[1:].zfill(2)
                        
                        formatted_date = f"{year}{month}{day}"
                        all_dates.append(formatted_date)
    
    return all_dates[0] if all_dates else None

print("Testing date extraction with zero-padding fix...")
print("-" * 50)

for test_case in test_cases:
    date = extract_date(test_case)
    print(f"Input: {test_case}")
    print(f"Extracted date: {date}")
    print(f"Expected format: 8 digits with zero-padding (YYYYMMDD)")
    print(f"Actual length: {len(date) if date else 0}")
    print(f"Is correctly formatted: {'Yes' if date and len(date) == 8 else 'No'}")
    print("-" * 50)

print("Test completed.")
