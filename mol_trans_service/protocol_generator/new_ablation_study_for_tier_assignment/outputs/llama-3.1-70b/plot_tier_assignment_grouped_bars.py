#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.ticker import MaxNLocator


TIERS = ("L1", "L2", "L3")
DISPLAY_GROUPS = (*TIERS, "Overall")
BASELINE_PREFIX = "ex1_"
QDHC_PREFIX = "ex3_"
TIER_ORDER = {tier: index for index, tier in enumerate(TIERS, start=1)}
METRIC_LABELS = (
    "Baseline: matched tier",
    "With QDHC: highest-tier match",
    "With QDHC: expert-tier inclusion",
)

# Figure text settings: edit these values directly if you want to change wording or font sizes.
TITLE_TEMPLATE = "Tier Adjudication by llama-3.1-70b"
X_AXIS_LABEL = "Expert-labeled Query Group"
Y_AXIS_LABEL = "Average Query Count"
TITLE_FONT_SIZE = 20
AXIS_LABEL_FONT_SIZE = 17
X_TICK_FONT_SIZE = 13
Y_TICK_FONT_SIZE = 12
LEGEND_FONT_SIZE = 12
BAR_VALUE_FONT_SIZE = 14


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot grouped bar charts for tier-assignment results."
    )
    parser.add_argument(
        "--input",
        default="result_data_origin.csv",
        help="Input CSV file. Defaults to result_data_origin.csv in the current directory.",
    )
    parser.add_argument(
        "--output",
        default="tier_assignment_grouped_bars.png",
        help="Output image path. Defaults to tier_assignment_grouped_bars.png.",
    )
    parser.add_argument(
        "--model-name",
        default=None,
        help="Model name shown in the title. Defaults to the current directory name.",
    )
    parser.add_argument(
        "--caption-output",
        default="tier_assignment_grouped_bars_caption.txt",
        help="Path to save a paper-ready figure caption.",
    )
    return parser.parse_args()


def read_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def get_run_columns(fieldnames: Iterable[str], prefix: str) -> list[str]:
    return sorted(column for column in fieldnames if column.startswith(prefix))


def extract_tiers(prediction: str) -> list[str]:
    value = (prediction or "").strip()
    if not value:
        return []

    if value.startswith("STAGED(") and value.endswith(")"):
        content = value[len("STAGED(") : -1]
        return [part.strip() for part in content.split("->") if part.strip() in TIER_ORDER]

    return [value] if value in TIER_ORDER else []


def final_tier(prediction: str) -> str | None:
    tiers = extract_tiers(prediction)
    if tiers:
        return max(tiers, key=TIER_ORDER.get)

    value = (prediction or "").strip()
    return value if value in TIER_ORDER else None


def tier_included(prediction: str, expert_tier: str) -> bool:
    tiers = extract_tiers(prediction)
    if tiers:
        return expert_tier in tiers
    return (prediction or "").strip() == expert_tier


def aggregate_counts(
    rows: list[dict[str, str]], baseline_runs: list[str], qdhc_runs: list[str]
) -> dict[str, dict[str, list[int]]]:
    results = {
        METRIC_LABELS[0]: {group: [] for group in DISPLAY_GROUPS},
        METRIC_LABELS[1]: {group: [] for group in DISPLAY_GROUPS},
        METRIC_LABELS[2]: {group: [] for group in DISPLAY_GROUPS},
    }

    for tier in TIERS:
        tier_rows = [row for row in rows if row.get("expert_tier", "").strip() == tier]

        for column in baseline_runs:
            count = sum(1 for row in tier_rows if final_tier(row.get(column, "")) == tier)
            results[METRIC_LABELS[0]][tier].append(count)

        for column in qdhc_runs:
            strict_count = sum(1 for row in tier_rows if final_tier(row.get(column, "")) == tier)
            included_count = sum(1 for row in tier_rows if tier_included(row.get(column, ""), tier))
            results[METRIC_LABELS[1]][tier].append(strict_count)
            results[METRIC_LABELS[2]][tier].append(included_count)

    for run_index in range(len(baseline_runs)):
        results[METRIC_LABELS[0]]["Overall"].append(
            sum(results[METRIC_LABELS[0]][tier][run_index] for tier in TIERS)
        )

    for run_index in range(len(qdhc_runs)):
        results[METRIC_LABELS[1]]["Overall"].append(
            sum(results[METRIC_LABELS[1]][tier][run_index] for tier in TIERS)
        )
        results[METRIC_LABELS[2]]["Overall"].append(
            sum(results[METRIC_LABELS[2]][tier][run_index] for tier in TIERS)
        )

    return results


def mean_and_range(values: list[int]) -> tuple[float, np.ndarray]:
    array = np.asarray(values, dtype=float)
    mean = float(array.mean())
    lower = mean - float(array.min())
    upper = float(array.max()) - mean
    return mean, np.array([[lower], [upper]])


def format_height(value: float) -> str:
    return str(int(value)) if value.is_integer() else f"{value:.1f}"


def get_group_sizes(rows: list[dict[str, str]]) -> dict[str, int]:
    sizes = {
        tier: sum(1 for row in rows if row.get("expert_tier", "").strip() == tier)
        for tier in TIERS
    }
    sizes["Overall"] = sum(sizes.values())
    return sizes


def build_group_labels(group_sizes: dict[str, int]) -> list[str]:
    return [f"{group} (n={group_sizes[group]})" for group in DISPLAY_GROUPS]


# def build_caption(model_name: str) -> str:
#     return (
#         f"{model_name} performance on tier adjudication. Bars show the mean query count "
#         "across three runs, and error bars show the min-max range. "
#         "Recommended-tier correct compares the expert-labeled tier with the model's "
#         "recommended execution tier: the single predicted tier when the model outputs one "
#         "tier, or the highest tier in a staged tier scheme. "
#         "Expert-tier included counts cases where the expert-labeled tier appears anywhere in "
#         "the model output, either as a single tier or within a staged tier scheme. "
#         "The gap between QDHC expert-tier included and QDHC recommended-tier correct therefore "
#         "reflects cases where the expert tier was present in the adjudication path but the "
#         "final recommendation was escalated above it."
#     )


def plot_chart(
    aggregated: dict[str, dict[str, list[int]]],
    group_sizes: dict[str, int],
    model_name: str,
    output_path: Path,
) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    rcParams["font.family"] = ["Arial"]
    fig, ax = plt.subplots(figsize=(7.8, 4.0), dpi=600)

    metrics = list(aggregated.keys())
    colors = ["#3B6FB6", "#E67E22", "#F4B26A"]
    x = np.array([0.0, 0.76, 1.52, 2.46])
    width = 0.18
    bar_gap = 0.03
    offset_step = width + bar_gap

    ymax = float(max(group_sizes.values()))
    reference_half_width = offset_step + width / 2 + 0.01

    ax.axvline(1.97, color="#D0D0D0", linewidth=1.0, linestyle=(0, (3, 3)), zorder=1)
    overall_span_half_width = 0.39
    ax.axvspan(
        x[-1] - overall_span_half_width,
        x[-1] + overall_span_half_width,
        color="#F5F5F5",
        alpha=0.9,
        zorder=0,
    )

    for xpos, group in zip(x, DISPLAY_GROUPS):
        ax.hlines(
            group_sizes[group],
            xpos - reference_half_width,
            xpos + reference_half_width,
            colors="#9A9A9A",
            linestyles=(0, (2, 2)),
            linewidth=1.2,
            zorder=1,
        )

    for index, metric in enumerate(metrics):
        means = []
        lower_errors = []
        upper_errors = []

        for group in DISPLAY_GROUPS:
            mean, error = mean_and_range(aggregated[metric][group])
            means.append(mean)
            lower_errors.append(error[0, 0])
            upper_errors.append(error[1, 0])

        offsets = x + (index - 1) * offset_step
        bars = ax.bar(
            offsets,
            means,
            width=width,
            label=metric,
            color=colors[index],
            edgecolor="none",
            linewidth=0,
            yerr=np.array([lower_errors, upper_errors]),
            capsize=4,
            error_kw={"elinewidth": 1.0, "capthick": 1.0, "ecolor": "#333333"},
            zorder=3,
        )
        ymax = max(ymax, max(mean + upper for mean, upper in zip(means, upper_errors)))

        for bar, mean, upper in zip(bars, means, upper_errors):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + upper + 0.12,
                format_height(mean),
                ha="center",
                va="bottom",
                fontsize=BAR_VALUE_FONT_SIZE,
                fontweight="bold",
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.8, "pad": 0.2},
            )

    ax.set_xticks(x)
    ax.set_xticklabels(build_group_labels(group_sizes), fontsize=X_TICK_FONT_SIZE, fontweight="bold")
    ax.set_ylabel(Y_AXIS_LABEL, fontsize=AXIS_LABEL_FONT_SIZE, fontweight="bold")
    ax.set_xlabel(X_AXIS_LABEL, fontsize=AXIS_LABEL_FONT_SIZE, fontweight="bold")
    ax.set_title(
        TITLE_TEMPLATE.format(model_name=model_name),
        fontsize=TITLE_FONT_SIZE,
        fontweight="bold",
        pad=12,
    )
    ax.legend(
        frameon=True,
        facecolor="white",
        edgecolor="#DDDDDD",
        framealpha=0.95,
        fontsize=LEGEND_FONT_SIZE,
        loc="upper left",
        bbox_to_anchor=(0.015, 0.985),
        ncol=1,
        borderaxespad=0.2,
        handlelength=1.5,
        prop={"weight": "bold", "size": LEGEND_FONT_SIZE},
    )
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(1.0)
    ax.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.5)
    ax.grid(False, axis="x")
    ax.xaxis.grid(False, which="both")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_ylim(0, ymax + 1.1)
    ax.set_xlim(-0.35, 2.90)
    ax.margins(x=0.0)
    ax.tick_params(axis="x", length=0)
    ax.tick_params(axis="y", labelsize=Y_TICK_FONT_SIZE)
    for label in ax.get_yticklabels():
        label.set_fontweight("bold")
    fig.tight_layout(pad=0.28)
    fig.savefig(output_path, dpi=600, bbox_inches="tight", pad_inches=0.03)
    svg_path = output_path.with_suffix(".svg")
    fig.savefig(svg_path, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()
    caption_output_path = Path(args.caption_output).resolve()

    rows = read_rows(input_path)
    if not rows:
        raise ValueError(f"No data rows found in {input_path}")

    fieldnames = rows[0].keys()
    baseline_runs = get_run_columns(fieldnames, BASELINE_PREFIX)
    qdhc_runs = get_run_columns(fieldnames, QDHC_PREFIX)
    if not baseline_runs or not qdhc_runs:
        raise ValueError("Missing ex1 or ex3 run columns in the input CSV.")

    model_name = args.model_name or input_path.parent.name
    aggregated = aggregate_counts(rows, baseline_runs, qdhc_runs)
    group_sizes = get_group_sizes(rows)
    plot_chart(aggregated, group_sizes, model_name, output_path)
    # caption_output_path.write_text(build_caption(model_name), encoding="utf-8")

    print(f"Saved figure to {output_path}")
    print(f"Saved figure to {output_path.with_suffix('.svg')}")
    print(f"Saved caption to {caption_output_path}")


if __name__ == "__main__":
    main()
