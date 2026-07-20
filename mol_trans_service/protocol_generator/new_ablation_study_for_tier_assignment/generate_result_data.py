#!/usr/bin/env python3
"""
Generate result_data.csv from tier assignment ablation study outputs.

Scans the target directory for ex* subdirectories, collects predicted tier
labels from all runs, and writes a consolidated CSV.

Usage:
    # Run from within outputs/{model}/
    cd outputs/llama-3.1-70b/
    python ../../generate_result_data.py

    # Or specify the model directory explicitly
    python generate_result_data.py outputs/llama-3.1-70b

    # Or scan all models at once
    python generate_result_data.py --all
"""
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional


def find_result_files(model_dir: Path) -> Dict[str, Dict[int, Path]]:
    """Scan model_dir for ex*/run_*/batch_test_*.json (excluding _reports.json).

    Returns:
        {condition: {run_id: path}} e.g. {"ex1": {1: Path(...), 2: Path(...)}}
    """
    result_files: Dict[str, Dict[int, Path]] = {}

    for ex_dir in sorted(model_dir.iterdir()):
        if not ex_dir.is_dir() or not ex_dir.name.startswith("ex"):
            continue
        condition = ex_dir.name

        for run_dir in sorted(ex_dir.iterdir()):
            if not run_dir.is_dir() or not run_dir.name.startswith("run_"):
                continue

            try:
                run_id = int(run_dir.name.split("_")[1])
            except (IndexError, ValueError):
                continue

            # Find the results JSON (not _reports.json)
            json_files = [
                f for f in sorted(run_dir.glob("batch_test_*.json"))
                if "_reports" not in f.stem
            ]
            if json_files:
                # Use the latest file if multiple exist
                result_file = json_files[-1]
                result_files.setdefault(condition, {})[run_id] = result_file

    return result_files


def load_results(result_path: Path) -> List[Dict]:
    """Load results from a batch test JSON file."""
    with open(result_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("results", [])


def generate_csv(model_dir: Path, output_path: Optional[Path] = None) -> Path:
    """Generate result_data.csv for a single model directory.

    CSV format:
        name, expert_tier, ex1_run1, ex1_run2, ..., ex2_run1, ..., ex3_run1, ...

    Args:
        model_dir: Path to outputs/{model}/
        output_path: Where to save CSV. Defaults to model_dir/result_data.csv

    Returns:
        Path to generated CSV.
    """
    if output_path is None:
        output_path = model_dir / "result_data.csv"

    # Discover all result files
    result_files = find_result_files(model_dir)

    if not result_files:
        print(f"⚠️  No result files found in {model_dir}")
        return output_path

    # Build column order: sorted by condition, then run_id
    columns: List[str] = []
    column_data: Dict[str, Dict[str, str]] = {}  # {col_name: {query_name: tier}}

    for condition in sorted(result_files.keys()):
        for run_id in sorted(result_files[condition].keys()):
            col_name = f"{condition}_run{run_id}"
            columns.append(col_name)

            results = load_results(result_files[condition][run_id])
            col_map = {}
            for r in results:
                tier = r.get("predicted_tier", "")
                staged = r.get("staged_path")
                if tier == "STAGED" and staged:
                    tier = f"STAGED({staged})"
                col_map[r["name"]] = tier
            column_data[col_name] = col_map

    # Collect all query names and expert tiers (preserve original order)
    # Use the first result file to get the order
    first_condition = sorted(result_files.keys())[0]
    first_run = sorted(result_files[first_condition].keys())[0]
    first_results = load_results(result_files[first_condition][first_run])

    query_order = []
    expert_tiers = {}
    seen = set()
    for r in first_results:
        name = r["name"]
        if name not in seen:
            query_order.append(name)
            expert_tiers[name] = r.get("expert_tier", "")
            seen.add(name)

    # Also check other files for any missing queries
    for col_name, col_map in column_data.items():
        for name in col_map:
            if name not in seen:
                query_order.append(name)
                seen.add(name)

    # Write CSV
    header = ["name", "expert_tier"] + columns

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for name in query_order:
            row = [name, expert_tiers.get(name, "")]
            for col in columns:
                row.append(column_data.get(col, {}).get(name, ""))
            writer.writerow(row)

    # Print summary
    print(f"✅ CSV saved to: {output_path}")
    print(f"   Queries: {len(query_order)}")
    print(f"   Conditions × Runs: {len(columns)}")
    print(f"   Columns: {', '.join(columns)}")

    # Quick accuracy per column
    print(f"\n📊 Accuracy by condition × run:")
    for col in columns:
        col_map = column_data[col]
        total = 0
        correct = 0
        for name in query_order:
            expert = expert_tiers.get(name, "")
            predicted = col_map.get(name, "")
            if predicted and not predicted.startswith("Error"):
                total += 1
                if predicted == expert:
                    correct += 1
        if total > 0:
            print(f"   {col}: {correct}/{total} ({correct/total*100:.0f}%)")
        else:
            print(f"   {col}: no data")

    return output_path


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate result_data.csv from tier assignment outputs"
    )
    parser.add_argument(
        "model_dir", nargs="?", default=".",
        help="Path to model output directory (default: current directory)",
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Process all model directories under outputs/",
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help="Output CSV path (default: {model_dir}/result_data.csv)",
    )

    args = parser.parse_args()

    if args.all:
        # Find the outputs/ directory
        script_dir = Path(__file__).parent.resolve()
        outputs_dir = script_dir / "outputs"
        if not outputs_dir.exists():
            print(f"❌ outputs/ directory not found at {outputs_dir}")
            sys.exit(1)

        for model_dir in sorted(outputs_dir.iterdir()):
            if model_dir.is_dir():
                print(f"\n{'='*60}")
                print(f"  Processing: {model_dir.name}")
                print(f"{'='*60}")
                generate_csv(model_dir)
    else:
        model_dir = Path(args.model_dir).resolve()
        if not model_dir.exists():
            print(f"❌ Directory not found: {model_dir}")
            sys.exit(1)

        output_path = Path(args.output) if args.output else None
        generate_csv(model_dir, output_path)


if __name__ == "__main__":
    main()
