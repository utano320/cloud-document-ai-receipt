import re

date_patterns = [
    r"(\d{4}[/-]\d{1,2}[/-]\d{1,2})",
    r"(\d{2}[/-]\d{1,2}[/-]\d{1,2})",
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)",
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)",  # with weekday in parentheses
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)\s*\d{1,2}:\d{2}",  # with weekday and time
    r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)\s*\([^)]*\)\s*\d{1,2}:\d{2}[^0-9]*"  # with weekday, time and trailing chars
]

test_cases = [
    "2025年4月10日(木) 02:15",
    "2025年 4月12日 (土) 17:49 レジ :201",
    "2025年4月10日 (木) 2:31",
    "2025年4月10日 (木) 2:05)"
]

print("Testing date pattern recognition...")
for test_case in test_cases:
    print(f"Input: {test_case}")
    for pattern in date_patterns:
        matches = re.finditer(pattern, test_case)
        for match in matches:
            raw_date = match.group(1)
            print(f"  Pattern: {pattern} -> Matched: {raw_date}")
            
            normalized = raw_date
            normalized = re.sub(r"[/-]", "", normalized)
            normalized = re.sub(r"[年月]", "", normalized)
            normalized = normalized.replace("日", "")
            normalized = normalized.replace(" ", "")
            
            if len(normalized) == 8:
                yyyy = normalized[:4]
                mm = normalized[4:6].zfill(2)
                dd = normalized[6:8].zfill(2)
                normalized_date = f"{yyyy}{mm}{dd}"
                print(f"  Normalized date: {normalized_date}")
    print("")

print("Test completed.")
