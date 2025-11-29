from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from .llm_client import LLMClient
from .query_parser import ParsedQuery, QueryParser
from ..retrieval import QuerySystem, RetrievalEngine
from ..retrieval.retriever import RetrievalResult

LOCAL_TZ = timezone(timedelta(hours=8))


def convert_systems(parsed_systems) -> List[QuerySystem]:
    systems: List[QuerySystem] = []
    for entry in parsed_systems:
        systems.append(
            QuerySystem(
                name=entry.name,
                core_smiles=entry.core_smiles,
                anchor_groups=entry.anchor_groups,
                electrode_material=entry.electrode_material,
                electrode_surface=entry.electrode_surface,
                interface_geometry_text=entry.interface,
            )
        )
    return systems


def serialize_parsed_query(structured: ParsedQuery) -> Dict[str, Any]:
    return {
        "phenomenon": structured.phenomenon,
        "objectives": structured.objectives,
        "systems": [
            {
                "name": system.name,
                "core_smiles": system.core_smiles,
                "anchor_groups": system.anchor_groups,
                "electrode_material": system.electrode_material,
                "electrode_surface": system.electrode_surface,
                "interface": system.interface,
            }
            for system in structured.systems
        ],
        "raw_response": structured.raw_response,
    }


def serialize_results(results: List[RetrievalResult]) -> List[Dict[str, Any]]:
    payload: List[Dict[str, Any]] = []
    for result in results:
        entry: Dict[str, Any] = {
            "report_id": result.report_id,
            "path": str(result.path),
            "aggregate_score": result.aggregate_score,
            "phenomenon_score": result.phenomenon_score,
            "objective_score": result.objective_score,
            "system_score": result.system_score,
        }
        if result.system_details:
            entry["system_details"] = {
                "system_name": result.system_details.system_name,
                "score": result.system_details.score,
                "component_scores": result.system_details.component_scores,
                "source_path": str(result.system_details.source_path),
            }
        payload.append(entry)
    return payload


def load_generation_materials(manual_dir: Path) -> Dict[str, Any]:
    manual_prompt_path = manual_dir / "gen_report_prompt.md"
    qdhc_path = manual_dir / "QDHC_Guide.md"
    mst_path = manual_dir / "MST_Manual.md"
    return {
        "system_prompt": manual_prompt_path.read_text(encoding="utf-8"),
        "manual_prompt_path": manual_prompt_path,
        "qdhc_text": qdhc_path.read_text(encoding="utf-8"),
        "qdhc_path": qdhc_path,
        "mst_text": mst_path.read_text(encoding="utf-8"),
        "mst_path": mst_path,
    }


def collect_example_reports(results: List[RetrievalResult], max_reports: int = 3) -> List[Dict[str, Any]]:
    examples: List[Dict[str, Any]] = []
    for result in results[:max_reports]:
        path = Path(result.path)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        preview = text[:800]
        if len(text) > 800:
            preview += "..."
        examples.append(
            {
                "report_id": result.report_id,
                "path": path,
                "text": text,
                "preview": preview,
                "scores": {
                    "aggregate": result.aggregate_score,
                    "phenomenon": result.phenomenon_score,
                    "objective": result.objective_score,
                    "system": result.system_score,
                },
            }
        )
    return examples


def build_generation_user_prompt(
    *,
    query: str,
    qdhc_text: str,
    mst_text: str,
    examples: List[Dict[str, Any]],
) -> str:
    sections = [
        f"User Query:\n{query.strip()}",
        f"QDHC Guide:\n{qdhc_text.strip()}",
        f"MST Manual:\n{mst_text.strip()}",
    ]
    for idx, example in enumerate(examples, start=1):
        sections.append(f"Example Report {idx} ({example['path'].name}):\n{example['text'].strip()}")
    return "\n\n---\n\n".join(sections)


def generate_report_document(
    *,
    client: LLMClient,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.1,
) -> str:
    response = client.complete(
        user_prompt,
        system_prompt=system_prompt,
        temperature=temperature,
    )
    return response.strip()


def save_generation_outputs(
    *,
    prefix: str,
    timestamp: str,
    output_dir: Path,
    report_text: str,
    record_payload: Dict[str, Any],
) -> Dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"{prefix}_report_{timestamp}.md"
    record_path = output_dir / f"{prefix}_record_{timestamp}.json"
    report_path.write_text(report_text, encoding="utf-8")
    with record_path.open("w", encoding="utf-8") as fh:
        json.dump(record_payload, fh, ensure_ascii=False, indent=2)
    return {"report_path": report_path, "record_path": record_path}


@dataclass
class ParseRetrieveData:
    query: str
    structured: ParsedQuery
    systems: List[QuerySystem]
    results: List[RetrievalResult]
    parsed_serialized: Dict[str, Any]
    results_serialized: List[Dict[str, Any]]
    examples: List[Dict[str, Any]]
    run_time: datetime
    run_metadata: Dict[str, Any]


@dataclass
class WorkflowData:
    query: str
    structured: ParsedQuery
    systems: List[QuerySystem]
    results: List[RetrievalResult]
    parsed_serialized: Dict[str, Any]
    results_serialized: List[Dict[str, Any]]
    examples: List[Dict[str, Any]]
    report_text: Optional[str]
    report_path: Optional[Path]
    record_path: Optional[Path]
    run_time: datetime
    run_metadata: Dict[str, Any]

    def to_response(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "parsed": self.parsed_serialized,
            "results": self.results_serialized,
            "examples": [
                {
                    "report_id": example["report_id"],
                    "path": str(example["path"]),
                    "preview": example["preview"],
                    "scores": example["scores"],
                }
                for example in self.examples
            ],
            "generation": {
                "report_markdown": self.report_text,
                "report_path": str(self.report_path) if self.report_path else None,
                "record_path": str(self.record_path) if self.record_path else None,
            },
            "timestamp": self.run_time.isoformat(),
            "metadata": self.run_metadata,
        }


def describe_flow():
    print("\nExecution flow:")
    print("  1. Environment variables loaded from .env (provider, model, API endpoint/key, directories).")
    print("  2. Parsing LLM extracts phenomenon/objective/system info from the query.")
    print("  3. Retrieval engine evaluates phenomenon/objective/system similarity and ranks reports.")
    print("  4. QDHC/MST manuals plus top reports feed the generation LLM via manual/gen_report_prompt.md.")
    print("  5. Generated Markdown report and consolidated JSON record are saved under the configured output directory.")


def run_parse_and_retrieve(
    *,
    query: str,
    parse_client: LLMClient,
    engine: RetrievalEngine,
    reports_dir: Path,
    top_k: int,
) -> ParseRetrieveData:
    run_time = datetime.now(LOCAL_TZ)
    parser = QueryParser(parse_client)
    structured = parser.parse(query)
    systems = convert_systems(structured.systems)
    results = engine.search(
        phenomenon_text=structured.phenomenon,
        objective_text=structured.objectives,
        systems=systems or None,
        top_k=top_k,
    )
    parsed_serialized = serialize_parsed_query(structured)
    results_serialized = serialize_results(results)
    examples = collect_example_reports(results, max_reports=3)
    run_metadata = {
        "timestamp": run_time.isoformat(),
        "query": query,
        "parse_model": {"provider": parse_client.provider.value, "model": parse_client.model},
        "reports_dir": str(reports_dir),
        "parsed": parsed_serialized,
        "retrieval_results": results_serialized,
        "top_k": top_k,
    }
    return ParseRetrieveData(
        query=query,
        structured=structured,
        systems=systems,
        results=results,
        parsed_serialized=parsed_serialized,
        results_serialized=results_serialized,
        examples=examples,
        run_time=run_time,
        run_metadata=run_metadata,
    )


def generate_report_from_context(
    *,
    parse_data: ParseRetrieveData,
    gen_client: LLMClient,
    output_dir: Path,
    output_prefix: str,
    manual_dir: Path,
    materials: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    mats = materials or load_generation_materials(manual_dir)
    examples = parse_data.examples
    if not examples and parse_data.results:
        examples = collect_example_reports(parse_data.results, max_reports=3)

    record_payload: Dict[str, Any] = {
        **parse_data.run_metadata,
        "generation_model": {"provider": gen_client.provider.value, "model": gen_client.model},
    }
    report_text: Optional[str] = None
    report_path: Optional[Path] = None
    record_path: Optional[Path] = None

    if examples:
        user_prompt = build_generation_user_prompt(
            query=parse_data.query,
            qdhc_text=mats["qdhc_text"],
            mst_text=mats["mst_text"],
            examples=examples,
        )
        report_text = generate_report_document(
            client=gen_client,
            system_prompt=mats["system_prompt"],
            user_prompt=user_prompt,
            temperature=0.1,
        )
        generation_time = datetime.now(LOCAL_TZ)
        record_payload["generation_timestamp"] = generation_time.isoformat()
        record_payload["reports_used"] = [
            {
                "report_id": example["report_id"],
                "path": str(example["path"]),
                "scores": example["scores"],
            }
            for example in examples
        ]
        record_payload["context_files"] = {
            "manual_prompt": str(mats["manual_prompt_path"]),
            "qdhc_guide": str(mats["qdhc_path"]),
            "mst_manual": str(mats["mst_path"]),
        }
        record_payload["generated_report_text"] = report_text

        timestamp = generation_time.strftime("%Y%m%d_%H%M%S")
        outputs = save_generation_outputs(
            prefix=output_prefix,
            timestamp=timestamp,
            output_dir=output_dir,
            report_text=report_text,
            record_payload=record_payload,
        )
        report_path = outputs["report_path"]
        record_path = outputs["record_path"]

    return {
        "report_text": report_text,
        "report_path": report_path,
        "record_path": record_path,
        "record_payload": record_payload,
    }


def run_full_workflow(
    *,
    query: str,
    parse_client: LLMClient,
    gen_client: LLMClient,
    engine: RetrievalEngine,
    reports_dir: Path,
    output_dir: Path,
    output_prefix: str,
    top_k: int,
    manual_dir: Path,
    materials: Optional[Dict[str, Any]] = None,
) -> WorkflowData:
    parse_data = run_parse_and_retrieve(
        query=query,
        parse_client=parse_client,
        engine=engine,
        reports_dir=reports_dir,
        top_k=top_k,
    )
    gen_output = generate_report_from_context(
        parse_data=parse_data,
        gen_client=gen_client,
        output_dir=output_dir,
        output_prefix=output_prefix,
        manual_dir=manual_dir,
        materials=materials,
    )
    return WorkflowData(
        query=parse_data.query,
        structured=parse_data.structured,
        systems=parse_data.systems,
        results=parse_data.results,
        parsed_serialized=parse_data.parsed_serialized,
        results_serialized=parse_data.results_serialized,
        examples=parse_data.examples,
        report_text=gen_output["report_text"],
        report_path=gen_output["report_path"],
        record_path=gen_output["record_path"],
        run_time=parse_data.run_time,
        run_metadata=gen_output["record_payload"],
    )
