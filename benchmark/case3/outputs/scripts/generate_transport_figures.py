#!/usr/bin/env python3

from __future__ import annotations

import math
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = SCRIPT_DIR.parent
ROOT = OUTPUTS_DIR / "raw"
DATA_DIR = OUTPUTS_DIR / "data"
FIGURES_DIR = OUTPUTS_DIR / "figures"
ANGLE_VALUES = [0, 15, 30, 45, 60, 75, 90]
V_TARGET = 1.718


def parse_angles(path: Path) -> tuple[int, int, int]:
    match = re.search(r"A(\d{3})_B(\d{3})_C(\d{3})", path.name)
    if not match:
        raise ValueError(f"Could not parse angles from {path.name}")
    return tuple(int(group) for group in match.groups())


def load_transmission_ef_zero(path: Path) -> float:
    data = np.loadtxt(path, skiprows=1)
    energies = data[:, 0]
    trans = data[:, 1]
    return float(np.interp(0.0, energies, trans))


def load_voltage_current(path: Path) -> tuple[float, float]:
    data = np.loadtxt(path, skiprows=1)
    voltages = data[:, 0]
    currents = data[:, 1]
    i_plus = float(np.interp(V_TARGET, voltages, currents))
    i_minus = float(np.interp(-V_TARGET, voltages, currents))
    return i_plus, i_minus


def build_dataframe() -> pd.DataFrame:
    rows: list[dict[str, float | int | str]] = []
    for cdir in sorted(ROOT.glob("A_*/B_*/C_*")):
        if not cdir.is_dir():
            continue
        trans_file = cdir / "Field_0.0000" / "Transmission.txt"
        iv_file = cdir / "voltage_current.txt"
        if not trans_file.is_file() or not iv_file.is_file():
            continue

        junction_file = next(cdir.glob("junction_dpdp_A*_B*_C*.xyz"))
        angle_a, angle_b, angle_c = parse_angles(junction_file)
        t_ef = load_transmission_ef_zero(trans_file)
        i_plus, i_minus = load_voltage_current(iv_file)
        abs_i_plus = abs(i_plus)
        abs_i_minus = abs(i_minus)
        rr = abs_i_plus / abs_i_minus if abs_i_minus > 0 else math.inf
        log_rr = math.log10(rr) if rr > 0 and math.isfinite(rr) else math.nan

        rows.append(
            {
                "A_deg": angle_a,
                "B_deg": angle_b,
                "C_deg": angle_c,
                "transmission_file": str(trans_file.relative_to(ROOT)),
                "t_ef_0V": t_ef,
                "log10_t_ef_0V": math.log10(t_ef),
                "i_plus_1.718V_A": i_plus,
                "i_minus_1.718V_A": i_minus,
                "abs_i_plus_1.718V_A": abs_i_plus,
                "abs_i_minus_1.718V_A": abs_i_minus,
                "rectification_ratio_1.718V": rr,
                "log10_rectification_ratio_1.718V": log_rr,
            }
        )

    if not rows:
        raise RuntimeError("No completed transport results found.")
    return pd.DataFrame(rows).sort_values(["A_deg", "B_deg", "C_deg"]).reset_index(drop=True)


def write_summary(df: pd.DataFrame) -> None:
    csv_path = DATA_DIR / "transport_metrics_summary.csv"
    df.to_csv(csv_path, index=False)

    stats_lines = [
        f"Structure count: {len(df)}",
        f"T(E_F, 0 V) min: {df['t_ef_0V'].min():.8e}",
        f"T(E_F, 0 V) max: {df['t_ef_0V'].max():.8e}",
        f"T(E_F, 0 V) mean: {df['t_ef_0V'].mean():.8e}",
        f"log10 T(E_F, 0 V) min: {df['log10_t_ef_0V'].min():.6f}",
        f"log10 T(E_F, 0 V) max: {df['log10_t_ef_0V'].max():.6f}",
        f"Rectification ratio @ 1.718 V min: {df['rectification_ratio_1.718V'].min():.6f}",
        f"Rectification ratio @ 1.718 V max: {df['rectification_ratio_1.718V'].max():.6f}",
        f"Rectification ratio @ 1.718 V mean: {df['rectification_ratio_1.718V'].mean():.6f}",
    ]
    (DATA_DIR / "transport_metrics_summary.txt").write_text("\n".join(stats_lines) + "\n", encoding="utf-8")


def make_3d_heatmap(
    df: pd.DataFrame,
    value_col: str,
    title: str,
    cbar_label: str,
    outfile: Path,
    cmap_name: str,
    alpha_mode: str,
    center_value: float | None = None,
) -> None:
    fig = plt.figure(figsize=(9, 7), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")

    x = df["A_deg"].to_numpy()
    y = df["B_deg"].to_numpy()
    z = df["C_deg"].to_numpy()
    values = df[value_col].to_numpy()

    if alpha_mode == "value":
        norm = mcolors.Normalize(vmin=float(values.min()), vmax=float(values.max()))
        alpha_scale = norm(values)
        cmap = plt.get_cmap(cmap_name)
        rgba = cmap(alpha_scale)
        rgba[:, 3] = 0.18 + 0.82 * alpha_scale
    elif alpha_mode == "distance":
        if center_value is None:
            raise ValueError("center_value is required when alpha_mode='distance'")
        max_delta = float(np.max(np.abs(values - center_value)))
        if max_delta == 0:
            max_delta = 1.0
        norm = mcolors.TwoSlopeNorm(vmin=float(values.min()), vcenter=center_value, vmax=float(values.max()))
        strength = np.abs(values - center_value) / max_delta
        cmap = plt.get_cmap(cmap_name)
        rgba = cmap(norm(values))
        rgba[:, 3] = 0.18 + 0.82 * strength
    else:
        raise ValueError(f"Unsupported alpha_mode: {alpha_mode}")

    sizes = 40.0 + 80.0 * rgba[:, 3]
    scatter = ax.scatter(
        x,
        y,
        z,
        c=rgba,
        s=sizes,
        edgecolors="none",
        linewidths=0.0,
        depthshade=False,
    )

    ax.set_xlabel("A (deg)", labelpad=8)
    ax.set_ylabel("B (deg)", labelpad=8)
    ax.set_zlabel("C (deg)", labelpad=8)
    ax.set_xticks(ANGLE_VALUES)
    ax.set_yticks(ANGLE_VALUES)
    ax.set_zticks(ANGLE_VALUES)
    ax.set_title(title, pad=18)
    ax.view_init(elev=22, azim=38)
    ax.grid(True, alpha=0.18)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_alpha(0.05)
        axis.pane.set_edgecolor("#BBBBBB")

    mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array([])
    cbar = fig.colorbar(mappable, ax=ax, pad=0.08, shrink=0.82)
    cbar.set_label(cbar_label)

    fig.savefig(outfile, dpi=300)
    plt.close(fig)


def make_main_effect_plot(df: pd.DataFrame) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)
    metrics = [
        ("log10_t_ef_0V", r"$\log_{10} T(E_F, 0)$"),
        ("log10_rectification_ratio_1.718V", r"$\log_{10} RR(1.718\,V)$"),
    ]
    angle_cols = ["A_deg", "B_deg", "C_deg"]

    for ax, (metric, ylabel) in zip(axes, metrics):
        for angle_col, marker in zip(angle_cols, ["o", "s", "^"]):
            grouped = df.groupby(angle_col)[metric].mean().reindex(ANGLE_VALUES)
            ax.plot(ANGLE_VALUES, grouped.values, marker=marker, label=angle_col.replace("_deg", ""))
        ax.set_xlabel("Torsion angle (deg)")
        ax.set_ylabel(ylabel)
        ax.set_xticks(ANGLE_VALUES)
        ax.grid(True, alpha=0.3)
        ax.legend()

    fig.suptitle("Main Effects of A/B/C on Transport Metrics", fontsize=14)
    fig.savefig(FIGURES_DIR / "main_effects_transport_metrics.png", dpi=300)
    plt.close(fig)


def make_representative_transmission_plot(df: pd.DataFrame) -> None:
    selected = []
    idx_max_t = df["t_ef_0V"].idxmax()
    idx_min_t = df["t_ef_0V"].idxmin()
    idx_max_rr = df["rectification_ratio_1.718V"].idxmax()
    ref = df[(df["A_deg"] == 0) & (df["B_deg"] == 0) & (df["C_deg"] == 0)].index[0]

    for label, idx in [
        ("max T(E_F,0)", idx_max_t),
        ("min T(E_F,0)", idx_min_t),
        ("max RR", idx_max_rr),
        ("A=B=C=0", ref),
    ]:
        if idx not in [item[1] for item in selected]:
            selected.append((label, idx))

    fig, ax = plt.subplots(figsize=(7.5, 5.5), constrained_layout=True)
    for label, idx in selected:
        row = df.loc[idx]
        trans_path = ROOT / Path(row["transmission_file"])
        data = np.loadtxt(trans_path, skiprows=1)
        energies = data[:, 0]
        trans = data[:, 1]
        ax.plot(energies, np.log10(np.clip(trans, 1e-20, None)), label=f"{label}: A{int(row['A_deg'])}/B{int(row['B_deg'])}/C{int(row['C_deg'])}")

    ax.axvline(0.0, color="black", linestyle="--", linewidth=1)
    ax.set_xlabel("Energy relative to $E_F$ (eV)")
    ax.set_ylabel(r"$\log_{10} T(E)$")
    ax.set_title("Representative Zero-Field Transmission Spectra")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.savefig(FIGURES_DIR / "representative_transmission_spectra.png", dpi=300)
    plt.close(fig)


def make_conductance_histogram(df: pd.DataFrame) -> None:
    conductance = df["t_ef_0V"].to_numpy()
    positive = conductance[conductance > 0]
    if positive.size == 0:
        raise RuntimeError("No positive conductance values found for histogram.")

    log_min = np.floor(np.log10(positive.min()))
    log_max = np.ceil(np.log10(positive.max()))
    bins = np.logspace(log_min, log_max, 18)

    fig, ax = plt.subplots(figsize=(7.5, 5.5), constrained_layout=True)
    ax.hist(
        positive,
        bins=bins,
        color="#4C78A8",
        edgecolor="black",
        alpha=0.85,
    )
    ax.set_xscale("log")
    ax.set_xlabel(r"Zero-bias conductance $G/G_0 \approx T(E_F, 0)$")
    ax.set_ylabel("Count")
    ax.set_title("Histogram of Zero-Bias Conductance Across 343 Conformations")
    ax.grid(True, which="both", axis="x", alpha=0.25)

    mean_val = positive.mean()
    median_val = np.median(positive)
    ax.axvline(mean_val, color="#E45756", linestyle="--", linewidth=1.5, label=f"Mean = {mean_val:.2e}")
    ax.axvline(median_val, color="#54A24B", linestyle=":", linewidth=1.8, label=f"Median = {median_val:.2e}")
    ax.legend()

    fig.savefig(FIGURES_DIR / "conductance_histogram_zero_bias.png", dpi=300)
    plt.close(fig)


def make_rectification_histogram(df: pd.DataFrame) -> None:
    rr = df["rectification_ratio_1.718V"].to_numpy()
    log_rr = df["log10_rectification_ratio_1.718V"].to_numpy()

    positive_rr = rr[rr > 0]
    if positive_rr.size == 0:
        raise RuntimeError("No positive rectification ratios found for histogram.")

    log_min = np.floor(np.log10(positive_rr.min()))
    log_max = np.ceil(np.log10(positive_rr.max()))
    rr_bins = np.logspace(log_min, log_max, 18)

    log_rr_min = np.floor(log_rr.min() * 2.0) / 2.0
    log_rr_max = np.ceil(log_rr.max() * 2.0) / 2.0
    log_rr_bins = np.linspace(log_rr_min, log_rr_max, 18)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), constrained_layout=True)

    axes[0].hist(
        positive_rr,
        bins=rr_bins,
        color="#F58518",
        edgecolor="black",
        alpha=0.85,
    )
    axes[0].set_xscale("log")
    axes[0].set_xlabel(r"Rectification ratio $RR = |I(+1.718V)|/|I(-1.718V)|$")
    axes[0].set_ylabel("Count")
    axes[0].set_title("Histogram of Rectification Ratio")
    axes[0].grid(True, which="both", axis="x", alpha=0.25)
    axes[0].axvline(1.0, color="black", linestyle="--", linewidth=1.2)

    axes[1].hist(
        log_rr,
        bins=log_rr_bins,
        color="#72B7B2",
        edgecolor="black",
        alpha=0.85,
    )
    axes[1].set_xlabel(r"$\log_{10} RR(1.718V)$")
    axes[1].set_ylabel("Count")
    axes[1].set_title(r"Histogram of $\log_{10} RR$")
    axes[1].grid(True, axis="y", alpha=0.25)
    axes[1].axvline(0.0, color="black", linestyle="--", linewidth=1.2)

    fig.suptitle("Rectification Statistics Across 343 Conformations", fontsize=14)
    fig.savefig(FIGURES_DIR / "rectification_histograms.png", dpi=300)
    plt.close(fig)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df = build_dataframe()
    write_summary(df)
    make_3d_heatmap(
        df,
        "log10_t_ef_0V",
        r"3D Map of Zero-Bias Conductance: $\log_{10} T(E_F, 0)$",
        r"$\log_{10} T(E_F, 0)$",
        FIGURES_DIR / "heatmaps_log10_Tef0_by_A.png",
        "Blues",
        "value",
    )
    make_3d_heatmap(
        df,
        "log10_rectification_ratio_1.718V",
        r"3D Map of Rectification at $\pm 1.718$ V: $\log_{10} RR$",
        r"$\log_{10} RR(1.718\,V)$",
        FIGURES_DIR / "heatmaps_log10_RR_by_A.png",
        "RdBu_r",
        "distance",
        center_value=0.0,
    )
    make_main_effect_plot(df)
    make_representative_transmission_plot(df)
    make_conductance_histogram(df)
    make_rectification_histogram(df)
    print(f"Generated analysis data in {DATA_DIR} and figures in {FIGURES_DIR}")


if __name__ == "__main__":
    main()
