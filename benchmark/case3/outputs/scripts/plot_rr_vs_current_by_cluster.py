#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib import font_manager as fm
from scipy.spatial import ConvexHull


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = SCRIPT_DIR.parent
DATA_DIR = OUTPUTS_DIR / "data"
FIGURES_DIR = OUTPUTS_DIR / "figures"
CSV_PATH = DATA_DIR / "transport_metrics_with_rr_clusters.csv"
PNG_PATH = FIGURES_DIR / "rr_vs_current_by_cluster.png"
SVG_PATH = FIGURES_DIR / "rr_vs_current_by_cluster.svg"

FONT_FAMILY = "Arial"
AXIS_LABEL_FONT_SIZE = 20
TITLE_FONT_SIZE = 23
TITLE_PAD = 20
LEGEND_FONT_SIZE = 16
TICK_FONT_SIZE = 15

CLUSTER_COLORS = {
    0: "#1B5E20",
    1: "#C96A12",
    2: "#2E6EA6",
    3: "#A63A3A",
}
CLUSTER_REGION_ALPHA = 0.10
FIXED_REPRESENTATIVE_POINTS = {
    0: (75, 15, 15),
    1: (15, 15, 75),
    2: (15, 90, 15),
    3: (15, 15, 15),
}
REPRESENTATIVE_MARKER = "o"
EXTREME_MARKER = "D"
REPRESENTATIVE_MARKER_SIZE = 160
EXTREME_MARKER_SIZE = 170
BACKGROUND_SCATTER_ALPHA = 0.50
REFERENCE_LINE_COLOR = "#555555"
REFERENCE_LINE_STYLE = "--"
REFERENCE_LINE_WIDTH = 1.4


def load_arial_fonts() -> tuple[fm.FontProperties | None, fm.FontProperties | None]:
    regular_candidates = [
        Path("/usr/share/fonts/truetype/msttcorefonts/Arial.ttf"),
        Path("/usr/share/fonts/truetype/msttcorefonts/arial.ttf"),
    ]
    bold_candidates = [
        Path("/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf"),
        Path("/usr/share/fonts/truetype/msttcorefonts/arialbd.ttf"),
    ]

    regular_prop = None
    bold_prop = None

    for font_path in regular_candidates:
        if font_path.exists():
            fm.fontManager.addfont(str(font_path))
            regular_prop = fm.FontProperties(fname=str(font_path))
            break

    for font_path in bold_candidates:
        if font_path.exists():
            fm.fontManager.addfont(str(font_path))
            bold_prop = fm.FontProperties(fname=str(font_path))
            break

    return regular_prop, bold_prop


def main() -> None:
    regular_font, bold_font = load_arial_fonts()

    df = pd.read_csv(CSV_PATH)
    if "rr_cluster_k4" not in df.columns:
        raise RuntimeError("Column rr_cluster_k4 not found. Run cluster_rectification_regions.py first.")

    plot_df = df.copy()
    plot_df["max_abs_current_A"] = plot_df[["abs_i_plus_1.718V_A", "abs_i_minus_1.718V_A"]].max(axis=1)

    fig, ax = plt.subplots(figsize=(8.8, 6.6), constrained_layout=True)

    for cluster_id in sorted(plot_df["rr_cluster_k4"].unique()):
        sub = plot_df[plot_df["rr_cluster_k4"] == cluster_id].copy()
        color = CLUSTER_COLORS.get(int(cluster_id), "#555555")
        hull_points = np.column_stack(
            [
                sub["log10_rectification_ratio_1.718V"].to_numpy(),
                np.log10(sub["max_abs_current_A"].to_numpy()),
            ]
        )
        if len(hull_points) >= 3:
            hull = ConvexHull(hull_points)
            hull_vertices = hull_points[hull.vertices]
            ax.fill(
                hull_vertices[:, 0],
                10 ** hull_vertices[:, 1],
                facecolor=color,
                edgecolor="none",
                alpha=CLUSTER_REGION_ALPHA,
                zorder=1,
            )

        ax.scatter(
            sub["log10_rectification_ratio_1.718V"],
            sub["max_abs_current_A"],
            s=44,
            c=color,
            alpha=BACKGROUND_SCATTER_ALPHA,
            edgecolors="none",
            label=f"Cluster {cluster_id}",
            zorder=2,
        )

        rep_a, rep_b, rep_c = FIXED_REPRESENTATIVE_POINTS[int(cluster_id)]
        representative_match = sub[
            (sub["A_deg"] == rep_a)
            & (sub["B_deg"] == rep_b)
            & (sub["C_deg"] == rep_c)
        ]
        if len(representative_match) != 1:
            raise RuntimeError(
                f"Expected exactly one representative point for cluster {cluster_id} "
                f"at ({rep_a}, {rep_b}, {rep_c}), found {len(representative_match)}."
            )
        representative_row = representative_match.iloc[0]

        ax.scatter(
            [float(representative_row["log10_rectification_ratio_1.718V"])],
            [float(representative_row["max_abs_current_A"])],
            s=REPRESENTATIVE_MARKER_SIZE,
            c=color,
            marker=REPRESENTATIVE_MARKER,
            edgecolors="black",
            linewidths=1.2,
            zorder=5,
        )

        rr_abs = np.abs(sub["log10_rectification_ratio_1.718V"].to_numpy())
        extreme_local_idx = int(np.argmax(rr_abs))
        extreme_row = sub.iloc[extreme_local_idx]

        ax.scatter(
            [float(extreme_row["log10_rectification_ratio_1.718V"])],
            [float(extreme_row["max_abs_current_A"])],
            s=EXTREME_MARKER_SIZE,
            c=color,
            marker=EXTREME_MARKER,
            edgecolors="black",
            linewidths=1.3,
            zorder=6,
        )

    xlabel = ax.set_xlabel(r"Log$_{10}$(RR)", fontsize=AXIS_LABEL_FONT_SIZE)
    ylabel = ax.set_ylabel("Max(|I(±1.72 V)|) (A)", fontsize=AXIS_LABEL_FONT_SIZE)
    title = ax.set_title("Rectification–Current Performance Map", fontsize=TITLE_FONT_SIZE, pad=TITLE_PAD)
    ax.set_yscale("log")
    ax.axvline(0.0, color=REFERENCE_LINE_COLOR, linestyle=REFERENCE_LINE_STYLE, linewidth=REFERENCE_LINE_WIDTH, zorder=1)
    ax.grid(True, alpha=0.25, linewidth=0.8)
    ax.tick_params(axis="both", labelsize=TICK_FONT_SIZE)
    if bold_font is not None:
        xlabel.set_fontproperties(bold_font)
        ylabel.set_fontproperties(bold_font)
        title.set_fontproperties(bold_font)
        xlabel.set_fontsize(AXIS_LABEL_FONT_SIZE)
        ylabel.set_fontsize(AXIS_LABEL_FONT_SIZE)
        title.set_fontsize(TITLE_FONT_SIZE)
    elif regular_font is not None:
        xlabel.set_fontproperties(regular_font)
        ylabel.set_fontproperties(regular_font)
        title.set_fontproperties(regular_font)
        xlabel.set_fontsize(AXIS_LABEL_FONT_SIZE)
        ylabel.set_fontsize(AXIS_LABEL_FONT_SIZE)
        title.set_fontsize(TITLE_FONT_SIZE)

    if regular_font is not None:
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontproperties(regular_font)
            label.set_fontsize(TICK_FONT_SIZE)

    legend_handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor=CLUSTER_COLORS[0], markeredgecolor="none", markersize=9, label="Cluster 0"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=CLUSTER_COLORS[1], markeredgecolor="none", markersize=9, label="Cluster 1"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=CLUSTER_COLORS[2], markeredgecolor="none", markersize=9, label="Cluster 2"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=CLUSTER_COLORS[3], markeredgecolor="none", markersize=9, label="Cluster 3"),
        Line2D([0], [0], marker=REPRESENTATIVE_MARKER, color="w", markerfacecolor="#7f7f7f", markeredgecolor="black", markersize=9, label="Representative point"),
        Line2D([0], [0], marker=EXTREME_MARKER, color="w", markerfacecolor="#7f7f7f", markeredgecolor="black", markersize=8, label="Extreme point"),
    ]
    legend = ax.legend(
        legend_handles,
        [handle.get_label() for handle in legend_handles],
        loc="best",
        fontsize=LEGEND_FONT_SIZE,
        frameon=True,
    )
    if regular_font is not None:
        for text in legend.get_texts():
            text.set_fontproperties(regular_font)
            text.set_fontsize(LEGEND_FONT_SIZE)

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG_PATH, dpi=600)
    fig.savefig(SVG_PATH)
    plt.close(fig)

    print(f"Wrote {PNG_PATH}")
    print(f"Wrote {SVG_PATH}")


if __name__ == "__main__":
    main()
