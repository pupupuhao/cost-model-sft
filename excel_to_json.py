import pandas as pd
import json
import os


def convert_all_to_json(file_list, output_filename="cost_data_full.json"):
    # 统一的工作表标签
    sheet_names = ["建筑，安装", "市政", "公路", "园林", "燃气专用"]
    all_data = []

    for file_info in file_list:
        file_path = file_info['path']
        table_type = file_info['type']  # 人工、机械、材料

        if not os.path.exists(file_path):
            print(f"⚠️ 跳过：找不到文件 {file_path}")
            continue

        print(f"开始处理【{table_type}表】: {file_path}")

        for sheet in sheet_names:
            try:
                # 1. 先读前几行找表头
                df_temp = pd.read_excel(
                    file_path, sheet_name=sheet, engine='openpyxl', nrows=10)
                header_row = None
                for i, row in df_temp.iterrows():
                    if "名称" in [str(v).strip() for v in row.values]:
                        header_row = i
                        break

                if header_row is None:
                    continue

                # 2. 正式读取该 Sheet 数据
                df = pd.read_excel(file_path, sheet_name=sheet,
                                   skiprows=header_row + 1, engine='openpyxl')
                df.columns = [str(c).strip().replace('\n', '')
                              for c in df.columns]

                count = 0
                for _, row in df.iterrows():
                    # --- 1. 提取名称并过滤空行 ---
                    name = str(row.get('名称', '')).strip()
                    if not name or name.lower() in ['nan', 'none', '']:
                        continue

                    # --- 2. 核心优化：处理规格中的 nan ---
                    # 获取规格，如果缺失则默认为 '无'
                    raw_spec = str(row.get('规格', '无')).strip()
                    # 拦截 nan 字符串
                    spec = "无" if raw_spec.lower() in [
                        'nan', 'none', ''] else raw_spec

                    # --- 3. 提取计量单位（同理处理 nan） ---
                    raw_unit = str(row.get('计量单位', '')).strip()
                    unit = "单位待定" if raw_unit.lower(
                    ) in ['nan', 'none', ''] else raw_unit

                    # --- 4. 价格处理（确保数字干净） ---
                    p1 = row.get('含税价(元)', row.get('含规费价格(元)', '0'))
                    p2 = row.get('除税价(元)', row.get('不含规费价格(元)', '0'))

                    # 额外保险：如果价格读出来也是 nan，转为 0
                    p1 = "0" if str(p1).lower() == 'nan' else p1
                    p2 = "0" if str(p2).lower() == 'nan' else p2

                    entry = {
                        "instruction": f"查询2026年2月上海{sheet}{table_type}信息价",
                        "input": f"项目名称：{name}，规格：{spec}",
                        "output": f"根据2026年2月上海市建设工程市场信息价，【{sheet}】{table_type}类的“{name}”（规格：{spec}）单价为：计量单位{unit}，含税/含规费单价{p1}元，除税/不含规费单价{p2}元。"
                    }
                    all_data.append(entry)
                    count += 1

                print(f"   - 【{sheet}】标签页处理完毕，抓取 {count} 条")

            except Exception:
                # 如果某个文件没有特定的 Sheet（如机械表没燃气标签），直接跳过
                pass

    # 保存为统一的训练集
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 全部完成！共生成 {len(all_data)} 条混合训练数据。")
    print(f"文件保存至: {os.path.abspath(output_filename)}")


if __name__ == "__main__":
    # 使用你提供的准确文件名
    files_to_process = [
        {'path': '2026年2月信息价（人工）.xlsx', 'type': '人工'},
        {'path': '2026年2月信息价（机械）.xlsx', 'type': '机械'},
        {'path': '2026年2月信息价（材料）.xlsx', 'type': '材料'}
    ]
    convert_all_to_json(files_to_process)
