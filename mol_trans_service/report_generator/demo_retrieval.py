from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional

from .retrieval import QuerySystem, RetrievalEngine


def build_query_system(args: argparse.Namespace) -> Optional[QuerySystem]:
    if not any(
        [
            args.core_smiles,
            args.anchor_groups,
            args.electrode_material,
            args.electrode_surface,
            args.interface_text,
        ]
    ):
        return None

    anchor_groups: List[str] = []
    if args.anchor_groups:
        anchor_groups = [item.strip() for item in args.anchor_groups.split(",") if item.strip()]

    return QuerySystem(
        name=args.system_name,
        core_smiles=args.core_smiles,
        anchor_groups=anchor_groups,
        electrode_material=args.electrode_material,
        electrode_surface=args.electrode_surface,
        interface_geometry_text=args.interface_text,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Demo CLI for the QDHC triple-retrieval engine."
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=Path("."),
        help="Directory containing report markdown files.",
    )
    parser.add_argument(
        "--phenomenon",
        type=str,
        default="",
        help="Phenomenon description text (mapped to literature summaries).",
    )
    parser.add_argument(
        "--objective",
        type=str,
        default="",
        help="Computation objective text (mapped to computational objectives).",
    )
    parser.add_argument(
        "--system-name",
        type=str,
        default="",
        help="Optional label for the query system.",
    )
    parser.add_argument(
        "--core-smiles",
        type=str,
        default="",
        help="Core molecule SMILES string for system similarity.",
    )
    parser.add_argument(
        "--anchor-groups",
        type=str,
        default="",
        help="Comma-separated anchor group keywords.",
    )
    parser.add_argument(
        "--electrode-material",
        type=str,
        default="",
        help="Electrode material keyword (e.g., Au, Ag).",
    )
    parser.add_argument(
        "--electrode-surface",
        type=str,
        default="",
        help="Electrode surface description keyword.",
    )
    parser.add_argument(
        "--interface-text",
        type=str,
        default="",
        help="Free-form interface geometry description.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of results to return.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    engine = RetrievalEngine.from_directory(args.reports_dir)
    query_system = build_query_system(args)
    systems = [query_system] if query_system else []

    results = engine.search(
        phenomenon_text=args.phenomenon or None,
        objective_text=args.objective or None,
        systems=systems or None,
        top_k=args.top_k,
    )

    if not results:
        print("No matching reports found for the provided query.")
        return

    for idx, result in enumerate(results, start=1):
        print(f"{idx}. {result.report_id} (score={result.aggregate_score:.3f})")
        print(f"   path: {result.path}")
        if args.phenomenon:
            print(f"   phenomenon_score={result.phenomenon_score:.3f}")
        if args.objective:
            print(f"   objective_score={result.objective_score:.3f}")
        if systems:
            print(f"   system_score={result.system_score:.3f}")
            if result.system_details:
                details = result.system_details
                print(
                    "   matched system: "
                    f"{details.system_name} (query={details.component_scores['matched_query']})"
                )
                print(
                    "   component scores: "
                    f"smiles={details.component_scores['smiles']:.3f}, "
                    f"anchors={details.component_scores['anchors']:.3f}, "
                    f"electrode={details.component_scores['electrode']:.3f}, "
                    f"interface={details.component_scores['interface']:.3f}"
                )
        print()


if __name__ == "__main__":
    main()
