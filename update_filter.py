import requests
import re

# 讀取 source.txt 中的網址
with open('source.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

all_rules = set()

for url in urls:
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # 簡單過濾：只保留非註解且長度合理的規則
            lines = response.text.splitlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith(('!', '#')):
                    all_rules.add(line)
    except Exception as e:
        print(f"無法下載 {url}: {e}")

# 將結果寫入最終檔案
with open('my_combined_list.txt', 'w') as f:
    f.write("! Title: My Combined Filter\n")
    f.write("! Last Modified: " + "\n")
    for rule in sorted(all_rules):
        f.write(rule + '\n')
