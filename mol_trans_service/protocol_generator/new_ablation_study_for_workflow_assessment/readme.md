cd mol_trans_service/protocol_generator/new_ablation_study_for_workflow_assessment/


# Condition A — 仅 MST Manual
python batch_test.py -c cond_a -m gemini-2.5-pro -r 1
# Condition B — MST Manual + 检索示例（默认 top-3）
python batch_test.py -c cond_b -m llama-3.1-70b -r 1
# 设置 top-k 为 5
python batch_test.py -c cond_b -m llama-3.1-70b --top-k 5
# 只跑前 3 个 case 试试
python batch_test.py -c cond_a -n 3
# 3 次并行
python batch_test.py -c cond_a --parallel 3
# 重跑失败项
python batch_test.py -c cond_a -r 1 --retry-failed



# 开启保存（每个 case 生成一个 .md 文件）
python batch_test.py -c cond_a -m gemini-2.5-pro --save-prompt
# 默认不开启
python batch_test.py -c cond_a -m gemini-2.5-pro



#######
python batch_test.py -c cond_b -m gemini-2.5-pro -s 7 -n 1 -r 5 --save-prompt
