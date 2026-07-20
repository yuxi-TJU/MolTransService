#!/usr/bin/env python3
"""
Batch Testing Script for Workflow Assessment Ablation Study

Tests whether literature-derived examples improve workflow generation quality
(Sections 6-7) when the tier decision and MST Manual are already provided.

Conditions:
  cond_a: MST-only    — fixed Sections 1-5 + MST Manual + raw query
  cond_b: MST+Examples — fixed Sections 1-5 + MST Manual + top-k examples + raw query

Only runs the first 15 test cases (L1/L2/L3), skipping Out-of-scope queries.

Usage:
    python batch_test.py -c cond_a -m gemini-2.5-pro -r 1
    python batch_test.py -c cond_b -m llama-3.1-70b --top-k 5
    python batch_test.py -c cond_a --parallel 3
    python batch_test.py -c cond_b -r 1 --retry-failed
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
ABLATION_CONDITIONS = ["cond_a", "cond_b"]

# Only test L1/L2/L3 cases (first 15 queries)
MAX_CASE_INDEX = 15

# Prompt materials (loaded once at import time)
INSTRUCTION_PROMPT = (_CURRENT_DIR / "instruction_prompt_for_workflow.md").read_text(encoding="utf-8")
MST_MANUAL = (_CURRENT_DIR / "MST_Manual.md").read_text(encoding="utf-8")

# Paths
PROTOCOL_DIR = _CURRENT_DIR / "protocol"
TEST_QUERIES_PATH = _CURRENT_DIR / "test_queries.json"
REPORTS_DIR = _REPORT_GEN_DIR / "report_database"


# ── Helpers ───────────────────────────────────────────────────────

def load_test_queries(json_path: Path) -> List[Dict]:
    """Load test queries, keeping only the first MAX_CASE_INDEX (L1/L2/L3)."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["test_queries"][:MAX_CASE_INDEX]


def load_protocol(name: str) -> str:
    """Load the fixed Sections 1-5 protocol for a given test case."""
    protocol_path = PROTOCOL_DIR / f"{name}_protocol.md"
    if not protocol_path.exists():
        raise FileNotFoundError(f"Protocol not found: {protocol_path}")
    
    text = protocol_path.read_text(encoding="utf-8")
    
    # Strip out empty Sections 6-7 if present (we only want Sections 1-5)
    # Remove everything from "# 6." onwards
    match = re.search(r'\n# 6\.', text)
    if match:
        text = text[:match.start()].rstrip()
    
    return text


# Sections to keep from example reports
_KEEP_SECTIONS = {"0", "2", "3", "5", "6", "7"}


def filter_example_sections(report_text: str) -> str:
    """Extract only sections 0, 2, 3, 5, 6, 7 from an example report."""
    lines = report_text.split("\n")
    kept_lines: List[str] = []
    include = False

    for line in lines:
        # Check if this line is a section header like "# 0. Metadata"
        header_match = re.match(r'^# (\d+)\.', line)
        if header_match:
            section_num = header_match.group(1)
            include = section_num in _KEEP_SECTIONS

        if include:
            kept_lines.append(line)

    return "\n".join(kept_lines).strip()


# ── Prompt builders ───────────────────────────────────────────────

def build_user_prompt_cond_a(query: str, protocol_text: str) -> str:
    """Condition A (MST-only): raw query + fixed Sections 1-5 + MST Manual."""
    sections = [
        f"Original Research Query:\n{query.strip()}",
        f"Fixed Problem Specification (Sections 1-5):\n{protocol_text.strip()}",
        f"MST Manual:\n{MST_MANUAL.strip()}",
    ]
    return "\n\n---\n\n".join(sections)


def build_user_prompt_cond_b(query: str, protocol_text: str, examples: List[Dict]) -> str:
    """Condition B (MST + Examples): raw query + fixed Sections 1-5 + MST Manual + filtered examples."""
    sections = [
        f"Original Research Query:\n{query.strip()}",
        f"Fixed Problem Specification (Sections 1-5):\n{protocol_text.strip()}",
        f"MST Manual:\n{MST_MANUAL.strip()}",
    ]
    for idx, example in enumerate(examples, start=1):
        filtered_text = filter_example_sections(example["text"])
        sections.append(
            f"Example Report {idx} ({example['path'].name}):\n{filtered_text}"
        )
    return "\n\n---\n\n".join(sections)


# ── Retrieval engine (lazy singleton for cond_b) ──────────────────

_retrieval_engine: Optional[RetrievalEngine] = None


def get_retrieval_engine() -> RetrievalEngine:
    global _retrieval_engine
    if _retrieval_engine is None:
        print("🔍 Initializing retrieval engine...")
        _retrieval_engine = RetrievalEngine.from_directory(REPORTS_DIR)
    return _retrieval_engine


# ── Result file helpers ───────────────────────────────────────────

def find_latest_results_file(output_dir: Path, condition: str, model: str) -> Optional[Path]:
    """Find the latest results JSON (excluding _reports.json)."""
    pattern = f"batch_test_{condition}_{model}_*.json"
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
        status = r.get("status", "")
        if status.startswith("Error"):
            failed.append(r["name"])
    return failed


# ── Main batch test ───────────────────────────────────────────────

def run_batch_test(
    model: str = "gemini-2.5-pro",
    condition: str = "cond_a",
    run_id: int = 1,
    limit: int = None,
    start: int = 1,
    top_k: int = 3,
    retry_failed: bool = False,
    save_prompt: bool = False,
):
    """Run batch test for workflow assessment ablation study.

    Args:
        model: Model key from model registry.
        condition: Experiment condition (cond_a, cond_b).
        run_id: Run identifier for parallel execution.
        limit: Maximum number of queries to test.
        start: Starting query number (1-based).
        top_k: Number of examples to retrieve for cond_b.
        retry_failed: Only retry failed queries from previous run.
        save_prompt: Save full prompt and response to .md files.
    """
    # Setup output directory
    output_dir = _CURRENT_DIR / "outputs" / model / condition / f"run_{run_id}"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print(f"  Workflow Assessment: {condition} (Run {run_id})")
    print(f"  Output: {output_dir}")
    if condition == "cond_b":
        print(f"  Top-k examples: {top_k}")
    print("=" * 60)

    # Load test queries (first 15 only)
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

    print(f"📋 Testing {len(test_queries)} cases (L1/L2/L3 only)")

    # ── Initialize LLM clients ──
    gen_client = build_client_from_key(model)
    parse_client = build_client_from_key(model) if condition == "cond_b" else None
    print(f"🤖 Model: {gen_client.model}")
    print(f"🧪 Condition: {condition}")

    # Results storage
    results_dict = existing_results.copy()
    report_texts: Dict[str, str] = {}

    # ── Process each case ──
    for i, query_data in enumerate(test_queries, 1):
        name = query_data["name"]
        label = query_data["label"]
        query = query_data["query"]

        print(f"🔄 [{i}/{len(test_queries)}] {name} (tier: {label})...")

        try:
            # Load fixed protocol (Sections 1-5)
            protocol_text = load_protocol(name)

            # Build user prompt based on condition
            if condition == "cond_a":
                user_prompt = build_user_prompt_cond_a(query, protocol_text)

            else:  # cond_b
                # Parse query for triple retrieval
                parser = QueryParser(parse_client)
                structured = parser.parse(query)
                systems = convert_systems(structured.systems)

                # Triple retrieval → top-k examples
                engine = get_retrieval_engine()
                retrieval_results = engine.search(
                    phenomenon_text=structured.phenomenon,
                    objective_text=structured.objectives,
                    systems=systems or None,
                    top_k=top_k,
                )
                examples = collect_example_reports(retrieval_results, max_reports=top_k)
                user_prompt = build_user_prompt_cond_b(query, protocol_text, examples)

            # Call LLM
            report_text = gen_client.complete(
                user_prompt,
                system_prompt=INSTRUCTION_PROMPT,
                temperature=0.1,
            )

            # Save full prompt + response if enabled
            if save_prompt:
                prompt_dir = output_dir / "prompts"
                prompt_dir.mkdir(parents=True, exist_ok=True)
                prompt_file = prompt_dir / f"{name}_{condition}.md"
                with open(prompt_file, "w", encoding="utf-8") as pf:
                    pf.write(f"# {name} — {condition}\n\n")

                    # For cond_b, include the parse call details
                    if condition == "cond_b":
                        pf.write(f"## Step 1: Query Parsing (LLM Call #1)\n\n")
                        pf.write(f"### Parse Input\n\n{query}\n\n")
                        pf.write(f"### Parse Output (structured)\n\n")
                        pf.write(f"- Phenomenon: {structured.phenomenon}\n")
                        pf.write(f"- Objectives: {structured.objectives}\n")
                        pf.write(f"- Systems: {len(structured.systems)} system(s)\n")
                        if hasattr(structured, 'raw_response') and structured.raw_response:
                            pf.write(f"\n### Parse Raw LLM Response\n\n{structured.raw_response}\n\n")
                        pf.write(f"\n---\n\n")
                        pf.write(f"## Step 2: Workflow Generation (LLM Call #2)\n\n")
                    else:
                        pf.write(f"## Workflow Generation (LLM Call)\n\n")

                    pf.write(f"### System Prompt\n\n{INSTRUCTION_PROMPT}\n\n")
                    pf.write(f"---\n\n")
                    pf.write(f"### User Prompt\n\n{user_prompt}\n\n")
                    pf.write(f"---\n\n")
                    pf.write(f"### LLM Response\n\n{report_text}\n")
                print(f"   💾 Prompt saved: {prompt_file}")

            results_dict[name] = {
                "name": name,
                "tier": label,
                "condition": condition,
                "status": "OK",
            }
            report_texts[name] = report_text

            # Preview first line of output
            first_line = report_text.strip().split("\n")[0][:80]
            print(f"✅ [{i}/{len(test_queries)}] {name} — {first_line}")
            time.sleep(2)

        except Exception as e:
            print(f"❌ [{i}/{len(test_queries)}] {name} - Error: {str(e)}")
            results_dict[name] = {
                "name": name,
                "tier": label,
                "condition": condition,
                "status": f"Error: {str(e)}",
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
                "top_k": top_k if condition == "cond_b" else None,
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
    print(f"📊 Processed: {len(test_queries)} cases")
    print("=" * 60)

    successful = sum(1 for r in results if r["status"] == "OK")
    failed = len(results) - successful
    print(f"\n📈 Quick Stats:")
    print(f"   Successful: {successful}/{len(results)}")
    if failed > 0:
        print(f"   Failed: {failed}/{len(results)}")


# ── Parallel execution ────────────────────────────────────────────

def run_parallel(
    condition: str,
    model: str,
    num_runs: int,
    limit: int = None,
    start: int = 1,
    top_k: int = 3,
    retry_failed: bool = False,
    save_prompt: bool = False,
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
            "--top-k", str(top_k),
        ]
        if limit is not None:
            cmd.extend(["-n", str(limit)])
        if retry_failed:
            cmd.append("--retry-failed")
        if save_prompt:
            cmd.append("--save-prompt")
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
        description="Workflow assessment ablation study batch test"
    )
    parser.add_argument(
        "-c", "--condition", type=str, default="cond_a",
        choices=ABLATION_CONDITIONS,
        help="Experiment condition (default: cond_a)",
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
        help="Number of cases to test (default: all 15)",
    )
    parser.add_argument(
        "-s", "--start", type=int, default=1,
        help="Starting case number, 1-based (default: 1)",
    )
    parser.add_argument(
        "--top-k", type=int, default=3,
        help="Number of examples to retrieve for cond_b (default: 3)",
    )
    parser.add_argument(
        "--parallel", type=int, default=None,
        help="Launch N parallel runs (e.g., --parallel 3)",
    )
    parser.add_argument(
        "--retry-failed", action="store_true",
        help="Only retry failed queries from previous run",
    )
    parser.add_argument(
        "--save-prompt", action="store_true",
        help="Save full prompt and LLM response to .md files (default: off)",
    )

    args = parser.parse_args()

    if args.parallel:
        run_parallel(
            args.condition, args.model, args.parallel,
            args.limit, args.start, args.top_k, args.retry_failed,
            args.save_prompt,
        )
    else:
        run_batch_test(
            model=args.model,
            condition=args.condition,
            run_id=args.run_id,
            limit=args.limit,
            start=args.start,
            top_k=args.top_k,
            retry_failed=args.retry_failed,
            save_prompt=args.save_prompt,
        )
