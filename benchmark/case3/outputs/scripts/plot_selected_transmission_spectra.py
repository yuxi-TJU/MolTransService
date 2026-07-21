#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.offsetbox import AnchoredOffsetbox, HPacker, TextArea
import numpy as np
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = SCRIPT_DIR.parent
DATA_DIR = OUTPUTS_DIR / "data"
FIGURES_DIR = OUTPUTS_DIR / "figures"
METRICS_CSV_PATH = DATA_DIR / "selected_points_metrics.csv"
SPECTRA_CSV_PATH = DATA_DIR / "selected_transmission_spectra.csv"
PNG_PATH = FIGURES_DIR / "selected_rectification_transmission_spectra.png"
SVG_PATH = FIGURES_DIR / "selected_rectification_transmission_spectra.svg"

BIAS_VOLTAGE = 1.718
BIAS_WINDOW_HALF_WIDTH = BIAS_VOLTAGE / 2.0
X_LIMITS = (-1.5, 1.5)
Y_LIMITS = (1.0e-8, 5.0)

FONT_FAMILY = "Arial"
TITLE_FONT_SIZE = 19
SUPTITLE_FONT_SIZE = 26
AXIS_LABEL_FONT_SIZE = 21
TICK_FONT_SIZE = 16
LEGEND_FONT_SIZE = 15
LINE_WIDTH = 1.9
ARIAL_FONT_PATH = Path("/usr/share/fonts/truetype/msttcorefonts/Arial.ttf")
ARIAL_BOLD_FONT_PATH = Path("/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf")

BIAS_WINDOW_LOWER_COLOR = "#d0d0d0"
CLUSTER_UPPER_COLORS = {
    0: "#b9cdba",
    1: "#e9cfb6",
    2: "#bdcfdf",
    3: "#dfc0c0",
}

FIELD_SPECS = [
    ("Field_-0.0015", "-1.72 V", "#1e90ff"),
    ("Field_0.0000", "0 V", "#111111"),
    ("Field_0.0015", "+1.72 V", "#d62728"),
]

SELECTED_POINTS = [
    {
        "cluster": 3,
        "A": 15,
        "B": 15,
        "C": 15,
        "title": "Small A/B/C: forward",
    },
    {
        "cluster": 0,
        "A": 75,
        "B": 15,
        "C": 15,
        "title": "Large A: forward",
    },
    {
        "cluster": 2,
        "A": 15,
        "B": 90,
        "C": 15,
        "title": "Large B: reverse",
    },
    {
        "cluster": 1,
        "A": 15,
        "B": 15,
        "C": 75,
        "title": "Large C: reverse",
    },
]


def load_font_properties() -> tuple[fm.FontProperties, fm.FontProperties]:
    if ARIAL_FONT_PATH.exists() and ARIAL_BOLD_FONT_PATH.exists():
        fm.fontManager.addfont(str(ARIAL_FONT_PATH))
        fm.fontManager.addfont(str(ARIAL_BOLD_FONT_PATH))
        return fm.FontProperties(fname=str(ARIAL_FONT_PATH)), fm.FontProperties(fname=str(ARIAL_BOLD_FONT_PATH))
    return fm.FontProperties(family=FONT_FAMILY), fm.FontProperties(family=FONT_FAMILY, weight="bold")


def get_point_row(df: pd.DataFrame, point: dict[str, int | str]) -> pd.Series:
    match = df[
        (df["A_deg"] == point["A"])
        & (df["B_deg"] == point["B"])
        & (df["C_deg"] == point["C"])
        & (df["rr_cluster_k4"] == point["cluster"])
    ]
    if len(match) != 1:
        raise RuntimeError(
            "Expected exactly one row for "
            f"cluster={point['cluster']}, A/B/C=({point['A']},{point['B']},{point['C']}), "
            f"found {len(match)}."
        )
    return match.iloc[0]


def load_point_curves(
    spectra_df: pd.DataFrame, point_row: pd.Series
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    curves: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for field_dir, _, _ in FIELD_SPECS:
        selected = spectra_df[
            (spectra_df["label"] == point_row["label"])
            & (spectra_df["field_dir"] == field_dir)
        ].sort_values("energy_eV")
        if selected.empty:
            raise RuntimeError(
                f"No transmission data found for label={point_row['label']!r}, "
                f"field_dir={field_dir!r}."
            )
        energies = selected["energy_eV"].to_numpy(dtype=float)
        transmission = np.clip(selected["transmission"].to_numpy(dtype=float), 1.0e-20, None)
        curves[field_dir] = (energies, transmission)
    return curves


def style_axis(
    ax: plt.Axes,
    point: dict[str, int | str],
    row: pd.Series,
    curves: dict[str, tuple[np.ndarray, np.ndarray]],
    *,
    show_ylabel: bool,
    show_legend: bool,
    regular_font: fm.FontProperties,
    bold_font: fm.FontProperties,
) -> None:
    cluster = int(point["cluster"])
    upper_fill_color = CLUSTER_UPPER_COLORS[cluster]

    for field_dir, label, color in FIELD_SPECS:
        energies, transmission = curves[field_dir]
        ax.plot(energies, transmission, color=color, linewidth=LINE_WIDTH, label=label, zorder=3)

    zero_bias_energies, _ = curves["Field_0.0000"]
    window_mask = (
        (zero_bias_energies >= -BIAS_WINDOW_HALF_WIDTH)
        & (zero_bias_energies <= BIAS_WINDOW_HALF_WIDTH)
    )
    x_window = zero_bias_energies[window_mask]
    envelope_curves = []
    for field_dir, _, _ in FIELD_SPECS:
        energies, transmission = curves[field_dir]
        envelope_curves.append(np.interp(x_window, energies, transmission))
    y_window = np.max(np.vstack(envelope_curves), axis=0)

    ax.fill_between(
        x_window,
        y_window,
        Y_LIMITS[1],
        facecolor=upper_fill_color,
        alpha=0.75,
        zorder=0,
    )
    ax.fill_between(
        x_window,
        Y_LIMITS[0],
        y_window,
        facecolor=BIAS_WINDOW_LOWER_COLOR,
        alpha=0.95,
        zorder=0,
    )

    a = int(point["A"])
    b = int(point["B"])
    c = int(point["C"])
    logrr = float(row["log10_rectification_ratio_1.718V"])
    rr = float(row["rectification_ratio_1.718V"])

    ax.set_facecolor("white")
    ax.set_yscale("log")
    ax.set_xlim(*X_LIMITS)
    ax.set_ylim(*Y_LIMITS)
    xlabel = ax.set_xlabel("Energy (eV)")
    ylabel = ax.set_ylabel("Transmission" if show_ylabel else "")
    for text in (xlabel, ylabel):
        text.set_fontproperties(bold_font)
        text.set_fontsize(AXIS_LABEL_FONT_SIZE)

    ax.text(
        0.5,
        1.11,
        str(point["title"]),
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontproperties=bold_font,
        fontsize=TITLE_FONT_SIZE,
        color="black",
    )
    coordinate_text = TextArea(
        f"({a},{b},{c})",
        textprops={
            "color": "#c62828",
            "fontproperties": bold_font,
            "fontsize": TITLE_FONT_SIZE,
        },
    )
    metric_text = TextArea(
        f"  logRR={logrr:.3f}, RR={rr:.2f}",
        textprops={
            "color": "black",
            "fontproperties": bold_font,
            "fontsize": TITLE_FONT_SIZE,
        },
    )
    second_line = HPacker(children=[coordinate_text, metric_text], align="center", pad=0, sep=0)
    anchored_second_line = AnchoredOffsetbox(
        loc="upper center",
        child=second_line,
        frameon=False,
        bbox_to_anchor=(0.5, 1.035),
        bbox_transform=ax.transAxes,
        borderpad=0.0,
        pad=0.0,
    )
    ax.add_artist(anchored_second_line)

    ax.tick_params(axis="both", labelsize=TICK_FONT_SIZE)
    for tick_label in [*ax.get_xticklabels(), *ax.get_yticklabels()]:
        tick_label.set_fontproperties(regular_font)
        tick_label.set_fontsize(TICK_FONT_SIZE)
    for spine in ax.spines.values():
        spine.set_linewidth(1.0)

    if show_legend:
        legend_handles = [
            plt.Line2D([0], [0], color=color, linewidth=LINE_WIDTH, label=label)
            for _, label, color in FIELD_SPECS
        ]
        legend = ax.legend(
            handles=legend_handles,
            loc="lower left",
            frameon=False,
            fontsize=LEGEND_FONT_SIZE,
        )
        for text in legend.get_texts():
            text.set_fontproperties(regular_font)
            text.set_fontsize(LEGEND_FONT_SIZE)


def main() -> None:
    regular_font, bold_font = load_font_properties()
    plt.rcParams["font.family"] = FONT_FAMILY
    metrics_df = pd.read_csv(METRICS_CSV_PATH)
    spectra_df = pd.read_csv(SPECTRA_CSV_PATH)

    fig, axes = plt.subplots(1, 4, figsize=(22.0, 4.9), constrained_layout=False)
    fig.patch.set_facecolor("white")
    fig.subplots_adjust(left=0.055, right=0.995, bottom=0.16, top=0.80, wspace=0.16)

    suptitle = fig.suptitle(
        r"Bias-Dependent Transmission Spectra of Representative Points at 0 and $\pm$1.72 V",
        fontsize=SUPTITLE_FONT_SIZE,
        y=0.98,
    )
    suptitle.set_fontproperties(bold_font)
    suptitle.set_fontsize(SUPTITLE_FONT_SIZE)

    for idx, (ax, point) in enumerate(zip(axes.flat, SELECTED_POINTS)):
        row = get_point_row(metrics_df, point)
        curves = load_point_curves(spectra_df, row)
        style_axis(
            ax,
            point,
            row,
            curves,
            show_ylabel=idx == 0,
            show_legend=idx == 0,
            regular_font=regular_font,
            bold_font=bold_font,
        )

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG_PATH, dpi=600, bbox_inches="tight")
    fig.savefig(SVG_PATH, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG_PATH}")
    print(f"Wrote {SVG_PATH}")


if __name__ == "__main__":
    main()
