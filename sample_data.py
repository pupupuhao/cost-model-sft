import json
import random

# 原始数据文件（你的几千条造价Q&A）
input_file = "cost_data_full.jsonl"
# 测试用小批量数据文件
output_file = "cost_sample.jsonl"
# 提取数量（根据你的电脑性能调整，推荐10-20条）
sample_size = 10

# 读取原始数据并随机采样
data_list = []
with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:  # 跳过空行
            data_list.append(json.loads(line))

# 随机选10条（若数据不足10条则取全部）
sample_data = random.sample(data_list, min(sample_size, len(data_list)))

# 写入小批量测试文件
with open(output_file, "w", encoding="utf-8") as f:
    for item in sample_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"✅ 已生成小批量测试数据：{output_file}")
print(f"📊 测试数据条数：{len(sample_data)}")
