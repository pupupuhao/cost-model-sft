import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# 1. 路径配置
model_path = r"D:\cost-models\qwen\Qwen2.5-0.5B-Instruct"
# 注意：如果你改了 output_dir，请确保这里同步修改
adapter_path = "./cost-qwen-sample-result"

print("正在加载【上海造价审计专家】大脑...")

# 2. 加载基础模型与分词器
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float32,
    device_map="cpu"
)

# 3. 挂载 LoRA 补丁
model = PeftModel.from_pretrained(model, adapter_path)
model.eval()  # 切换到推理模式
print("✅ 0.0002 Loss 权重加载成功！")


def predict_cost(instruction, item_name):
    # 【关键修改】：构造与你提供的最新 JSONL 格式完全匹配的输入
    # 训练数据中规格统一改成了“无”，所以这里也必须是“无”
    prompt = f"{instruction}\n项目名称：{item_name}，规格：无"

    # 使用 Qwen2.5 特有的模板格式（可选，但对于 Instruct 模型更稳）
    messages = [
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True)

    inputs = tokenizer(text, return_tensors="pt").to("cpu")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            temperature=0.01,  # 极低随机性，确保单价死板准确
            repetition_penalty=1.0,  # 稍微调低，防止长名称被截断
            eos_token_id=tokenizer.eos_token_id
        )

    # 提取生成的回答部分
    response = tokenizer.decode(
        outputs[0][len(inputs["input_ids"][0]):], skip_special_tokens=True)
    return response.strip()


# 4. 这里的测试案例直接来自你刚才发的 10 条训练集
test_items = [
    ("查询2026年2月上海园林材料信息价", "黄石"),
    ("查询2026年2月上海燃气专用材料信息价", "聚乙烯电熔三通（PE80）SDR11dn110"),
    ("查询2026年2月上海市政机械信息价", "混凝土输送泵30m3/h"),
    ("查询2026年2月上海燃气专用材料信息价", "焊接式管道带压连接器LJQ-DN300-50 1.6MPa")
]

print("\n--- 🧠 上海造价 AI 现场考核 ---")
for inst, name in test_items:
    result = predict_cost(inst, name)
    print(f"\n🔍 提问内容: {inst} | {name}")
    print(f"💰 AI 回复: {result}")
