#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors as mcolors
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = SCRIPT_DIR.parent
DATA_DIR = OUTPUTS_DIR / "data"
FIGURES_DIR = OUTPUTS_DIR / "figures"
CSV_PATH = DATA_DIR / "transport_metrics_with_rr_clusters.csv"


def darken_rgba(rgba: tuple[float, float, float, float], factor: float = 0.72, alpha: float = 1.0) -> tuple[float, float, float, float]:
    r, g, b, _ = rgba
    return (r * factor, g * factor, b * factor, alpha)


def describe_clusters(df: pd.DataFrame, label_col: str) -> str:
    lines: list[str] = []
    for cluster_id in sorted(df[label_col].unique()):
        sub = df[df[label_col] == cluster_id]
        lines.append(f"{label_col} cluster {cluster_id}")
        lines.append(f"  count = {len(sub)}")
        lines.append(
            "  mean(A,B,C) = "
            f"({sub['A_deg'].mean():.2f}, {sub['B_deg'].mean():.2f}, {sub['C_deg'].mean():.2f})"
        )
        lines.append(
            "  median(A,B,C) = "
            f"({sub['A_deg'].median():.2f}, {sub['B_deg'].median():.2f}, {sub['C_deg'].median():.2f})"
        )
        lines.append(
            f"  mean RR = {sub['rectification_ratio_1.718V'].mean():.6f}, "
            f"median RR = {sub['rectification_ratio_1.718V'].median():.6f}"
        )
        lines.append(
            f"  mean log10(RR) = {sub['log10_rectification_ratio_1.718V'].mean():.6f}, "
            f"median log10(RR) = {sub['log10_rectification_ratio_1.718V'].median():.6f}"
        )
        lines.append(
            "  ranges: "
            f"A=[{sub['A_deg'].min()}, {sub['A_deg'].max()}], "
            f"B=[{sub['B_deg'].min()}, {sub['B_deg'].max()}], "
            f"C=[{sub['C_deg'].min()}, {sub['C_deg'].max()}]"
        )
        lines.append("")
    return "\n".join(lines)


def make_cluster_plot(df: pd.DataFrame, label_col: str, title: str, outfile: Path) -> None:
    fig = plt.figure(figsize=(9, 7), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")

    palette = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2", "#B279A2"]
    for idx, cluster_id in enumerate(sorted(df[label_col].unique())):
        sub = df[df[label_col] == cluster_id]
        ax.scatter(
            sub["A_deg"],
            sub["B_deg"],
            sub["C_deg"],
            s=80,
            c=palette[idx % len(palette)],
            edgecolors="none",
            alpha=0.78,
            depthshade=False,
            label=(
                f"Cluster {cluster_id}: n={len(sub)}, "
                f"median log10(RR)={sub['log10_rectification_ratio_1.718V'].median():.2f}"
            ),
        )

    ax.set_xlabel("A (deg)", labelpad=8)
    ax.set_ylabel("B (deg)", labelpad=8)
    ax.set_zlabel("C (deg)", labelpad=8)
    ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_yticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_zticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_title(title, pad=18)
    ax.view_init(elev=22, azim=40)
    ax.grid(True, alpha=0.18)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_alpha(0.05)
        axis.pane.set_edgecolor("#BBBBBB")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), fontsize=8)

    fig.savefig(outfile, dpi=300)
    plt.close(fig)


def make_cluster_envelope_plot(df: pd.DataFrame, label_col: str, title: str, outfile: Path) -> None:
    fig = plt.figure(figsize=(9.5, 7.5), constrained_layout=True)
    fig.patch.set_facecolor("#f2f2f2")
    ax = fig.add_subplot(111, projection="3d")

    values = df["log10_rectification_ratio_1.718V"].to_numpy()
    norm = mcolors.TwoSlopeNorm(vmin=float(values.min()), vcenter=0.0, vmax=float(values.max()))
    cmap = plt.get_cmap("RdBu_r")
    strength = np.abs(values) / max(np.abs(values.min()), np.abs(values.max()))
    rgba = cmap(norm(values))
    rgba[:, 3] = 0.04 + 0.18 * strength
    sizes = 3.0 + 5.0 * strength

    ax.scatter(
        df["A_deg"],
        df["B_deg"],
        df["C_deg"],
        c=rgba,
        s=sizes,
        edgecolors="none",
        depthshade=False,
    )

    hull_colors = ["#1B5E20", "#C96A12", "#2E6EA6", "#A63A3A", "#5E4FA2", "#2F7F8C"]
    for idx, cluster_id in enumerate(sorted(df[label_col].unique())):
        sub = df[df[label_col] == cluster_id]
        points = sub[["A_deg", "B_deg", "C_deg"]].to_numpy()
        if len(points) < 4:
            continue
        try:
            hull = ConvexHull(points)
        except Exception:
            continue
        face_color = hull_colors[idx % len(hull_colors)]
        border_color = darken_rgba(mcolors.to_rgba(face_color), factor=0.72, alpha=1.0)
        faces = [points[simplex] for simplex in hull.simplices]
        poly = Poly3DCollection(
            faces,
            facecolors=face_color,
            edgecolors="none",
            linewidths=0.0,
            alpha=0.34,
        )
        ax.add_collection3d(poly)

        centroid = points.mean(axis=0)
        ax.text(
            centroid[0],
            centroid[1],
            centroid[2],
            f"C{cluster_id}",
            color=face_color,
            fontsize=10,
            fontweight="bold",
        )

        # Highlight representative points:
        # 1) Typical point = nearest to cluster center in standardized feature space
        # 2) Extreme point = maximum |log10(RR)| within the cluster
        cluster_center = sub[["A_deg", "B_deg", "C_deg", "log10_rectification_ratio_1.718V"]].mean().to_numpy()
        features = sub[["A_deg", "B_deg", "C_deg", "log10_rectification_ratio_1.718V"]].to_numpy()
        typical_local_idx = int(np.argmin(np.sum((features - cluster_center) ** 2, axis=1)))
        typical_row = sub.iloc[typical_local_idx]

        rr_abs = np.abs(sub["log10_rectification_ratio_1.718V"].to_numpy())
        extreme_order = np.argsort(rr_abs)[::-1]
        extreme_local_idx = int(extreme_order[0])
        if extreme_local_idx == typical_local_idx and len(extreme_order) > 1:
            extreme_local_idx = int(extreme_order[1])
        extreme_row = sub.iloc[extreme_local_idx]

        for row, marker, label_prefix, size in [
            (typical_row, "o", "typ", 180),
            (extreme_row, "D", "ext", 220),
        ]:
            point_rgba = mcolors.to_rgba(face_color, alpha=1.0)
            ax.scatter(
                [row["A_deg"]],
                [row["B_deg"]],
                [row["C_deg"]],
                s=size,
                c=[point_rgba],
                edgecolors=[border_color],
                linewidths=2.1,
                depthshade=False,
                zorder=10,
            )
            rr_value = float(row["rectification_ratio_1.718V"])
            ax.text(
                float(row["A_deg"]) + 1.5,
                float(row["B_deg"]) + 1.5,
                float(row["C_deg"]) + 1.5,
                (
                    f"{label_prefix}{cluster_id}\n"
                    f"A/B/C=({int(row['A_deg'])},{int(row['B_deg'])},{int(row['C_deg'])})\n"
                    f"RR={rr_value:.2f}"
                ),
                color="black",
                fontsize=8.5,
                fontweight="bold",
            )

    ax.set_xlabel("A (deg)", labelpad=8)
    ax.set_ylabel("B (deg)", labelpad=8)
    ax.set_zlabel("C (deg)", labelpad=8)
    ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_yticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_zticks([0, 15, 30, 45, 60, 75, 90])
    ax.set_title(title, pad=18)
    ax.view_init(elev=22, azim=38)
    ax.grid(True, alpha=0.18)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_alpha(0.16)
        axis.pane.set_facecolor("#f2f2f2")
        axis.pane.set_edgecolor("#BBBBBB")

    mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array([])
    cbar = fig.colorbar(mappable, ax=ax, pad=0.08, shrink=0.82)
    cbar.set_label(r"$\log_{10} RR(1.718\,V)$")

    legend_handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="white", markeredgecolor="black", markersize=8, label="Typical point"),
        Line2D([0], [0], marker="D", color="w", markerfacecolor="white", markeredgecolor="black", markersize=8, label="Extreme point"),
    ]
    ax.legend(handles=legend_handles, loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize=8)

    fig.savefig(outfile, dpi=300, facecolor=fig.get_facecolor())
    plt.close(fig)


def main() -> None:
    df = pd.read_csv(CSV_PATH)
    feature_cols = ["A_deg", "B_deg", "C_deg", "log10_rectification_ratio_1.718V"]
    X = df[feature_cols].to_numpy()
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    scores = []
    for k in range(2, 7):
        model = KMeans(n_clusters=k, n_init=20, random_state=0)
        labels = model.fit_predict(Xs)
        score = silhouette_score(Xs, labels)
        scores.append((k, score, model.inertia_))

    lines = ["KMeans model selection on [A, B, C, log10(RR)]", ""]
    for k, score, inertia in scores:
        lines.append(f"k={k}: silhouette={score:.6f}, inertia={inertia:.6f}")
    lines.append("")

    # Stable coarse partition
    km2 = KMeans(n_clusters=2, n_init=20, random_state=0).fit(Xs)
    df["rr_cluster_k2"] = km2.labels_
    lines.append(describe_clusters(df, "rr_cluster_k2"))

    # More detailed region partition for visualization
    km4 = KMeans(n_clusters=4, n_init=20, random_state=0).fit(Xs)
    df["rr_cluster_k4"] = km4.labels_
    lines.append(describe_clusters(df, "rr_cluster_k4"))

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "rectification_cluster_summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    df.to_csv(DATA_DIR / "transport_metrics_with_rr_clusters.csv", index=False)

    make_cluster_plot(
        df,
        "rr_cluster_k2",
        "Stable 2-Cluster Partition of Rectification Behavior",
        FIGURES_DIR / "rectification_clusters_k2.png",
    )
    make_cluster_plot(
        df,
        "rr_cluster_k4",
        "4-Cluster Partition of Rectification Regions",
        FIGURES_DIR / "rectification_clusters_k4.png",
    )
    make_cluster_envelope_plot(
        df,
        "rr_cluster_k4",
        "Rectification Map with Cluster Envelopes",
        FIGURES_DIR / "rectification_clusters_k4_envelope.png",
    )

    print(f"Saved rectification clustering data to {DATA_DIR} and figures to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
