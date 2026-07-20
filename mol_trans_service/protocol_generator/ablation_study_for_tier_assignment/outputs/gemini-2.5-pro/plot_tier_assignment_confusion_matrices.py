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


TIERS = ("L1", "L2", "L3")
BASELINE_PREFIX = "ex1_"
QDHC_PREFIX = "ex3_"
TIER_ORDER = {tier: index for index, tier in enumerate(TIERS, start=1)}

TITLE = "Tier Assignment Confusion Matrices"
SUBTITLE_TEMPLATE = "{label} ({mode})"
AVG_MODE = "Mean across 3 runs"
TOTAL_MODE = "Total across 3 runs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot confusion matrices for ex1/ex3 tier-assignment runs."
    )
    parser.add_argument(
        "--input",
        default="result_data_origin.csv",
        help="Input CSV file. Defaults to result_data_origin.csv in the current directory.",
    )
    parser.add_argument(
        "--output",
        default="tier_assignment_confusion_matrices.png",
        help="Output image path. Defaults to tier_assignment_confusion_matrices.png.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=15,
        help="Number of leading queries to include. Defaults to 15.",
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


def build_run_matrix(rows: list[dict[str, str]], run_column: str) -> np.ndarray:
    matrix = np.zeros((len(TIERS), len(TIERS)), dtype=float)

    for row in rows:
        expert_tier = (row.get("expert_tier") or "").strip()
        predicted_tier = final_tier(row.get(run_column, ""))
        if expert_tier not in TIER_ORDER or predicted_tier not in TIER_ORDER:
            continue

        row_index = TIER_ORDER[expert_tier] - 1
        column_index = TIER_ORDER[predicted_tier] - 1
        matrix[row_index, column_index] += 1

    return matrix


def aggregate_matrices(
    rows: list[dict[str, str]], run_columns: list[str]
) -> tuple[np.ndarray, np.ndarray]:
    per_run = [build_run_matrix(rows, column) for column in run_columns]
    stacked = np.stack(per_run, axis=0)
    mean_matrix = stacked.mean(axis=0)
    total_matrix = stacked.sum(axis=0)
    return mean_matrix, total_matrix


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
    image = ax.imshow(matrix, cmap=cmap, vmin=0, vmax=vmax)
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
                fontsize=12,
                fontweight="bold",
                color=color,
            )

    ax.set_xticks(range(len(TIERS)))
    ax.set_yticks(range(len(TIERS)))
    ax.set_xticklabels(TIERS, fontsize=12, fontweight="bold")
    ax.set_yticklabels(TIERS, fontsize=12, fontweight="bold")
    ax.set_xlabel("Predicted tier", fontsize=13, fontweight="bold")
    ax.set_ylabel("Expert tier", fontsize=13, fontweight="bold")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=10)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_xticks(np.arange(-0.5, len(TIERS), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(TIERS), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=1.5)
    ax.tick_params(which="minor", bottom=False, left=False)
    return image


def plot_matrices(
    ex1_mean: np.ndarray,
    ex1_total: np.ndarray,
    ex3_mean: np.ndarray,
    ex3_total: np.ndarray,
    output_path: Path,
) -> None:
    plt.style.use("seaborn-v0_8-white")
    rcParams["font.family"] = ["Arial"]

    fig, axes = plt.subplots(2, 2, figsize=(10.5, 8.4), dpi=600, constrained_layout=True)

    mean_vmax = float(max(ex1_mean.max(), ex3_mean.max()))
    total_vmax = float(max(ex1_total.max(), ex3_total.max()))

    ex1_mean_image = draw_matrix(
        axes[0, 0],
        ex1_mean,
        SUBTITLE_TEMPLATE.format(label="ex1", mode=AVG_MODE),
        mean_vmax,
        "Blues",
        use_integer_labels=False,
    )
    ex3_mean_image = draw_matrix(
        axes[0, 1],
        ex3_mean,
        SUBTITLE_TEMPLATE.format(label="ex3", mode=AVG_MODE),
        mean_vmax,
        "Oranges",
        use_integer_labels=False,
    )
    ex1_total_image = draw_matrix(
        axes[1, 0],
        ex1_total,
        SUBTITLE_TEMPLATE.format(label="ex1", mode=TOTAL_MODE),
        total_vmax,
        "Blues",
        use_integer_labels=True,
    )
    ex3_total_image = draw_matrix(
        axes[1, 1],
        ex3_total,
        SUBTITLE_TEMPLATE.format(label="ex3", mode=TOTAL_MODE),
        total_vmax,
        "Oranges",
        use_integer_labels=True,
    )

    mean_colorbar = fig.colorbar(
        ex1_mean_image,
        ax=axes[0, :],
        fraction=0.035,
        pad=0.03,
    )
    mean_colorbar.ax.tick_params(labelsize=11)
    mean_colorbar.set_label("Average query count", fontsize=12, fontweight="bold")

    total_colorbar = fig.colorbar(
        ex1_total_image,
        ax=axes[1, :],
        fraction=0.035,
        pad=0.03,
    )
    total_colorbar.ax.tick_params(labelsize=11)
    total_colorbar.set_label("Total query count", fontsize=12, fontweight="bold")

    fig.suptitle(TITLE, fontsize=18, fontweight="bold")
    fig.savefig(output_path, dpi=600, bbox_inches="tight", pad_inches=0.04)
    fig.savefig(output_path.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    rows = read_rows(input_path)
    if len(rows) < args.limit:
        raise ValueError(f"{input_path} contains only {len(rows)} rows, fewer than --limit={args.limit}.")

    selected_rows = rows[: args.limit]
    fieldnames = rows[0].keys()

    ex1_runs = get_run_columns(fieldnames, BASELINE_PREFIX)
    ex3_runs = get_run_columns(fieldnames, QDHC_PREFIX)
    if not ex1_runs or not ex3_runs:
        raise ValueError("Missing ex1 or ex3 run columns in the input CSV.")

    ex1_mean, ex1_total = aggregate_matrices(selected_rows, ex1_runs)
    ex3_mean, ex3_total = aggregate_matrices(selected_rows, ex3_runs)
    plot_matrices(ex1_mean, ex1_total, ex3_mean, ex3_total, output_path)

    print(f"Saved figure to {output_path}")
    print(f"Saved figure to {output_path.with_suffix('.svg')}")


if __name__ == "__main__":
    main()
