#!/usr/bin/env python3
"""Regenerate the compact L2 and L3 transmission plots for Case 2."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


OUTPUT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = OUTPUT_ROOT / "data"
DEFAULT_FIGURES = OUTPUT_ROOT / "figures"
SYSTEM_ORDER = ("OPA2", "OPA3", "OPA4", "OPM2", "OPM3", "OPM4")
COLORS = {
    "OPA2": "#0072B2",
    "OPA3": "#56B4E9",
    "OPA4": "#A6CEE3",
    "OPM2": "#D55E00",
    "OPM3": "#E69F00",
    "OPM4": "#F0E442",
}


def plot_l2(data_path: Path, output_path: Path) -> None:
    data = pd.read_csv(data_path)
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    for system in SYSTEM_ORDER:
        subset = data[data["system"] == system]
        ax.semilogy(
            subset["energy_eV"],
            subset["transmission"],
            color=COLORS[system],
            linewidth=1.8,
            label=system,
        )
    ax.set_xlim(-12.8, -7.2)
    ax.set_ylim(1e-6, 2.0)
    ax.set_xlabel("Energy (eV)")
    ax.set_ylabel("Transmission")
    ax.set_title("Transmission spectra for six molecules coupled to gold clusters")
    ax.legend(frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_l3(data_path: Path, output_path: Path) -> None:
    data = pd.read_csv(data_path)
    fig, ax = plt.subplots(figsize=(6.0, 4.5))
    for system, color, label in (
        ("OPA3", "#0072B2", "OPA3 (sp)"),
        ("OPM3", "#D62728", "OPM3 (sp3)"),
    ):
        subset = data[data["system"] == system]
        ax.semilogy(
            subset["energy_relative_to_fermi_eV"],
            subset["transmission"],
            color=color,
            linewidth=1.7,
            label=label,
        )
    ax.axvline(0.0, color="black", linestyle="--", linewidth=0.8)
    ax.set_xlim(-4.0, 4.0)
    ax.set_ylim(1e-6, 2.0)
    ax.set_xlabel(r"Energy relative to $E_F$ (eV)")
    ax.set_ylabel("Transmission")
    ax.set_title("Electrode-referenced transmission: OPA3 vs OPM3")
    ax.legend(frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--figures", type=Path, default=DEFAULT_FIGURES)
    args = parser.parse_args()

    args.figures.mkdir(parents=True, exist_ok=True)
    plot_l2(args.data_dir / "l2_transmission_spectra.csv", args.figures / "l2_transmission_spectra.png")
    plot_l3(args.data_dir / "l3_transmission_spectra.csv", args.figures / "l3_transmission_opa3_opm3.png")


if __name__ == "__main__":
    main()
