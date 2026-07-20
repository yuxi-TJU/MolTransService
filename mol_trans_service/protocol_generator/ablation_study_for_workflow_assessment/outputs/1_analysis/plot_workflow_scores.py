"""
绘制 workflow evaluation scores by rubric dimension 折线图。
- gemini 两条曲线使用蓝色系（MST-only 浅，MST+Examples 深）
- qwen 两条曲线使用橙红色系（MST-only 浅，MST+Examples 深）
- 同模型两条曲线之间使用半透明填充来突显区别
- 所有字体使用 Arial，字号增大
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from pathlib import Path

# ── 全局字体设置 ──────────────────────────────────────────
mpl.rcParams["font.family"] = "Arial"
mpl.rcParams["font.size"] = 13

# ── 读取数据 ──────────────────────────────────────────────
csv_path = Path(__file__).parent / "workflow_scores.csv"
df = pd.read_csv(csv_path)

dimensions = ["Module selection", "Completeness", "Analysis design",
              "Hypothesis-testing", "Groundedness"]
x = np.arange(len(dimensions))


def get_scores(model: str, condition: str) -> list[float]:
    row = df[(df["Model"] == model) & (df["Condition"] == condition)]
    return row[dimensions].values.flatten().tolist()


gemini_mst = get_scores("gemini-2.5-pro", "MST-only")
gemini_ex  = get_scores("gemini-2.5-pro", "MST+Examples")
qwen_mst   = get_scores("qwen2.5-72b-instruct", "MST-only")
qwen_ex    = get_scores("qwen2.5-72b-instruct", "MST+Examples")

# ── 配色（同模型同色系，MST+Examples 用更深的颜色）─────────
# Gemini 色系：蓝
GEMINI_MST_COLOR  = "#98c9da"   # 
GEMINI_EX_COLOR   = "#2878b3"   #
GEMINI_FILL       = "#BBDEFB"   # 极浅蓝 (填充)

# Qwen 色系：橙红（与蓝色对比鲜明）
QWEN_MST_COLOR    = "#fea985"   # 
QWEN_EX_COLOR     = "#c82423"   # 
QWEN_FILL         = "#FFCCBC"   # 极浅橙 (填充)

# ── 绘图 ──────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

# 半透明填充
ax.fill_between(x, gemini_mst, gemini_ex,
                color=GEMINI_FILL, alpha=0.5, interpolate=True)
ax.fill_between(x, qwen_mst, qwen_ex,
                color=QWEN_FILL, alpha=0.5, interpolate=True)

# 折线 — Gemini（蓝色系）
ax.plot(x, gemini_mst, marker="o", linewidth=2.5, color=GEMINI_MST_COLOR,
        linestyle="--", label="gemini-2.5-pro | MST-only", markersize=8,
        markeredgecolor="white", markeredgewidth=0.8)
ax.plot(x, gemini_ex,  marker="s", linewidth=2.5, color=GEMINI_EX_COLOR,
        label="gemini-2.5-pro | MST+Examples", markersize=8,
        markeredgecolor="white", markeredgewidth=0.8)

# 折线 — Qwen（橙红色系）
ax.plot(x, qwen_mst,   marker="o", linewidth=2.5, color=QWEN_MST_COLOR,
        linestyle="--", label="qwen2.5-72b-instruct | MST-only", markersize=8,
        markeredgecolor="white", markeredgewidth=0.8)
ax.plot(x, qwen_ex,    marker="s", linewidth=2.5, color=QWEN_EX_COLOR,
        label="qwen2.5-72b-instruct | MST+Examples", markersize=8,
        markeredgecolor="white", markeredgewidth=0.8)

# ── 坐标轴 & 标注 ─────────────────────────────────────────
ax.set_xticks(x)
ax.set_xticklabels(dimensions, fontsize=12)
ax.set_xlabel("Rubric dimension", fontsize=14)
ax.set_ylabel("Average score", fontsize=14)
ax.set_title("Workflow evaluation scores by rubric dimension", fontsize=16, fontweight="bold")
ax.set_ylim(0, 2.15)
ax.tick_params(axis="both", labelsize=12)
ax.legend(loc="lower left", fontsize=13, framealpha=0.9, handlelength=2.5)

for spine in ax.spines.values():
    spine.set_visible(True)
ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()

# ── 保存 ──────────────────────────────────────────────────
out_path = Path(__file__).parent / "workflow_scores_line_chart.png"
fig.savefig(out_path, dpi=600, bbox_inches="tight")
print(f"图表已保存至: {out_path}")
plt.show()
