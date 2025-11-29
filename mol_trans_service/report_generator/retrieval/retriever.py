from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

from sentence_transformers import SentenceTransformer

from .report_parser import ParsedReport, ReportParser
from .system_similarity import QuerySystem, SystemSimilarityIndex, SystemSimilarityResult
from .vector_search import EmbeddingIndex


@dataclass
class RetrievalResult:
    report_id: str
    path: Path
    aggregate_score: float
    phenomenon_score: float = 0.0
    objective_score: float = 0.0
    system_score: float = 0.0
    system_details: Optional[SystemSimilarityResult] = None


class RetrievalEngine:
    """Coordinates the three retrieval channels (phenomenon, objective, system)."""

    def __init__(
        self,
        reports: Sequence[ParsedReport],
        *,
        model_name: str = "sentence-transformers/all-MiniLM-L12-v2",
        weights: Optional[Dict[str, float]] = None,
        candidate_multiplier: int = 3,
    ) -> None:
        if not reports:
            raise ValueError("At least one report is required to build a retrieval engine.")
        self._reports = list(reports)
        self._report_lookup: Dict[str, ParsedReport] = {
            report.path.name: report for report in self._reports
        }
        self._model = SentenceTransformer(model_name)
        self._weights = weights or {"phenomenon": 1.0, "objective": 1.0, "system": 1.0}
        self._candidate_multiplier = max(1, candidate_multiplier)

        self._phenomenon_index = EmbeddingIndex(model=self._model)
        self._objective_index = EmbeddingIndex(model=self._model)
        self._build_text_indexes()

        system_records = []
        for report in self._reports:
            for system in report.systems:
                system_records.append((report.path.name, report.path, system))
        self._system_index = SystemSimilarityIndex(system_records, model=self._model)

    @classmethod
    def from_directory(
        cls,
        directory: Path,
        *,
        pattern: str = "*_report_*.md",
        model_name: str = "sentence-transformers/all-MiniLM-L12-v2",
        weights: Optional[Dict[str, float]] = None,
    ) -> "RetrievalEngine":
        parser = ReportParser()
        paths = sorted(directory.glob(pattern))
        reports = parser.parse_many(paths)
        return cls(reports, model_name=model_name, weights=weights)

    def _build_text_indexes(self) -> None:
        items_phenomenon = []
        items_objective = []
        for report in self._reports:
            identifier = report.path.name
            summary_text = report.literature_summary.strip()
            if summary_text:
                items_phenomenon.append((identifier, summary_text))
            objective_text = report.computational_objectives.strip()
            if objective_text:
                items_objective.append((identifier, objective_text))
        self._phenomenon_index.add_many(items_phenomenon)
        self._objective_index.add_many(items_objective)

    def search(
        self,
        *,
        phenomenon_text: Optional[str] = None,
        objective_text: Optional[str] = None,
        systems: Optional[Sequence[QuerySystem]] = None,
        top_k: int = 3,
    ) -> List[RetrievalResult]:
        candidate_ids: Dict[str, RetrievalResult] = {}
        weights = self._weights
        phenomenon_scores: Dict[str, float] = {}
        objective_scores: Dict[str, float] = {}
        system_scores: Dict[str, SystemSimilarityResult] = {}

        max_candidates = max(top_k * self._candidate_multiplier, top_k)

        if phenomenon_text:
            phenomenon_scores = dict(
                self._phenomenon_index.search(phenomenon_text, top_k=max_candidates)
            )
        if objective_text:
            objective_scores = dict(
                self._objective_index.search(objective_text, top_k=max_candidates)
            )
        if systems:
            system_results = self._system_index.search(systems, top_k=max_candidates)
            system_scores = {result.report_id: result for result in system_results}

        if not (phenomenon_scores or objective_scores or system_scores):
            return []

        candidate_keys = (
            set(phenomenon_scores)
            | set(objective_scores)
            | set(system_scores)
        )

        results: List[RetrievalResult] = []
        for report_id in candidate_keys:
            report = self._report_lookup.get(report_id)
            if report is None:
                continue

            p_score = phenomenon_scores.get(report_id, 0.0)
            o_score = objective_scores.get(report_id, 0.0)
            sys_result = system_scores.get(report_id)
            s_score = sys_result.score if sys_result else 0.0

            total_weight = 0.0
            aggregate = 0.0
            if phenomenon_text and weights.get("phenomenon"):
                total_weight += weights["phenomenon"]
                aggregate += weights["phenomenon"] * p_score
            if objective_text and weights.get("objective"):
                total_weight += weights["objective"]
                aggregate += weights["objective"] * o_score
            if systems and weights.get("system"):
                total_weight += weights["system"]
                aggregate += weights["system"] * s_score
            if total_weight == 0.0:
                continue
            aggregate /= total_weight

            results.append(
                RetrievalResult(
                    report_id=report_id,
                    path=report.path,
                    aggregate_score=aggregate,
                    phenomenon_score=p_score,
                    objective_score=o_score,
                    system_score=s_score,
                    system_details=sys_result,
                )
            )

        results.sort(key=lambda item: item.aggregate_score, reverse=True)
        return results[:top_k]

    def get_report(self, report_id: str) -> Optional[ParsedReport]:
        return self._report_lookup.get(report_id)
