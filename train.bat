@echo off
chcp 65001 > nul  # 解决中文乱码
set HF_ENDPOINT=https://hf-mirror.com
set PYTHONIOENCODING=utf-8
set TRANSFORMERS_OFFLINE=0  # 允许在线下载缺失的tokenizer

:: 核心优化：适配Qwen2.5-0.5B-Instruct + CPU训练
llamafactory-cli train ^
    --stage sft ^
    --do_train True ^
    --model_name_or_path D:\cost-models\qwen\Qwen2.5-0.5B-Instruct ^
    --dataset cost_full ^
    --dataset_dir . ^
    --dataset_format jsonl ^  # 必须指定数据格式（你的Q&A是jsonl）
    --template qwen2 ^        # Qwen2.5要用qwen2模板（不是qwen）
    --finetuning_type lora ^
    --lora_target q_proj,v_proj ^  # Qwen2.5关键LoRA目标层
    --lora_rank 8 ^               # 0.5B模型适配的rank值
    --lora_alpha 32 ^             # 提升LoRA效果
    --output_dir ./cost-qwen-result ^
    --overwrite_cache True ^      # 显式指定布尔值
    --cutoff_len 256 ^
    --preprocessing_num_workers 0 ^  # CPU训练关闭多进程（避免报错）
    --per_device_train_batch_size 2 ^
    --gradient_accumulation_steps 8 ^
    --dataloader_num_workers 0 ^
    --lr_scheduler_type cosine ^
    --logging_steps 5 ^
    --save_steps 100 ^
    --save_total_limit 3 ^
    --learning_rate 1e-4 ^
    --num_train_epochs 2.0 ^
    --plot_loss True ^
    --bf16 False ^
    --fp16 False ^
    --use_cpu True ^              # 强制CPU训练
    --disable_tqdm True ^         # 关闭进度条，减少CPU开销
    --load_best_model_at_end False  # 避免验证集额外计算

echo ✅ 训练完成！结果保存在 ./cost-qwen-result
pause