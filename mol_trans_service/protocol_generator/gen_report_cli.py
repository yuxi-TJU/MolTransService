from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from .core import (
    available_models,
    build_client_from_key,
    describe_flow,
    load_generation_materials,
    run_full_workflow,
)
from .retrieval import RetrievalEngine

# Load environment variables first
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent
ENV_PATH = PROJECT_ROOT / ".env_for_gen_report"
load_dotenv(ENV_PATH)

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

MANUAL_DIR = BASE_DIR / "manual"


def _resolve_project_path(value: str | None, fallback: Path) -> Path:
    if value:
        path = Path(value).expanduser()
        if not path.is_absolute():
            return (PROJECT_ROOT / path).resolve()
        return path.resolve()
    return fallback

def parse_args() -> argparse.Namespace:
    model_choices = available_models()
    default_parse_model = os.getenv("PARSE_MODEL", model_choices[0])
    if default_parse_model not in model_choices:
        default_parse_model = model_choices[0]
    default_gen_model = os.getenv("GEN_MODEL", model_choices[0])
    if default_gen_model not in model_choices:
        default_gen_model = model_choices[0]
    default_reports_dir = os.getenv("REPORTS_DIR")
    default_output_prefix = os.getenv("OUTPUT_PREFIX", "test_id")
    default_output_dir = os.getenv("OUTPUT_DIR")

    resolved_reports_dir = _resolve_project_path(default_reports_dir, Path("."))
    resolved_output_dir = _resolve_project_path(default_output_dir, BASE_DIR / "generated_outputs")

    parser = argparse.ArgumentParser(
        description="End-to-end agent: parse query, retrieve reports, and generate a new report."
    )
    parser.add_argument("--query", type=str, required=True, help="User request to analyze.")
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=resolved_reports_dir,
        help="Directory containing *_report_*.md files.",
    )
    parser.add_argument(
        "--parse-model",
        type=str,
        choices=model_choices,
        default=default_parse_model,
        help="LLM model key for the parsing step.",
    )
    parser.add_argument(
        "--gen-model",
        type=str,
        choices=model_choices,
        default=default_gen_model,
        help="LLM model key for the report generation step.",
    )
    parser.add_argument(
        "--output-prefix",
        type=str,
        default=default_output_prefix,
        help="Prefix for generated report/record filenames.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=resolved_output_dir,
        help="Directory to store generated reports and records.",
    )
    parser.add_argument("--top-k", type=int, default=3, help="Number of reports to return.")
    return parser.parse_args()


def print_results(structured, systems, results):
    print("Parsed query:")
    print(f"  Phenomenon : {structured.phenomenon}")
    print(f"  Objectives : {structured.objectives}")
    if systems:
        for idx, system in enumerate(systems, start=1):
            print(
                f"  System {idx}: name={system.name}, smiles={system.core_smiles}, "
                f"anchors={system.anchor_groups}, electrode={system.electrode_material}"
            )
    else:
        print("  Systems    : []")
    print()

    if not results:
        print("No matching reports found.")
        return

    for idx, result in enumerate(results, start=1):
        print(f"{idx}. {result.report_id} (score={result.aggregate_score:.3f})")
        print(f"   path: {result.path}")
        if structured.phenomenon:
            print(f"   phenomenon_score={result.phenomenon_score:.3f}")
        if structured.objectives:
            print(f"   objective_score={result.objective_score:.3f}")
        if systems:
            print(f"   system_score={result.system_score:.3f}")
            if result.system_details:
                details = result.system_details
                components = details.component_scores
                print(
                    "   matched system: "
                    f"{details.system_name} (query={components['matched_query']})"
                )
                print(
                    "   component scores: "
                    f"smiles={components['smiles']:.3f}, "
                    f"anchors={components['anchors']:.3f}, "
                    f"electrode={components['electrode']:.3f}, "
                    f"interface={components['interface']:.3f}"
                )
        print()


def main() -> None:
    args = parse_args()

    parse_client = build_client_from_key(args.parse_model)
    gen_client = build_client_from_key(args.gen_model)

    engine = RetrievalEngine.from_directory(args.reports_dir)
    materials = load_generation_materials(MANUAL_DIR)

    workflow_data = run_full_workflow(
        query=args.query,
        parse_client=parse_client,
        gen_client=gen_client,
        engine=engine,
        reports_dir=args.reports_dir,
        output_dir=args.output_dir,
        output_prefix=args.output_prefix,
        top_k=args.top_k,
        manual_dir=MANUAL_DIR,
        materials=materials,
    )

    structured = workflow_data.structured
    systems = workflow_data.systems
    results = workflow_data.results

    print_results(structured, systems, results)

    if workflow_data.report_path:
        print(f"Generated report saved to: {workflow_data.report_path}")
    if workflow_data.record_path:
        print(f"Generation record saved to: {workflow_data.record_path}")

    describe_flow()


if __name__ == "__main__":
    main()
