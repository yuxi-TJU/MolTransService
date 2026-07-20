# generate_result_data.py 使用说明

## 功能

从 `batch_test.py` 生成的输出文件中提取所有 tier 预测结果，整合为一个 `result_data.csv` 文件，供后续统计分析和绘图使用。

## 前提条件

需要先使用 `batch_test.py` 完成测试，输出目录结构示例：

```
outputs/
└── gemini-2.5-pro/          ← 模型目录
    ├── ex1/
    │   ├── run_1/
    │   │   ├── batch_test_ex1_gemini-2.5-pro_20260310_*.json      ← 结果文件
    │   │   └── batch_test_ex1_gemini-2.5-pro_20260310_*_reports.json
    │   ├── run_2/
    │   └── run_3/
    ├── ex3/
    │   ├── run_1/
    │   ├── run_2/
    │   └── run_3/
    └── result_data.csv       ← 生成的文件
```

## 用法

```bash
# 进入脚本所在目录
cd ablation_study_for_tier_assignment/

# 方式 1：指定模型目录
python generate_result_data.py outputs/gemini-2.5-pro

# 方式 2：cd 进模型目录后运行
cd outputs/gemini-2.5-pro
python ../../generate_result_data.py

# 方式 3：批量处理所有模型
python generate_result_data.py --all

# 方式 4：指定输出路径
python generate_result_data.py outputs/gemini-2.5-pro -o /tmp/result.csv
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `model_dir` | 模型输出目录路径（默认：当前目录） |
| `--all` | 自动扫描 `outputs/` 下所有模型目录并逐一处理 |
| `-o`, `--output` | 指定 CSV 输出路径（默认：`{model_dir}/result_data.csv`） |

## 输出格式

生成的 `result_data.csv` 格式如下：

```
name,expert_tier,ex1_run1,ex1_run2,ex1_run3,ex3_run1,ex3_run2,ex3_run3
test_paper_1,L1,L3,L3,L3,L2,L2,L1
test_paper_2,L1,L3,L3,L3,L1,L1,L3
...
```

| 列 | 说明 |
|----|------|
| `name` | 查询名称（如 `test_paper_1`） |
| `expert_tier` | 人工标注的正确 tier |
| `ex{N}_run{M}` | 第 N 组实验、第 M 次运行的预测 tier |

## 终端输出示例

```
✅ CSV saved to: outputs/gemini-2.5-pro/result_data.csv
   Queries: 20
   Conditions × Runs: 6
   Columns: ex1_run1, ex1_run2, ex1_run3, ex3_run1, ex3_run2, ex3_run3

📊 Accuracy by condition × run:
   ex1_run1: 10/20 (50%)
   ex1_run2: 11/20 (55%)
   ex1_run3: 10/20 (50%)
   ex3_run1: 14/20 (70%)
   ex3_run2: 14/20 (70%)
   ex3_run3: 13/20 (65%)
```

## 注意事项

- 脚本自动扫描 `ex*/run_*/batch_test_*.json`，排除 `_reports.json` 文件
- 如果同一 run 下有多个结果文件，取最新的（按文件名排序）
- `STAGED` 预测会以 `STAGED(L1→L2)` 格式保留在 CSV 中
- `Out` 标签已统一为 `OOS`
