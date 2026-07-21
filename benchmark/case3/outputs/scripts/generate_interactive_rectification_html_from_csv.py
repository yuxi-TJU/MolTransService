#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import cm
from matplotlib import colors as mcolors
from scipy.spatial import ConvexHull


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = SCRIPT_DIR.parent
DATA_DIR = OUTPUTS_DIR / "data"
INTERACTIVE_DIR = OUTPUTS_DIR / "interactive"
DEFAULT_CSV = DATA_DIR / "transport_metrics_with_rr_clusters.csv"
DEFAULT_HTML = INTERACTIVE_DIR / "rectification_clusters_k4_envelope_interactive.html"
REQUIRED_COLUMNS = [
    "A_deg",
    "B_deg",
    "C_deg",
    "rectification_ratio_1.718V",
    "log10_rectification_ratio_1.718V",
    "rr_cluster_k4",
]


def darken_rgba(
    rgba: tuple[float, float, float, float], factor: float = 0.72, alpha: float = 1.0
) -> tuple[float, float, float, float]:
    r, g, b, _ = rgba
    return (r * factor, g * factor, b * factor, alpha)


def rgba_string(rgba: tuple[float, float, float, float]) -> str:
    r, g, b, a = rgba
    return f"rgba({int(round(r * 255))},{int(round(g * 255))},{int(round(b * 255))},{a:.4f})"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an interactive rectification envelope HTML from a CSV file."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help=f"Input CSV path (default: {DEFAULT_CSV.name})",
    )
    parser.add_argument(
        "--html",
        type=Path,
        default=DEFAULT_HTML,
        help=f"Output HTML path (default: {DEFAULT_HTML.name})",
    )
    return parser.parse_args()


def load_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
    return df[REQUIRED_COLUMNS].copy()


def build_traces(df: pd.DataFrame) -> list[dict]:
    values = df["log10_rectification_ratio_1.718V"].to_numpy()
    scale = max(np.abs(values.min()), np.abs(values.max()))
    norm = mcolors.TwoSlopeNorm(vmin=float(values.min()), vcenter=0.0, vmax=float(values.max()))
    cmap = cm.get_cmap("RdBu_r")

    colors: list[str] = []
    sizes: list[float] = []
    hover_text: list[str] = []
    for _, row in df.iterrows():
        value = float(row["log10_rectification_ratio_1.718V"])
        rgba = list(cmap(norm(value)))
        rgba[3] = 0.05 + 0.12 * abs(value) / scale
        colors.append(rgba_string(tuple(rgba)))
        sizes.append(3.5 + 4.5 * abs(value) / scale)
        hover_text.append(
            "<br>".join(
                [
                    f"A = {int(row['A_deg'])}°",
                    f"B = {int(row['B_deg'])}°",
                    f"C = {int(row['C_deg'])}°",
                    f"log10(RR) = {value:.3f}",
                    f"RR = {float(row['rectification_ratio_1.718V']):.3f}",
                ]
            )
        )

    traces: list[dict] = [
        {
            "type": "scatter3d",
            "mode": "markers",
            "name": "All conformations",
            "x": df["A_deg"].tolist(),
            "y": df["B_deg"].tolist(),
            "z": df["C_deg"].tolist(),
            "text": hover_text,
            "hovertemplate": "%{text}<extra></extra>",
            "marker": {
                "size": sizes,
                "color": colors,
                "line": {"width": 0},
                "symbol": "circle",
            },
        }
    ]

    hull_colors = [
        "rgba(27,94,32,0.34)",
        "rgba(201,106,18,0.34)",
        "rgba(46,110,166,0.34)",
        "rgba(166,58,58,0.34)",
    ]
    hull_line_colors = [
        "rgba(27,94,32,0.95)",
        "rgba(201,106,18,0.95)",
        "rgba(46,110,166,0.95)",
        "rgba(166,58,58,0.95)",
    ]

    for idx, cluster_id in enumerate(sorted(df["rr_cluster_k4"].unique())):
        sub = df[df["rr_cluster_k4"] == cluster_id].copy()
        points = sub[["A_deg", "B_deg", "C_deg"]].to_numpy()

        if len(points) >= 4:
            hull = ConvexHull(points)
            traces.append(
                {
                    "type": "mesh3d",
                    "name": f"Cluster {cluster_id} region",
                    "x": points[:, 0].tolist(),
                    "y": points[:, 1].tolist(),
                    "z": points[:, 2].tolist(),
                    "i": hull.simplices[:, 0].tolist(),
                    "j": hull.simplices[:, 1].tolist(),
                    "k": hull.simplices[:, 2].tolist(),
                    "color": hull_colors[idx % len(hull_colors)],
                    "opacity": 0.12,
                    "hoverinfo": "skip",
                    "flatshading": True,
                    "showlegend": True,
                    "contour": {"show": False},
                }
            )

        cluster_center = sub[
            ["A_deg", "B_deg", "C_deg", "log10_rectification_ratio_1.718V"]
        ].mean().to_numpy()
        features = sub[
            ["A_deg", "B_deg", "C_deg", "log10_rectification_ratio_1.718V"]
        ].to_numpy()
        typical_local_idx = int(np.argmin(np.sum((features - cluster_center) ** 2, axis=1)))
        typical_row = sub.iloc[typical_local_idx]

        rr_abs = np.abs(sub["log10_rectification_ratio_1.718V"].to_numpy())
        extreme_order = np.argsort(rr_abs)[::-1]
        extreme_local_idx = int(extreme_order[0])
        if extreme_local_idx == typical_local_idx and len(extreme_order) > 1:
            extreme_local_idx = int(extreme_order[1])
        extreme_row = sub.iloc[extreme_local_idx]

        for row, marker_symbol, name in [
            (typical_row, "circle-open", f"Cluster {cluster_id} typical"),
            (extreme_row, "diamond-open", f"Cluster {cluster_id} extreme"),
        ]:
            value = float(row["log10_rectification_ratio_1.718V"])
            point_rgba = rgba_string(darken_rgba(tuple(cmap(norm(value))), factor=0.68, alpha=1.0))
            traces.append(
                {
                    "type": "scatter3d",
                    "mode": "markers+text",
                    "name": name,
                    "x": [float(row["A_deg"])],
                    "y": [float(row["B_deg"])],
                    "z": [float(row["C_deg"])],
                    "text": [f"{name.split()[-1]} {cluster_id}"],
                    "textposition": "top center",
                    "hovertemplate": (
                        f"A = {int(row['A_deg'])}°<br>"
                        f"B = {int(row['B_deg'])}°<br>"
                        f"C = {int(row['C_deg'])}°<br>"
                        f"log10(RR) = {value:.3f}<br>"
                        f"RR = {float(row['rectification_ratio_1.718V']):.3f}<extra></extra>"
                    ),
                    "marker": {
                        "size": 12 if marker_symbol == "circle-open" else 13,
                        "color": point_rgba,
                        "symbol": marker_symbol,
                        "line": {
                            "color": hull_line_colors[idx % len(hull_line_colors)],
                            "width": 6,
                        },
                    },
                }
            )

    return traces


def build_layout() -> dict:
    return {
        "title": {"text": "Interactive Rectification Map with Cluster Envelopes", "x": 0.5},
        "scene": {
            "xaxis": {"title": "A (deg)", "tickvals": [0, 15, 30, 45, 60, 75, 90]},
            "yaxis": {"title": "B (deg)", "tickvals": [0, 15, 30, 45, 60, 75, 90]},
            "zaxis": {"title": "C (deg)", "tickvals": [0, 15, 30, 45, 60, 75, 90]},
            "camera": {"eye": {"x": 1.55, "y": 1.45, "z": 1.1}},
        },
        "legend": {"x": 0.01, "y": 0.99, "bgcolor": "rgba(255,255,255,0.8)"},
        "margin": {"l": 0, "r": 0, "t": 50, "b": 0},
    }


def write_html(html_path: Path, traces: list[dict], layout: dict) -> None:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Interactive Rectification Map</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
</head>
<body>
  <div id="plot" style="width: 100%; height: 95vh;"></div>
  <script>
    const data = {json.dumps(traces)};
    const layout = {json.dumps(layout)};
    Plotly.newPlot('plot', data, layout, {{
      responsive: true,
      displaylogo: false,
      scrollZoom: true
    }});
  </script>
</body>
</html>
"""
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(html, encoding="utf-8")


def main() -> None:
    args = parse_args()
    df = load_data(args.csv)
    traces = build_traces(df)
    layout = build_layout()
    write_html(args.html, traces, layout)
    print(f"Wrote interactive HTML to {args.html}")


if __name__ == "__main__":
    main()
