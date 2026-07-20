#!/usr/bin/env python3
"""
Compare ex1 (Baseline) vs ex3 (QDHC Guide) tier assignment results.

Supports multi-run: auto-detects all ex1_run* and ex3_run* columns,
computes per-run metrics, and shows mean ± std with error bars.

Reads result_data.csv from the current directory and generates:
  1. A comparison figure (PNG) with error bars
  2. A summary printed to terminal

Two evaluation scenarios:
  A. All 20 queries  — includes OOS recognition metrics
  B. First 15 queries — L1/L2/L3 only (no OOS)

Usage:
    Copy this script into a directory containing result_data.csv, then:
        python plot_comparison.py
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams["font.family"] = "Arial"
matplotlib.rcParams["font.size"] = 12

# Tier ordering for over/under estimation (L1 < L2 < L3)
TIER_RANK = {"L1": 1, "L2": 2, "L3": 3}


def load_csv(csv_path: Path):
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def detect_run_columns(header_keys):
    """Auto-detect ex1_run* and ex3_run* columns."""
    ex1_cols = sorted([k for k in header_keys if re.match(r"ex1_run\d+", k)])
    ex3_cols = sorted([k for k in header_keys if re.match(r"ex3_run\d+", k)])
    return ex1_cols, ex3_cols


def classify_prediction(expert: str, predicted: str):
    if expert == "OOS":
        return "oos_correct" if predicted == "OOS" else "oos_miss"
    if expert not in TIER_RANK or predicted not in TIER_RANK:
        return "other"
    if predicted == expert:
        return "correct"
    elif TIER_RANK[predicted] > TIER_RANK[expert]:
        return "overestimate"
    else:
        return "underestimate"


def compute_stats(rows, ex_col: str, include_oos: bool = True):
    """Compute classification stats for a given experiment column."""
    subset = rows if include_oos else rows[:15]

    total = 0
    correct = 0
    overestimate = 0
    underestimate = 0
    oos_correct = 0
    oos_miss = 0
    other = 0

    per_tier_correct = Counter()
    per_tier_total = Counter()

    for row in subset:
        expert = row["expert_tier"]
        predicted = row.get(ex_col, "").strip()

        if not predicted or predicted.startswith("Error") or predicted == "PARSE_ERROR":
            other += 1
            total += 1
            per_tier_total[expert] += 1
            continue

        if predicted.startswith("STAGED"):
            other += 1
            total += 1
            per_tier_total[expert] += 1
            continue

        total += 1
        per_tier_total[expert] += 1
        cat = classify_prediction(expert, predicted)

        if cat == "correct":
            correct += 1
            per_tier_correct[expert] += 1
        elif cat == "overestimate":
            overestimate += 1
        elif cat == "underestimate":
            underestimate += 1
        elif cat == "oos_correct":
            oos_correct += 1
            correct += 1
            per_tier_correct[expert] += 1
        elif cat == "oos_miss":
            oos_miss += 1
        else:
            other += 1

    return {
        "total": total,
        "correct": correct,
        "overestimate": overestimate,
        "underestimate": underestimate,
        "oos_correct": oos_correct,
        "oos_miss": oos_miss,
        "other": other,
        "accuracy": correct / total if total > 0 else 0,
        "per_tier_correct": dict(per_tier_correct),
        "per_tier_total": dict(per_tier_total),
    }


def compute_multi_run_stats(rows, run_cols, include_oos=True):
    """Compute per-run stats and aggregate mean ± std.

    Returns:
        all_stats: list of per-run stat dicts
        agg: dict of aggregated {metric: (mean, std)}
    """
    all_stats = [compute_stats(rows, col, include_oos) for col in run_cols]

    def agg_metric(key):
        vals = [s[key] for s in all_stats]
        return float(np.mean(vals)), float(np.std(vals, ddof=0))

    agg = {
        "correct": agg_metric("correct"),
        "overestimate": agg_metric("overestimate"),
        "underestimate": agg_metric("underestimate"),
        "oos_miss": agg_metric("oos_miss"),
        "accuracy": agg_metric("accuracy"),
    }

    # Per-tier accuracy
    for tier in ["L1", "L2", "L3", "OOS"]:
        accs = []
        for s in all_stats:
            t = s["per_tier_total"].get(tier, 0)
            c = s["per_tier_correct"].get(tier, 0)
            accs.append((c / t * 100) if t > 0 else 0)
        agg[f"tier_acc_{tier}"] = (float(np.mean(accs)), float(np.std(accs, ddof=0)))

    # Overall accuracy as percentage
    overall_accs = [s["accuracy"] * 100 for s in all_stats]
    agg["overall_acc_pct"] = (float(np.mean(overall_accs)), float(np.std(overall_accs, ddof=0)))

    return all_stats, agg


def plot_comparison(rows, ex1_cols, ex3_cols, model_name, output_path):
    """Generate a comparison figure with error bars."""
    # Multi-run stats
    _, ex1_all = compute_multi_run_stats(rows, ex1_cols, include_oos=True)
    _, ex3_all = compute_multi_run_stats(rows, ex3_cols, include_oos=True)
    _, ex1_15 = compute_multi_run_stats(rows, ex1_cols, include_oos=False)
    _, ex3_15 = compute_multi_run_stats(rows, ex3_cols, include_oos=False)

    n_runs_ex1 = len(ex1_cols)
    n_runs_ex3 = len(ex3_cols)

    fig, axes = plt.subplots(1, 3, figsize=(17, 6))
    fig.suptitle(
        f"Tier Assignment: Baseline (Ex1) vs QDHC Guide (Ex3)\n"
        f"Model: {model_name}  |  Runs: Ex1×{n_runs_ex1}, Ex3×{n_runs_ex3}",
        fontsize=14, fontweight="bold", y=1.02,
    )

    width = 0.35
    capsize = 4
    ex1_style = dict(color="#BBDEFB", edgecolor="#1565C0", linewidth=1.2)
    ex3_style = dict(color="#C8E6C9", edgecolor="#2E7D32", linewidth=1.2)
    err_kw_ex1 = dict(ecolor="#1565C0", capsize=capsize, capthick=1.5, elinewidth=1.5)
    err_kw_ex3 = dict(ecolor="#2E7D32", capsize=capsize, capthick=1.5, elinewidth=1.5)

    def add_value_labels(ax, bars, errs, fmt="{:.1f}"):
        for bar, err in zip(bars, errs):
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + err + 0.3,
                    fmt.format(h), ha="center", va="bottom",
                    fontsize=10, fontweight="bold")

    # ── Panel 1: All 20 queries ──
    ax = axes[0]
    categories = ["Correct", "Over-\nestimate", "Under-\nestimate", "OOS\nmissed"]
    keys = ["correct", "overestimate", "underestimate", "oos_miss"]

    means_ex1 = [ex1_all[k][0] for k in keys]
    stds_ex1 = [ex1_all[k][1] for k in keys]
    means_ex3 = [ex3_all[k][0] for k in keys]
    stds_ex3 = [ex3_all[k][1] for k in keys]

    x = np.arange(len(categories))
    bars1 = ax.bar(x - width / 2, means_ex1, width, yerr=stds_ex1,
                   label="Ex1 (Baseline)", error_kw=err_kw_ex1, **ex1_style)
    bars2 = ax.bar(x + width / 2, means_ex3, width, yerr=stds_ex3,
                   label="Ex3 (QDHC Guide)", error_kw=err_kw_ex3, **ex3_style)

    add_value_labels(ax, bars1, stds_ex1)
    add_value_labels(ax, bars2, stds_ex3)

    ax.set_ylabel("Count (mean)")
    ax.set_title("All 20 Queries", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=10)
    ax.legend(fontsize=10)
    max_val = max(max(m + s for m, s in zip(means_ex1, stds_ex1)),
                  max(m + s for m, s in zip(means_ex3, stds_ex3)))
    ax.set_ylim(0, max_val + 4)

    # ── Panel 2: First 15 queries ──
    ax = axes[1]
    categories_15 = ["Correct", "Over-\nestimate", "Under-\nestimate"]
    keys_15 = ["correct", "overestimate", "underestimate"]

    means_ex1_15 = [ex1_15[k][0] for k in keys_15]
    stds_ex1_15 = [ex1_15[k][1] for k in keys_15]
    means_ex3_15 = [ex3_15[k][0] for k in keys_15]
    stds_ex3_15 = [ex3_15[k][1] for k in keys_15]

    x2 = np.arange(len(categories_15))
    bars1 = ax.bar(x2 - width / 2, means_ex1_15, width, yerr=stds_ex1_15,
                   label="Ex1 (Baseline)", error_kw=err_kw_ex1, **ex1_style)
    bars2 = ax.bar(x2 + width / 2, means_ex3_15, width, yerr=stds_ex3_15,
                   label="Ex3 (QDHC Guide)", error_kw=err_kw_ex3, **ex3_style)

    add_value_labels(ax, bars1, stds_ex1_15)
    add_value_labels(ax, bars2, stds_ex3_15)

    ax.set_ylabel("Count (mean)")
    ax.set_title("First 15 Queries (L1/L2/L3 only)", fontsize=13, fontweight="bold")
    ax.set_xticks(x2)
    ax.set_xticklabels(categories_15, fontsize=10)
    ax.legend(fontsize=10)
    max_val = max(max(m + s for m, s in zip(means_ex1_15, stds_ex1_15)),
                  max(m + s for m, s in zip(means_ex3_15, stds_ex3_15)))
    ax.set_ylim(0, max_val + 4)

    # ── Panel 3: Per-tier accuracy ──
    ax = axes[2]
    tiers_all = ["L1", "L2", "L3", "OOS", "Overall"]
    tier_keys = [f"tier_acc_{t}" for t in ["L1", "L2", "L3", "OOS"]] + ["overall_acc_pct"]

    means_ex1_acc = [ex1_all[k][0] for k in tier_keys]
    stds_ex1_acc = [ex1_all[k][1] for k in tier_keys]
    means_ex3_acc = [ex3_all[k][0] for k in tier_keys]
    stds_ex3_acc = [ex3_all[k][1] for k in tier_keys]

    x3 = np.arange(len(tiers_all))
    bars1 = ax.bar(x3 - width / 2, means_ex1_acc, width, yerr=stds_ex1_acc,
                   label="Ex1 (Baseline)", error_kw=err_kw_ex1, **ex1_style)
    bars2 = ax.bar(x3 + width / 2, means_ex3_acc, width, yerr=stds_ex3_acc,
                   label="Ex3 (QDHC Guide)", error_kw=err_kw_ex3, **ex3_style)

    add_value_labels(ax, bars1, stds_ex1_acc, fmt="{:.0f}%")
    add_value_labels(ax, bars2, stds_ex3_acc, fmt="{:.0f}%")

    ax.set_ylabel("Accuracy (%)")
    ax.set_title("Per-Tier Accuracy (All 20)", fontsize=13, fontweight="bold")
    ax.set_xticks(x3)
    ax.set_xticklabels(tiers_all, fontsize=11)
    ax.set_ylim(0, 115)
    ax.axhline(y=50, color="gray", linestyle="--", alpha=0.4, linewidth=0.8)
    ax.legend(fontsize=10)

    # Ensure all spines visible
    for a in axes:
        for spine in a.spines.values():
            spine.set_visible(True)

    plt.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"\n📊 Figure saved to: {output_path}")
    plt.close(fig)


def print_multi_run_summary(label, agg, include_oos=True):
    """Print aggregated multi-run stats."""
    print(f"\n{'─'*50}")
    print(f"  {label}")
    print(f"{'─'*50}")
    m, s = agg["correct"]
    print(f"  Correct:       {m:.1f} ± {s:.1f}")
    m, s = agg["overestimate"]
    print(f"  Overestimate:  {m:.1f} ± {s:.1f}")
    m, s = agg["underestimate"]
    print(f"  Underestimate: {m:.1f} ± {s:.1f}")
    if include_oos:
        m, s = agg["oos_miss"]
        print(f"  OOS missed:    {m:.1f} ± {s:.1f}")
    m, s = agg["accuracy"]
    print(f"  Accuracy:      {m*100:.1f}% ± {s*100:.1f}%")

    print(f"\n  Per-tier accuracy:")
    for tier in ["L1", "L2", "L3"] + (["OOS"] if include_oos else []):
        m, s = agg.get(f"tier_acc_{tier}", (0, 0))
        print(f"    {tier}: {m:.1f}% ± {s:.1f}%")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Compare ex1 vs ex3 tier assignment (multi-run with error bars)"
    )
    parser.add_argument(
        "-m", "--model-dir", type=str, default=None,
        help="Path to model output directory containing result_data.csv "
             "(default: current directory)",
    )
    args = parser.parse_args()

    if args.model_dir:
        model_dir = Path(args.model_dir).resolve()
    else:
        model_dir = Path.cwd()

    csv_path = model_dir / "result_data.csv"
    if not csv_path.exists():
        # Also try outputs/{model_dir} relative to script location
        script_dir = Path(__file__).parent.resolve()
        alt_path = script_dir / "outputs" / args.model_dir / "result_data.csv" if args.model_dir else None
        if alt_path and alt_path.exists():
            csv_path = alt_path
            model_dir = alt_path.parent
        else:
            print(f"❌ result_data.csv not found at {csv_path}")
            sys.exit(1)

    rows = load_csv(csv_path)
    ex1_cols, ex3_cols = detect_run_columns(rows[0].keys())

    if not ex1_cols or not ex3_cols:
        print("❌ CSV must contain ex1_run* and ex3_run* columns.")
        print(f"   Found: ex1={ex1_cols}, ex3={ex3_cols}")
        sys.exit(1)

    model_name = model_dir.name
    print("=" * 50)
    print(f"  Model: {model_name}")
    print(f"  CSV:   {csv_path}")
    print(f"  Ex1 runs: {ex1_cols}")
    print(f"  Ex3 runs: {ex3_cols}")
    print("=" * 50)

    # Multi-run stats
    _, ex1_agg_all = compute_multi_run_stats(rows, ex1_cols, include_oos=True)
    _, ex3_agg_all = compute_multi_run_stats(rows, ex3_cols, include_oos=True)
    _, ex1_agg_15 = compute_multi_run_stats(rows, ex1_cols, include_oos=False)
    _, ex3_agg_15 = compute_multi_run_stats(rows, ex3_cols, include_oos=False)

    print("\n▶ Scenario A: All 20 Queries (including OOS)")
    print_multi_run_summary(f"Ex1 — Baseline ({len(ex1_cols)} runs)", ex1_agg_all)
    print_multi_run_summary(f"Ex3 — QDHC Guide ({len(ex3_cols)} runs)", ex3_agg_all)

    print(f"\n\n▶ Scenario B: First 15 Queries (L1/L2/L3 only)")
    print_multi_run_summary(f"Ex1 — Baseline ({len(ex1_cols)} runs)", ex1_agg_15, include_oos=False)
    print_multi_run_summary(f"Ex3 — QDHC Guide ({len(ex3_cols)} runs)", ex3_agg_15, include_oos=False)

    # Improvement
    delta_m = ex3_agg_all["accuracy"][0] - ex1_agg_all["accuracy"][0]
    delta_15_m = ex3_agg_15["accuracy"][0] - ex1_agg_15["accuracy"][0]
    print(f"\n{'='*50}")
    print(f"  Mean Accuracy Improvement (Ex3 − Ex1):")
    print(f"    All 20:  {delta_m*100:+.1f}%  "
          f"({ex1_agg_all['accuracy'][0]*100:.1f}% → {ex3_agg_all['accuracy'][0]*100:.1f}%)")
    print(f"    First 15: {delta_15_m*100:+.1f}%  "
          f"({ex1_agg_15['accuracy'][0]*100:.1f}% → {ex3_agg_15['accuracy'][0]*100:.1f}%)")
    print(f"{'='*50}")

    # Generate figure
    output_path = model_dir / "comparison_ex1_vs_ex3.png"
    plot_comparison(rows, ex1_cols, ex3_cols, model_name, output_path)


if __name__ == "__main__":
    main()

