#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.image import AxesImage


TRUE_TIERS = ("L1", "L2", "L3")
PREDICTED_TIERS = ("L1", "L2", "L3", "OOS")
BASELINE_PREFIX = "ex1_"
QDHC_PREFIX = "ex3_"
TRUE_TIER_ORDER = {tier: index for index, tier in enumerate(TRUE_TIERS)}
PREDICTED_TIER_ORDER = {tier: index for index, tier in enumerate(PREDICTED_TIERS)}

TITLE = "Tier Adjudication Confusion Matrices for Gemini-2.5-pro"
EX1_HIGHEST_SUBTITLE = "Baseline"
EX3_HIGHEST_SUBTITLE = "With QDHC (Highest tier)"
EX3_INCLUDED_SUBTITLE = "With QDHC (Expert tier included)"

# Figure text settings: edit these values directly to adjust all fonts in the figure.
FONT_FAMILY = "Arial"
TITLE_FONT_SIZE = 25
SUBTITLE_FONT_SIZE = 20
AXIS_LABEL_FONT_SIZE = 18
TICK_FONT_SIZE = 16
CELL_FONT_SIZE = 17


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot confusion matrices for ex1/ex3 tier-assignment runs, including OOS predictions."
    )
    parser.add_argument(
        "--input",
        default="result_data_origin.csv",
        help="Input CSV file. Defaults to result_data_origin.csv in the current directory.",
    )
    parser.add_argument(
        "--output",
        default="tier_assignment_confusion_matrices_with_oos.png",
        help="Output image path. Defaults to tier_assignment_confusion_matrices_with_oos.png.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=15,
        help="Number of leading non-OOS expert-tier queries to include. Defaults to 15.",
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
        return [
            part.strip()
            for part in content.split("->")
            if part.strip() in PREDICTED_TIER_ORDER
        ]

    return [value] if value in PREDICTED_TIER_ORDER else []


def final_tier(prediction: str) -> str | None:
    tiers = extract_tiers(prediction)
    if tiers:
        return max(tiers, key=lambda tier: PREDICTED_TIER_ORDER[tier])

    value = (prediction or "").strip()
    return value if value in PREDICTED_TIER_ORDER else None


def expert_tier_or_final_tier(prediction: str, expert_tier: str) -> str | None:
    tiers = extract_tiers(prediction)
    if tiers:
        if expert_tier in tiers:
            return expert_tier
        return max(tiers, key=lambda tier: PREDICTED_TIER_ORDER[tier])

    value = (prediction or "").strip()
    return value if value in PREDICTED_TIER_ORDER else None


def select_non_oos_rows(rows: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    selected_rows = [
        row for row in rows if (row.get("expert_tier") or "").strip() in TRUE_TIER_ORDER
    ]
    if len(selected_rows) < limit:
        raise ValueError(
            f"Found only {len(selected_rows)} non-OOS expert-tier rows, fewer than --limit={limit}."
        )
    return selected_rows[:limit]


def build_run_matrix(
    rows: list[dict[str, str]],
    run_column: str,
    prediction_resolver,
) -> np.ndarray:
    matrix = np.zeros((len(TRUE_TIERS), len(PREDICTED_TIERS)), dtype=float)

    for row in rows:
        expert_tier = (row.get("expert_tier") or "").strip()
        predicted_tier = prediction_resolver(row.get(run_column, ""), expert_tier)
        if expert_tier not in TRUE_TIER_ORDER or predicted_tier not in PREDICTED_TIER_ORDER:
            continue

        row_index = TRUE_TIER_ORDER[expert_tier]
        column_index = PREDICTED_TIER_ORDER[predicted_tier]
        matrix[row_index, column_index] += 1

    return matrix


def aggregate_matrices(
    rows: list[dict[str, str]],
    run_columns: list[str],
    prediction_resolver,
) -> np.ndarray:
    per_run = [build_run_matrix(rows, column, prediction_resolver) for column in run_columns]
    stacked = np.stack(per_run, axis=0)
    return stacked.mean(axis=0)


def format_cell(value: float, use_integer: bool) -> str:
    if use_integer:
        return str(int(round(value)))
    return f"{value:.1f}"


def draw_matrix(
    ax: plt.Axes,
    matrix: np.ndarray,
    title: str,
    vmax: float,
    cmap: str,
    use_integer_labels: bool,
) -> AxesImage:
    image = ax.imshow(matrix, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
    threshold = vmax * 0.55 if vmax else 0.0

    for row_index in range(matrix.shape[0]):
        for column_index in range(matrix.shape[1]):
            value = matrix[row_index, column_index]
            color = "white" if value > threshold else "#1F1F1F"
            ax.text(
                column_index,
                row_index,
                format_cell(value, use_integer_labels),
                ha="center",
                va="center",
                fontsize=CELL_FONT_SIZE,
                fontweight="bold",
                color=color,
            )

    ax.set_xticks(range(len(PREDICTED_TIERS)))
    ax.set_yticks(range(len(TRUE_TIERS)))
    ax.set_xticklabels(PREDICTED_TIERS, fontsize=TICK_FONT_SIZE, fontweight="bold")
    ax.set_yticklabels(TRUE_TIERS, fontsize=TICK_FONT_SIZE, fontweight="bold")
    ax.set_xlabel("Predicted tier", fontsize=AXIS_LABEL_FONT_SIZE, fontweight="bold")
    ax.set_ylabel("Expert tier", fontsize=AXIS_LABEL_FONT_SIZE, fontweight="bold")
    ax.set_title(title, fontsize=SUBTITLE_FONT_SIZE, fontweight="bold", pad=10)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xticks(np.arange(-0.5, len(PREDICTED_TIERS), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(TRUE_TIERS), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=1.5)
    ax.tick_params(which="minor", bottom=False, left=False)
    return image


def plot_matrices(
    ex1_highest_mean: np.ndarray,
    ex3_highest_mean: np.ndarray,
    ex3_included_mean: np.ndarray,
    output_path: Path,
) -> None:
    plt.style.use("seaborn-v0_8-white")
    rcParams["font.family"] = [FONT_FAMILY]

    fig, axes = plt.subplots(1, 3, figsize=(15.2, 4.4), dpi=600, constrained_layout=True)

    highest_vmax = float(max(ex1_highest_mean.max(), ex3_highest_mean.max()))
    included_vmax = float(ex3_included_mean.max())

    draw_matrix(
        axes[0],
        ex1_highest_mean,
        EX1_HIGHEST_SUBTITLE,
        highest_vmax,
        "Blues",
        use_integer_labels=False,
    )
    draw_matrix(
        axes[1],
        ex3_highest_mean,
        EX3_HIGHEST_SUBTITLE,
        highest_vmax,
        "Oranges",
        use_integer_labels=False,
    )

    draw_matrix(
        axes[2],
        ex3_included_mean,
        EX3_INCLUDED_SUBTITLE,
        included_vmax,
        "Oranges",
        use_integer_labels=False,
    )

    fig.suptitle(TITLE, fontsize=TITLE_FONT_SIZE, fontweight="bold")
    fig.savefig(output_path, dpi=600, bbox_inches="tight", pad_inches=0.04)
    fig.savefig(output_path.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    rows = read_rows(input_path)
    selected_rows = select_non_oos_rows(rows, args.limit)
    fieldnames = rows[0].keys()

    ex1_runs = get_run_columns(fieldnames, BASELINE_PREFIX)
    ex3_runs = get_run_columns(fieldnames, QDHC_PREFIX)
    if not ex1_runs or not ex3_runs:
        raise ValueError("Missing ex1 or ex3 run columns in the input CSV.")

    ex1_highest_mean = aggregate_matrices(selected_rows, ex1_runs, lambda prediction, _: final_tier(prediction))
    ex3_highest_mean = aggregate_matrices(selected_rows, ex3_runs, lambda prediction, _: final_tier(prediction))
    ex3_included_mean = aggregate_matrices(selected_rows, ex3_runs, expert_tier_or_final_tier)
    plot_matrices(
        ex1_highest_mean,
        ex3_highest_mean,
        ex3_included_mean,
        output_path,
    )

    print(f"Saved figure to {output_path}")
    print(f"Saved figure to {output_path.with_suffix('.svg')}")


if __name__ == "__main__":
    main()
