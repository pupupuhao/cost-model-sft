import json

# 读取JSON文件（外层数组）
with open("cost_data_full.json", "r", encoding="utf-8") as f:
    data_list = json.load(f)

# 写入JSONL文件（每行1条）
with open("cost_data_full.jsonl", "w", encoding="utf-8") as f:
    for item in data_list:
        # 确保每行是独立的JSON串
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("✅ JSON已转为JSONL格式，文件：cost_full.jsonl")
