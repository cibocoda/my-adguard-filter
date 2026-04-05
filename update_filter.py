import requests
import re
from datetime import datetime

# 讀取來源網址
try:
    with open('source.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    print("錯誤: 找不到 source.txt")
    exit(1)

all_rules = set()

for url in urls:
    try:
        print(f"正在下載: {url}")
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                line = line.strip()
                
                # 1. 嚴格過濾：跳過註解、空白行，以及「放行規則 (@@)」
                if not line or line.startswith(('!', '#', '[', '@@')):
                    continue
                
                # 2. 格式清洗
                # 移除 hosts 格式開頭的 IP
                line = re.sub(r'^(0\.0\.0\.0|127\.0\.0\.1)\s+', '', line)
                # 移除 Adblock 特有符號
                line = line.replace('||', '').replace('^', '')
                # 移除行尾備註
                line = line.split('#')[0].split('!')[0].strip()
                
                # 3. 有效性檢查 (只保留看起來像網域的字串)
                if '.' in line and len(line) > 3 and not line[0].isdigit():
                    # 額外保險：如果清洗完還帶有特殊符號（如 / 或 *），通常是過於複雜的網頁規則，DNS 擋不了，跳過
                    if '/' not in line and '*' not in line:
                        all_rules.add(line)
        else:
            print(f"下載失敗 (Status {response.status_code}): {url}")
    except Exception as e:
        print(f"處理出錯 {url}: {e}")

# 寫入最終合併檔案
with open('my_combined_list.txt', 'w') as f:
    f.write(f"! Title: My Optimized Combined Filter\n")
    f.write(f"! Last Modified: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"! Total Unique Rules: {len(all_rules)}\n")
    f.write("!\n")
    # 排序後寫入，方便追蹤變動
    for rule in sorted(all_rules):
        f.write(rule + '\n')

print(f"完成！總計唯一規則數: {len(all_rules)}")
