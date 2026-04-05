import requests
from datetime import datetime

# 讀取來源
try:
    with open('source.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
except FileNotFoundError:
    print("Error: source.txt not found")
    exit(1)

all_rules = set()

for url in urls:
    try:
        print(f"Downloading: {url}")
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            lines = response.text.splitlines()
            for line in lines:
                line = line.strip()
                # 只過濾掉註解和空白行，保留原始規則格式（包含 @@, ||, ^ 等）
                if line and not line.startswith(('!', '#', '[')):
                    all_rules.add(line)
        else:
            print(f"Failed: {url}")
    except Exception as e:
        print(f"Error {url}: {e}")

# 寫入檔案
with open('my_combined_list.txt', 'w') as f:
    f.write(f"! Title: My Combined Filter (Original Format)\n")
    f.write(f"! Last Modified: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"! Total Rules: {len(all_rules)}\n")
    f.write("!\n")
    # 排序後寫入
    for rule in sorted(all_rules):
        f.write(rule + '\n')

print(f"Done! Total: {len(all_rules)}")
