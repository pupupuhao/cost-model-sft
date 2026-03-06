import os
import warnings
from llamafactory.train.tuner import run_exp

warnings.filterwarnings("ignore")

# 环境设置
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["PYTHONIOENCODING"] = "utf-8"


def main():
    # 构造参数字典，直接传给 run_exp
    # 注意：这里我们不再用 sys.argv，而是直接定义参数
    args = dict(
        stage="sft",
        do_train=True,
        model_name_or_path=r"D:\cost-models\qwen\Qwen2.5-0.5B-Instruct",
        dataset="cost_full",
        dataset_dir=".",
        template="qwen",
        finetuning_type="lora",
        lora_target="all",
        lora_rank=16,
        lora_alpha=32,
        output_dir="./cost-qwen-sample-result",
        overwrite_cache=True,
        cutoff_len=256,
        max_samples=10,
        preprocessing_num_workers=1,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=1,
        lr_scheduler_type="constant",
        logging_steps=1,
        save_steps=50,
        learning_rate=5e-5,
        num_train_epochs=20.0,
        plot_loss=True,
        fp16=False,
        use_cpu=True,
    )

    print("🚀 正在通过 API 启动小批量造价数据微调...")
    # 直接将字典传给 run_exp (LLaMA-Factory 支持这种调用)
    run_exp(args)
    print("✅ 训练完成！结果保存在 ./cost-qwen-sample-result")


if __name__ == "__main__":
    main()
