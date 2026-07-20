"""Plot workflow-assessment bar charts with the same visual style as tier-assignment bars."""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Figure text settings: edit these values directly if you want to change wording or font sizes.
TITLE_TEXT = "Workflow Quality under MST-only and MST + Retrieved Precedents"
X_AXIS_LABEL = "Rubric Dimension"
Y_AXIS_LABEL = "Average Score"
TITLE_FONT_SIZE = 17
AXIS_LABEL_FONT_SIZE = 14
X_TICK_FONT_SIZE = 12
Y_TICK_FONT_SIZE = 12
LEGEND_FONT_SIZE = 10.5
BAR_VALUE_FONT_SIZE = 12

# Color settings: Gemini uses a teal family; Qwen uses a red family.
GEMINI_MST_COLOR = "#A8CCCC"
GEMINI_EX_COLOR = "#6ca6a7"
QWEN_MST_COLOR = "#D89A92"
QWEN_EX_COLOR = "#bb554a"

MST_ONLY_CONDITION = "MST-only"
# Keep reading the original data while rendering the updated terminology in the figure.
PRECEDENTS_SOURCE_CONDITION = "MST+Examples"
PRECEDENTS_DISPLAY_LABEL = "MST + Precedents"


def get_scores(frame: pd.DataFrame, model: str, condition: str, columns: list[str]) -> list[float]:
    row = frame[(frame["Model"] == model) & (frame["Condition"] == condition)]
    if row.empty:
        available_conditions = sorted(frame.loc[frame["Model"] == model, "Condition"].dropna().unique().tolist())
        raise ValueError(
            f"No data found for model={model!r}, condition={condition!r}. "
            f"Available conditions for this model: {available_conditions}"
        )
    return row[columns].values.flatten().tolist()


def format_score(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".")


def annotate_bars(ax: plt.Axes, bars, font_size: float) -> None:
    for bar in bars:
        height = float(bar.get_height())
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.05,
            format_score(height),
            ha="center",
            va="bottom",
            fontsize=font_size,
            fontweight="bold",
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.8, "pad": 0.15},
        )


def main() -> None:
    mpl.rcParams["font.family"] = ["Arial"]

    csv_path = Path(__file__).parent / "workflow_scores.csv"
    df = pd.read_csv(csv_path)

    display_dimensions = [
        "Module selection",
        "Completeness",
        "Analysis design",
        "Hypothesis-testing",
        "Groundedness",
    ]
    csv_dimensions = [
        "Module path",
        "Completeness",
        "Analysis design",
        "Hypothesis-testing",
        "Groundedness",
    ]
    x = np.arange(len(display_dimensions))

    gemini_mst = get_scores(df, "gemini-2.5-pro", MST_ONLY_CONDITION, csv_dimensions)
    gemini_ex = get_scores(df, "gemini-2.5-pro", PRECEDENTS_SOURCE_CONDITION, csv_dimensions)
    qwen_mst = get_scores(df, "qwen2.5-72b-instruct", MST_ONLY_CONDITION, csv_dimensions)
    qwen_ex = get_scores(df, "qwen2.5-72b-instruct", PRECEDENTS_SOURCE_CONDITION, csv_dimensions)

    fig, ax = plt.subplots(figsize=(12.5, 3.5), dpi=600)

    width = 0.18
    bar_gap = 0.025
    offset_step = width + bar_gap

    bars1 = ax.bar(
        x - 1.5 * offset_step,
        gemini_mst,
        width=width,
        label=f"Gemini | {MST_ONLY_CONDITION}",
        color=GEMINI_MST_COLOR,
        edgecolor="none",
        linewidth=0,
        zorder=3,
    )
    bars2 = ax.bar(
        x - 0.5 * offset_step,
        gemini_ex,
        width=width,
        label=f"Gemini | {PRECEDENTS_DISPLAY_LABEL}",
        color=GEMINI_EX_COLOR,
        edgecolor="none",
        linewidth=0,
        zorder=3,
    )
    bars3 = ax.bar(
        x + 0.5 * offset_step,
        qwen_mst,
        width=width,
        label=f"Qwen | {MST_ONLY_CONDITION}",
        color=QWEN_MST_COLOR,
        edgecolor="none",
        linewidth=0,
        zorder=3,
    )
    bars4 = ax.bar(
        x + 1.5 * offset_step,
        qwen_ex,
        width=width,
        label=f"Qwen | {PRECEDENTS_DISPLAY_LABEL}",
        color=QWEN_EX_COLOR,
        edgecolor="none",
        linewidth=0,
        zorder=3,
    )

    annotate_bars(ax, bars1, BAR_VALUE_FONT_SIZE)
    annotate_bars(ax, bars2, BAR_VALUE_FONT_SIZE)
    annotate_bars(ax, bars3, BAR_VALUE_FONT_SIZE)
    annotate_bars(ax, bars4, BAR_VALUE_FONT_SIZE)

    ax.set_xticks(x)
    ax.set_xticklabels(display_dimensions, fontsize=X_TICK_FONT_SIZE, fontweight="bold")
    ax.set_xlabel(X_AXIS_LABEL, fontsize=AXIS_LABEL_FONT_SIZE, fontweight="bold")
    ax.set_ylabel(Y_AXIS_LABEL, fontsize=AXIS_LABEL_FONT_SIZE, fontweight="bold")
    ax.set_title(TITLE_TEXT, fontsize=TITLE_FONT_SIZE, fontweight="bold", pad=12)

    ax.set_ylim(0, 2.6)
    ax.set_xlim(-0.5, len(display_dimensions) - 0.5)
    ax.set_yticks(np.arange(0, 2.1, 0.5))
    ax.tick_params(axis="x", length=0)
    ax.tick_params(axis="y", labelsize=Y_TICK_FONT_SIZE)
    for label in ax.get_yticklabels():
        label.set_fontweight("bold")

    ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.015, 0.985),
        frameon=True,
        facecolor="white",
        edgecolor="#DDDDDD",
        framealpha=0.95,
        handlelength=1.5,
        borderaxespad=0.2,
        prop={"weight": "bold", "size": LEGEND_FONT_SIZE},
        ncol=4,
    )

    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(1.0)
    ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.5)
    ax.grid(False, axis="x")
    ax.xaxis.grid(False, which="both")

    fig.tight_layout(pad=0.3)

    out_png = Path(__file__).parent / "workflow_scores_bar_chart.png"
    out_svg = out_png.with_suffix(".svg")
    fig.savefig(out_png, dpi=600, bbox_inches="tight", pad_inches=0.03)
    fig.savefig(out_svg, bbox_inches="tight", pad_inches=0.03)
    print(f"Chart saved to: {out_png}")
    print(f"Chart saved to: {out_svg}")
    plt.close(fig)


if __name__ == "__main__":
    main()
