

import re

date_pattern = r"(\d{4}年\s*\d{1,2}月\s*\d{1,2}日)"

test_cases = [
    "2025年4月10日",
    "2025年04月10日",
    "2025年 3月18日",
    "2025年 03月 18日",
    "テスト 2025年4月10日 テスト",
    "テスト 2025年 04月 10日 テスト"
]

print("Testing date pattern recognition...")
for test_case in test_cases:
    matches = re.finditer(date_pattern, test_case)
    found = False
    for match in matches:
        found = True
        raw_date = match.group(1)
        print(f"Input: {test_case} -> Matched: {raw_date}")
    
    if not found:
        print(f"Input: {test_case} -> No match found")

print("\nTest completed.")
