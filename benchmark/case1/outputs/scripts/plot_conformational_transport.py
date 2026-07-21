#!/usr/bin/env python3
"""Regenerate the two reported Case 1 plots from the processed grid."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


OUTPUT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = OUTPUT_ROOT / "data" / "transmission_grid.csv"
DEFAULT_FIGURES = OUTPUT_ROOT / "figures"
SELECTED_PHI = (0, 30, 60, 120, 150, 180)


def load_grid(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Load a wide phi-by-theta transmission table."""
    frame = pd.read_csv(path)
    if frame.shape[1] < 3:
        raise ValueError("The grid must contain phi and at least two theta columns.")

    phi = pd.to_numeric(frame.iloc[:, 0], errors="raise").to_numpy(dtype=float)
    theta = np.asarray([float(value) for value in frame.columns[1:]], dtype=float)
    transmission = frame.iloc[:, 1:].apply(pd.to_numeric, errors="raise").to_numpy(dtype=float)
    if np.isnan(transmission).any():
        raise ValueError("The transmission grid contains missing values.")

    phi_order = np.argsort(phi)
    theta_order = np.argsort(theta)
    return (
        phi[phi_order],
        theta[theta_order],
        transmission[phi_order][:, theta_order],
    )


def plot_heatmap(
    phi: np.ndarray,
    theta: np.ndarray,
    transmission: np.ndarray,
    output_path: Path,
) -> None:
    fig = plt.figure(figsize=(8.2, 5.6))
    ax = plt.gca()
    image = ax.imshow(
        np.log10(np.clip(transmission, 1e-20, None)),
        origin="lower",
        aspect="auto",
        extent=[theta.min(), theta.max(), phi.min(), phi.max()],
        interpolation="nearest",
    )
    ax.set_xlabel("theta (degrees)")
    ax.set_ylabel("phi (degrees)")
    ax.set_title("log10 Transmission heatmap")
    colorbar = plt.colorbar(image, ax=ax)
    colorbar.set_label("log10(T)")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def plot_cos2_slices(
    phi: np.ndarray,
    theta: np.ndarray,
    transmission: np.ndarray,
    output_path: Path,
) -> None:
    scale_y = 1e3
    cos2_theta = np.cos(np.deg2rad(theta)) ** 2
    fig = plt.figure(figsize=(8.8, 5.4))
    ax = plt.gca()

    for target_phi in SELECTED_PHI:
        row = int(np.argmin(np.abs(phi - target_phi)))
        ax.plot(
            cos2_theta,
            transmission[row] * scale_y,
            marker="o",
            linewidth=2,
            label=f"phi = {phi[row]:g}°",
        )

    ax.set_xlabel(r"$\cos^2(\theta)$")
    ax.set_ylabel(f"Transmission (×{scale_y:g})")
    ax.set_title(r"Transmission vs $\cos^2(\theta)$ (selected $\phi$)")
    ax.set_xlim(1.0, 0.0)
    ax.grid(True, alpha=0.3)
    ax.legend(frameon=True, fontsize=9, ncol=1)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--figures", type=Path, default=DEFAULT_FIGURES)
    args = parser.parse_args()

    args.figures.mkdir(parents=True, exist_ok=True)
    phi, theta, transmission = load_grid(args.data)
    plot_heatmap(phi, theta, transmission, args.figures / "transmission_heatmap_log10.png")
    plot_cos2_slices(phi, theta, transmission, args.figures / "transmission_vs_cos2_theta.png")


if __name__ == "__main__":
    main()
