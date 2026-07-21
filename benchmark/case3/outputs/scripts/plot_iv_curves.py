from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = SCRIPT_DIR.parent
DATA_DIR = OUTPUTS_DIR / "data"
FIGURES_DIR = OUTPUTS_DIR / "figures"

CONFIG = {
    "data_file": DATA_DIR / "iv_curves_two_junctions.csv",
    "tp_junction": "symmetric_tetraphenyl_control",
    "dpdp_junction": "asymmetric_dpdp",
    "output": FIGURES_DIR / "iv_curves_two_junctions.png",
    "title": "The I-V Curves of Two Junctions",
    "font_family": "Arial",
    "figure_size": (8.8, 6.4),
    "dpi": 600,
    "xlim": (-2.0, 2.0),
    "ylim": (-20.0, 80.0),
    "current_scale": 1e8,
    "tp_label": "symmetric",
    "dpdp_label": "asymmetric",
    "tp_color": "#1f9cf5",
    "dpdp_color": "#ff7f0e",
    "line_width": 2.4,
    "tp_marker_size": 7.2,
    "dpdp_marker_size": 6.8,
}


def load_iv_data(file_path: Path, junction: str):
    data = np.genfromtxt(file_path, delimiter=",", names=True, dtype=None, encoding="utf-8")
    selected = data[data["junction"] == junction]
    if selected.size == 0:
        raise ValueError(f"No rows found for junction {junction!r} in {file_path}")
    voltage = selected["voltage_V"].astype(float)
    current = selected["current_A"].astype(float) * CONFIG["current_scale"]
    return voltage, current


def main():
    plt.rcParams["font.family"] = CONFIG["font_family"]

    tp_v, tp_i = load_iv_data(CONFIG["data_file"], CONFIG["tp_junction"])
    dpdp_v, dpdp_i = load_iv_data(CONFIG["data_file"], CONFIG["dpdp_junction"])

    fig, ax = plt.subplots(figsize=CONFIG["figure_size"], dpi=CONFIG["dpi"])

    ax.plot(
        tp_v,
        tp_i,
        color=CONFIG["tp_color"],
        marker="^",
        markersize=CONFIG["tp_marker_size"],
        linewidth=CONFIG["line_width"],
        label=CONFIG["tp_label"],
    )
    ax.plot(
        dpdp_v,
        dpdp_i,
        color=CONFIG["dpdp_color"],
        marker="o",
        markersize=CONFIG["dpdp_marker_size"],
        linewidth=CONFIG["line_width"],
        label=CONFIG["dpdp_label"],
    )

    ax.set_xlim(*CONFIG["xlim"])
    ax.set_ylim(*CONFIG["ylim"])
    ax.set_xlabel("Voltage (V)", fontsize=20, fontweight="bold", labelpad=8)
    ax.set_ylabel("Current (A)", fontsize=20, fontweight="bold", labelpad=8)
    ax.set_title(CONFIG["title"], fontsize=22, fontweight="bold", pad=16)

    ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.02, 0.98),
        frameon=False,
        fontsize=20,
        handlelength=2.2,
        handletextpad=0.4,
        borderaxespad=0.2,
    )

    ax.text(
        0.0,
        1.01,
        r"$\times 10^{8}$",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=16,
        fontweight="bold",
    )

    ax.set_xticks(np.arange(-2.0, 2.01, 0.5))
    ax.set_yticks(np.arange(-20.0, 81.0, 20.0))
    ax.tick_params(axis="both", direction="in", width=1.6, length=8, labelsize=18, pad=8)

    ax.xaxis.set_major_formatter(plt.FormatStrFormatter("%.1f"))
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter("%.0f"))

    for spine in ax.spines.values():
        spine.set_linewidth(1.6)

    fig.tight_layout()
    CONFIG["output"].parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(CONFIG["output"], dpi=CONFIG["dpi"])
    plt.close(fig)

    print(f"Saved figure to: {CONFIG['output']}")


if __name__ == "__main__":
    main()
