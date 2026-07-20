#!/usr/bin/env python3
"""
Batch Testing Script for Tier Assignment Ablation Study

Conditions:
  ex1: Baseline — tier definitions only (no guide, no examples)
  ex2: Tier definitions + retrieved example reports (no guide)
  ex3: Full QDHC Guide with decision rules (no examples)

Usage:
    # Single run
    python batch_test.py -c ex1 -r 1

    # 3 parallel runs
    python batch_test.py -c ex1 --parallel 3

    # Retry failed queries
    python batch_test.py -c ex1 -r 1 --retry-failed
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

# ── Path setup ────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_REPORT_GEN_DIR = _CURRENT_DIR.parent          # protocol_generator/
_MOL_TRANS_DIR = _REPORT_GEN_DIR.parent         # mol_trans_service/
_PROJECT_ROOT = _MOL_TRANS_DIR.parent

if str(_MOL_TRANS_DIR) not in sys.path:
    sys.path.insert(0, str(_MOL_TRANS_DIR))
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

# ── Environment variables ─────────────────────────────────────────
from dotenv import load_dotenv

local_env = _CURRENT_DIR / ".env"
if local_env.exists():
    load_dotenv(local_env)
ablation_env = _REPORT_GEN_DIR / "ablation_study" / ".env"
if ablation_env.exists():
    load_dotenv(ablation_env, override=False)
project_env = _PROJECT_ROOT / ".env_for_gen_report"
if project_env.exists():
    load_dotenv(project_env, override=False)

# ── Imports ───────────────────────────────────────────────────────
from mol_trans_service.protocol_generator.core.llm_client import LLMClient
from mol_trans_service.protocol_generator.core.model_registry import build_client_from_key
from mol_trans_service.protocol_generator.core.query_parser import QueryParser
from mol_trans_service.protocol_generator.core.workflow import (
    convert_systems,
    collect_example_reports,
)
from mol_trans_service.protocol_generator.retrieval import RetrievalEngine

# ── Constants ─────────────────────────────────────────────────────
ABLATION_CONDITIONS = ["ex1", "ex2", "ex3"]

# Prompt materials (loaded once at import time)
INSTRUCTION_EX1_2 = (_CURRENT_DIR / "instruction_prompt_for_ex1_2.md").read_text(encoding="utf-8")
INSTRUCTION_EX3 = (_CURRENT_DIR / "instruction_prompt_for_ex3.md").read_text(encoding="utf-8")
TIER_DEFINITION = (_CURRENT_DIR / "qdhc_tier_definition.md").read_text(encoding="utf-8")
QDHC_GUIDE = (_CURRENT_DIR / "QDHC_Guide.md").read_text(encoding="utf-8")

# Shared test queries (from old ablation study)
TEST_QUERIES_PATH = _REPORT_GEN_DIR / "ablation_study" / "test_queries.json"
REPORTS_DIR = _REPORT_GEN_DIR / "report_database"

# Expert label mapping: "Out" → "OOS"
LABEL_MAP = {"Out": "OOS", "L1": "L1", "L2": "L2", "L3": "L3"}


# ── Helpers ───────────────────────────────────────────────────────

def load_test_queries(json_path: Path) -> List[Dict]:
    """Load test queries from JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["test_queries"]


def extract_final_tier(report_text: str) -> str:
    """Extract tier label from <FINAL_TIER>...</FINAL_TIER> tag."""
    match = re.search(r"<FINAL_TIER>\s*(.*?)\s*</FINAL_TIER>", report_text, re.IGNORECASE)
    if match:
        return match.group(1).strip().upper()
    return "PARSE_ERROR"


def extract_staged_path(report_text: str) -> Optional[str]:
    """Extract staged path from <STAGED_PATH>...</STAGED_PATH> tag."""
    match = re.search(r"<STAGED_PATH>\s*(.*?)\s*</STAGED_PATH>", report_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None


# ── Prompt builders ───────────────────────────────────────────────

def build_user_prompt_ex1(query: str) -> str:
    """Ex1 (Baseline): tier definitions + raw query."""
    sections = [
        TIER_DEFINITION.strip(),
        f"Research Query:\n{query.strip()}",
    ]
    return "\n\n---\n\n".join(sections)


def build_user_prompt_ex2(query: str, examples: List[Dict]) -> str:
    """Ex2: tier definitions + raw query + retrieved example reports."""
    sections = [
        TIER_DEFINITION.strip(),
        f"Research Query:\n{query.strip()}",
    ]
    for idx, example in enumerate(examples, start=1):
        sections.append(
            f"Example Report {idx} ({example['path'].name}):\n{example['text'].strip()}"
        )
    return "\n\n---\n\n".join(sections)


def build_user_prompt_ex3(query: str) -> str:
    """Ex3: full QDHC guide + raw query."""
    sections = [
        QDHC_GUIDE.strip(),
        f"Research Query:\n{query.strip()}",
    ]
    return "\n\n---\n\n".join(sections)


# ── Retrieval engine (lazy singleton for Ex2) ─────────────────────

_retrieval_engine: Optional[RetrievalEngine] = None


def get_retrieval_engine() -> RetrievalEngine:
    global _retrieval_engine
    if _retrieval_engine is None:
        print("🔍 Initializing retrieval engine...")
        _retrieval_engine = RetrievalEngine.from_directory(REPORTS_DIR)
    return _retrieval_engine


# ── Result file helpers ───────────────────────────────────────────

def find_latest_results_file(output_dir: Path, condition: str, model: str) -> Optional[Path]:
    """Find the latest results JSON for a given condition and model."""
    pattern = f"batch_test_{condition}_{model}_*.json"
    # Exclude *_reports.json files
    files = sorted(
        [f for f in output_dir.glob(pattern) if "_reports" not in f.stem],
        reverse=True,
    )
    return files[0] if files else None


def load_failed_queries(results_path: Path) -> List[str]:
    """Load names of failed queries from a previous results file."""
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    failed = []
    for r in data.get("results", []):
        tier = r.get("predicted_tier", "")
        if tier.startswith("Error") or tier == "PARSE_ERROR":
            failed.append(r["name"])
    return failed


# ── Main batch test ───────────────────────────────────────────────

def run_batch_test(
    model: str = "gemini-2.5-pro",
    condition: str = "ex1",
    run_id: int = 1,
    limit: int = None,
    start: int = 1,
    retry_failed: bool = False,
):
    """Run batch test for tier assignment ablation study.

    Args:
        model: Model key from model registry.
        condition: Experiment condition (ex1, ex2, ex3).
        run_id: Run identifier for parallel execution.
        limit: Maximum number of queries to test.
        start: Starting query number (1-based).
        retry_failed: Only retry failed queries from previous run.
    """
    # Setup output directory
    output_dir = _CURRENT_DIR / "outputs" / model / condition / f"run_{run_id}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f"  Tier Assignment Ablation: {condition} (Run {run_id})")
    print(f"  Output: {output_dir}")
    print("=" * 60)

    # Load test queries
    if not TEST_QUERIES_PATH.exists():
        print(f"❌ Test queries not found: {TEST_QUERIES_PATH}")
        return

    all_queries = load_test_queries(TEST_QUERIES_PATH)
    all_queries_dict = {q["name"]: q for q in all_queries}

    # ── Handle retry-failed mode ──
    failed_names: List[str] = []
    existing_results: Dict[str, Dict] = {}
    original_results_file: Optional[Path] = None

    if retry_failed:
        results_file = find_latest_results_file(output_dir, condition, model)
        if results_file:
            original_results_file = results_file
            print(f"📂 Loading previous results: {results_file}")
            failed_names = load_failed_queries(results_file)
            with open(results_file, "r", encoding="utf-8") as f:
                prev_data = json.load(f)
                for r in prev_data.get("results", []):
                    if r["name"] not in failed_names:
                        existing_results[r["name"]] = r
            if failed_names:
                print(f"🔄 Retrying {len(failed_names)} failed queries: {failed_names}")
            else:
                print("✅ No failed queries to retry!")
                return
        else:
            print(f"⚠️  No previous results found for {condition}/{model}")
            return

    # ── Determine which queries to run ──
    if retry_failed:
        test_queries = [
            all_queries_dict[name]
            for name in failed_names
            if name in all_queries_dict
        ]
    else:
        start_idx = start - 1
        if limit is not None:
            test_queries = all_queries[start_idx : start_idx + limit]
        else:
            test_queries = all_queries[start_idx:]

    print(f"📋 Testing {len(test_queries)} queries")

    # ── Initialize LLM clients ──
    gen_client = build_client_from_key(model)
    # Ex2 needs a parse client for query parsing (triple retrieval)
    parse_client = build_client_from_key(model) if condition == "ex2" else None
    print(f"🤖 Model: {gen_client.model}")
    print(f"🧪 Condition: {condition}")

    # Select system prompt
    system_prompt = INSTRUCTION_EX3 if condition == "ex3" else INSTRUCTION_EX1_2

    # Results storage
    results_dict = existing_results.copy()
    report_texts: Dict[str, str] = {}

    # ── Process each query ──
    for i, query_data in enumerate(test_queries, 1):
        name = query_data["name"]
        label = LABEL_MAP.get(query_data["label"], query_data["label"])
        query = query_data["query"]

        if not query.strip():
            print(f"⚠️  [{i}/{len(test_queries)}] {name} - Skipping (empty)")
            results_dict[name] = {
                "name": name,
                "expert_tier": label,
                "predicted_tier": "EMPTY",
                "staged_path": None,
            }
            report_texts[name] = ""
            continue

        print(f"🔄 [{i}/{len(test_queries)}] {name} (expected: {label})...")

        try:
            # Build user prompt based on condition
            if condition == "ex1":
                user_prompt = build_user_prompt_ex1(query)

            elif condition == "ex2":
                # Parse query for triple retrieval
                parser = QueryParser(parse_client)
                structured = parser.parse(query)
                systems = convert_systems(structured.systems)

                # Triple retrieval → top-3 examples
                engine = get_retrieval_engine()
                retrieval_results = engine.search(
                    phenomenon_text=structured.phenomenon,
                    objective_text=structured.objectives,
                    systems=systems or None,
                    top_k=3,
                )
                examples = collect_example_reports(retrieval_results, max_reports=3)
                user_prompt = build_user_prompt_ex2(query, examples)

            else:  # ex3
                user_prompt = build_user_prompt_ex3(query)

            # Call LLM
            report_text = gen_client.complete(
                user_prompt,
                system_prompt=system_prompt,
                temperature=0.1,
            )

            # Extract tier label
            predicted_tier = extract_final_tier(report_text)
            staged_path = (
                extract_staged_path(report_text) if predicted_tier == "STAGED" else None
            )

            results_dict[name] = {
                "name": name,
                "expert_tier": label,
                "predicted_tier": predicted_tier,
                "staged_path": staged_path,
            }
            report_texts[name] = report_text

            tier_display = predicted_tier
            if staged_path:
                tier_display += f" ({staged_path})"
            print(f"✅ [{i}/{len(test_queries)}] {name} → {tier_display}")
            time.sleep(2)

        except Exception as e:
            print(f"❌ [{i}/{len(test_queries)}] {name} - Error: {str(e)}")
            results_dict[name] = {
                "name": name,
                "expert_tier": label,
                "predicted_tier": f"Error: {str(e)}",
                "staged_path": None,
            }
            report_texts[name] = ""

    # ── Convert to ordered list ──
    results = [
        results_dict[q["name"]] for q in all_queries if q["name"] in results_dict
    ]

    # ── Save results JSON ──
    if retry_failed and original_results_file:
        results_path = original_results_file
        print(f"📝 Updating: {results_path}")
    else:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_filename = f"batch_test_{condition}_{model}_{timestamp}.json"
        results_path = output_dir / results_filename

    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "test_condition": condition,
                "model": gen_client.model,
                "run_id": run_id,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_queries": len(results),
                "results": results,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    # ── Save full report texts separately ──
    reports_path = results_path.with_name(results_path.stem + "_reports.json")

    # When retrying, merge with existing report texts
    if retry_failed and reports_path.exists():
        with open(reports_path, "r", encoding="utf-8") as f:
            old_reports_data = json.load(f)
        for r in old_reports_data.get("results", []):
            if r["name"] not in report_texts:
                report_texts[r["name"]] = r.get("report_text", "")

    with open(reports_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "results": [
                    {"name": q["name"], "report_text": report_texts.get(q["name"], "")}
                    for q in all_queries
                    if q["name"] in report_texts
                ]
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    # ── Summary ──
    print("\n" + "=" * 60)
    print(f"✅ Batch test completed!")
    print(f"📁 Results: {results_path}")
    print(f"📁 Reports: {reports_path}")
    print(f"📊 Processed: {len(test_queries)} queries")
    print("=" * 60)

    successful = sum(1 for r in results if not r["predicted_tier"].startswith("Error"))
    correct = sum(1 for r in results if r["predicted_tier"] == r["expert_tier"])
    total = len(results)
    print(f"\n📈 Quick Stats:")
    print(f"   Successful: {successful}/{total}")
    print(f"   Correct:    {correct}/{total} ({correct / max(total, 1) * 100:.0f}%)")


# ── Parallel execution ────────────────────────────────────────────

def run_parallel(
    condition: str,
    model: str,
    num_runs: int,
    limit: int = None,
    start: int = 1,
    retry_failed: bool = False,
):
    """Launch multiple parallel batch test processes."""
    print("=" * 60)
    print(f"  Launching {num_runs} parallel runs for: {condition}")
    if retry_failed:
        print("  Mode: Retry failed queries")
    print("=" * 60)

    processes = []
    for run_id in range(1, num_runs + 1):
        cmd = [
            sys.executable,
            str(_CURRENT_DIR / "batch_test.py"),
            "-c", condition,
            "-m", model,
            "-r", str(run_id),
            "-s", str(start),
        ]
        if limit is not None:
            cmd.extend(["-n", str(limit)])
        if retry_failed:
            cmd.append("--retry-failed")
        print(f"🚀 Starting run_{run_id}: {' '.join(cmd)}")
        proc = subprocess.Popen(cmd)
        processes.append((run_id, proc))

    print(f"\n⏳ Waiting for {num_runs} processes...")

    for run_id, proc in processes:
        proc.wait()
        status = "✅" if proc.returncode == 0 else "❌"
        print(f"{status} Run {run_id} finished (code {proc.returncode})")

    print("\n" + "=" * 60)
    print("All parallel runs completed!")
    print("=" * 60)


# ── CLI ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    from mol_trans_service.protocol_generator.core.model_registry import available_models

    parser = argparse.ArgumentParser(
        description="Tier assignment ablation study batch test"
    )
    parser.add_argument(
        "-c", "--condition", type=str, default="ex1",
        choices=ABLATION_CONDITIONS,
        help="Experiment condition (default: ex1)",
    )
    parser.add_argument(
        "-m", "--model", type=str, default="gemini-2.5-pro",
        choices=available_models(),
        help="Model to use (default: gemini-2.5-pro)",
    )
    parser.add_argument(
        "-r", "--run-id", type=int, default=1,
        help="Run ID for output directory (default: 1)",
    )
    parser.add_argument(
        "-n", "--limit", type=int, default=None,
        help="Number of queries to test (default: all)",
    )
    parser.add_argument(
        "-s", "--start", type=int, default=1,
        help="Starting query number, 1-based (default: 1)",
    )
    parser.add_argument(
        "--parallel", type=int, default=None,
        help="Launch N parallel runs (e.g., --parallel 3)",
    )
    parser.add_argument(
        "--retry-failed", action="store_true",
        help="Only retry failed queries from previous run",
    )

    args = parser.parse_args()

    if args.parallel:
        run_parallel(
            args.condition, args.model, args.parallel,
            args.limit, args.start, args.retry_failed,
        )
    else:
        run_batch_test(
            model=args.model,
            condition=args.condition,
            run_id=args.run_id,
            limit=args.limit,
            start=args.start,
            retry_failed=args.retry_failed,
        )
