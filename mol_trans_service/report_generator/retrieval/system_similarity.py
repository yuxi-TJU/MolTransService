from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
from sentence_transformers import SentenceTransformer

from .report_parser import ParsedSystem

# Morgan fingerprint generator (ECFP4, 2048 bits)
_MORGAN_GENERATOR = AllChem.GetMorganGenerator(radius=2, fpSize=2048)


@dataclass
class QuerySystem:
    """Minimal representation of a user-provided system description."""

    name: Optional[str] = None
    core_smiles: Optional[str] = None
    full_chemical_name: Optional[str] = None
    anchor_groups: Optional[Sequence[str]] = None
    electrode_material: Optional[str] = None
    electrode_surface: Optional[str] = None
    interface_geometry_text: Optional[str] = None


@dataclass
class SystemSimilarityResult:
    report_id: str
    system_name: str
    score: float
    component_scores: Dict[str, float]
    source_path: Path


@dataclass
class _SystemRecord:
    report_id: str
    report_path: Path
    system_name: str
    core_smiles: Optional[str]
    full_chemical_name: Optional[str]
    fingerprint: Optional[DataStructs.ExplicitBitVect]
    chemical_name_embedding: Optional[np.ndarray]
    anchor_set: Sequence[str]
    electrode_material: Optional[str]
    electrode_surface: Optional[str]
    interface_text: Optional[str]
    interface_embedding: Optional[np.ndarray]


class SystemSimilarityIndex:
    """Computes mixed chemical/textual similarity between query systems and report systems."""

    def __init__(
        self,
        systems: Iterable[Tuple[str, Path, ParsedSystem]],
        *,
        model: Optional[SentenceTransformer] = None,
        anchor_weight: float = 0.15,
        smiles_weight: float = 0.35,
        chemical_name_weight: float = 0.20,
        electrode_weight: float = 0.15,
        interface_weight: float = 0.15,
    ) -> None:
        self._model = model or SentenceTransformer("sentence-transformers/all-MiniLM-L12-v2")
        self._records: List[_SystemRecord] = []
        self._weights = {
            "smiles": smiles_weight,
            "chemical_name": chemical_name_weight,
            "anchors": anchor_weight,
            "electrode": electrode_weight,
            "interface": interface_weight,
        }
        for report_id, path, system in systems:
            record = _SystemRecord(
                report_id=report_id,
                report_path=path,
                system_name=system.name,
                core_smiles=system.core_smiles,
                full_chemical_name=system.full_chemical_name,
                fingerprint=self._fingerprint(system.core_smiles),
                chemical_name_embedding=self._embed_text(system.full_chemical_name),
                anchor_set=self._normalize_anchor_groups(system.anchor_groups),
                electrode_material=self._normalize_token(system.electrode_material),
                electrode_surface=self._normalize_token(system.electrode_surface),
                interface_text=system.interface_geometry_text,
                interface_embedding=self._embed_text(system.interface_geometry_text),
            )
            self._records.append(record)

    def _get_adjusted_weights(self, query: QuerySystem) -> Dict[str, float]:
        """Get adjusted weights based on query content.
        
        When SMILES is not provided, redistribute its weight to chemical_name
        to improve text-based chemical matching.
        """
        weights = self._weights.copy()
        has_smiles = query.core_smiles and self._fingerprint(query.core_smiles) is not None
        has_chemical_name = bool(query.full_chemical_name)
        
        if not has_smiles and has_chemical_name:
            # Transfer SMILES weight to chemical_name when SMILES is unavailable
            smiles_weight = weights.get("smiles", 0.0)
            weights["chemical_name"] = weights.get("chemical_name", 0.0) + smiles_weight
            weights["smiles"] = 0.0
        
        return weights

    def search(
        self,
        query_systems: Sequence[QuerySystem],
        *,
        top_k: int = 3,
    ) -> List[SystemSimilarityResult]:
        if not self._records or not query_systems:
            return []

        # Pre-compute embeddings for query interface descriptions and chemical names
        query_embeddings = [
            self._embed_text(system.interface_geometry_text) for system in query_systems
        ]
        query_chemical_name_embeddings = [
            self._embed_text(system.full_chemical_name) for system in query_systems
        ]
        query_anchors = [self._normalize_anchor_groups(system.anchor_groups or []) for system in query_systems]
        query_fingerprints = [self._fingerprint(system.core_smiles) for system in query_systems]
        query_materials = [self._normalize_token(system.electrode_material) for system in query_systems]
        query_surfaces = [self._normalize_token(system.electrode_surface) for system in query_systems]

        best_per_report: Dict[str, SystemSimilarityResult] = {}

        for record in self._records:
            best_score = -1.0
            best_components: Dict[str, float] = {}
            best_query_name: str = ""
            best_weights: Dict[str, float] = {}

            for idx, query in enumerate(query_systems):
                comp_scores = self._score_components(
                    query_fp=query_fingerprints[idx],
                    record_fp=record.fingerprint,
                    query_anchors=query_anchors[idx],
                    record_anchors=record.anchor_set,
                    query_material=query_materials[idx],
                    record_material=record.electrode_material,
                    query_surface=query_surfaces[idx],
                    record_surface=record.electrode_surface,
                    query_embed=query_embeddings[idx],
                    record_embed=record.interface_embedding,
                    query_chemical_name_embed=query_chemical_name_embeddings[idx],
                    record_chemical_name_embed=record.chemical_name_embedding,
                )
                # Use adjusted weights based on query content
                adjusted_weights = self._get_adjusted_weights(query)
                score = sum(comp_scores[key] * adjusted_weights[key] for key in adjusted_weights)
                if score > best_score:
                    best_score = score
                    best_components = comp_scores
                    best_query_name = query.name or f"QuerySystem[{idx}]"
                    best_weights = adjusted_weights

            if best_score < 0.0:
                continue

            existing = best_per_report.get(record.report_id)
            if existing is None or best_score > existing.score:
                best_per_report[record.report_id] = SystemSimilarityResult(
                    report_id=record.report_id,
                    system_name=record.system_name,
                    score=best_score,
                    component_scores=best_components | {"matched_query": best_query_name},
                    source_path=record.report_path,
                )

        results = sorted(best_per_report.values(), key=lambda r: r.score, reverse=True)
        return results[:top_k]

    def _embed_text(self, text: Optional[str]) -> Optional[np.ndarray]:
        if not text:
            return None
        vector = self._model.encode(
            [text],
            show_progress_bar=False,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )[0]
        return vector

    @staticmethod
    def _fingerprint(smiles: Optional[str]) -> Optional[DataStructs.ExplicitBitVect]:
        if not smiles:
            return None
        if smiles.strip().lower() in {"n/a", "na", "none", "null"}:
            return None
        molecule = Chem.MolFromSmiles(smiles)
        if molecule is None:
            return None
        return _MORGAN_GENERATOR.GetFingerprint(molecule)

    @staticmethod
    def _normalize_anchor_groups(groups: Sequence[str]) -> List[str]:
        return sorted({g.strip().lower() for g in groups if g})

    @staticmethod
    def _normalize_token(token: Optional[str]) -> Optional[str]:
        if not token or token.strip().lower() in {"n/a", "null", "none"}:
            return None
        return token.strip().lower()

    @staticmethod
    def _compute_embedding_similarity(
        query_embed: Optional[np.ndarray],
        record_embed: Optional[np.ndarray],
    ) -> float:
        """Compute normalized cosine similarity between two embeddings."""
        if query_embed is None or record_embed is None:
            return 0.0
        raw_score = float(np.dot(query_embed, record_embed))
        # Normalize from [-1, 1] to [0, 1]
        normalized = (raw_score + 1.0) / 2.0
        return max(0.0, min(1.0, normalized))

    @staticmethod
    def _score_components(
        *,
        query_fp: Optional[DataStructs.ExplicitBitVect],
        record_fp: Optional[DataStructs.ExplicitBitVect],
        query_anchors: Sequence[str],
        record_anchors: Sequence[str],
        query_material: Optional[str],
        record_material: Optional[str],
        query_surface: Optional[str],
        record_surface: Optional[str],
        query_embed: Optional[np.ndarray],
        record_embed: Optional[np.ndarray],
        query_chemical_name_embed: Optional[np.ndarray],
        record_chemical_name_embed: Optional[np.ndarray],
    ) -> Dict[str, float]:
        smiles_score = 0.0
        if query_fp is not None and record_fp is not None:
            smiles_score = float(DataStructs.TanimotoSimilarity(query_fp, record_fp))

        chemical_name_score = SystemSimilarityIndex._compute_embedding_similarity(
            query_chemical_name_embed, record_chemical_name_embed
        )

        anchor_score = 0.0
        if query_anchors and record_anchors:
            q_set, r_set = set(query_anchors), set(record_anchors)
            union = q_set | r_set
            anchor_score = len(q_set & r_set) / len(union) if union else 0.0

        electrode_score = 0.0
        if query_material and record_material:
            electrode_score = 1.0 if query_material == record_material else 0.0
        if query_surface and record_surface:
            surface_score = 1.0 if query_surface == record_surface else 0.0
            # Blend surface into electrode component
            electrode_score = (electrode_score + surface_score) / 2 if electrode_score else surface_score

        interface_score = SystemSimilarityIndex._compute_embedding_similarity(
            query_embed, record_embed
        )

        return {
            "smiles": smiles_score,
            "chemical_name": chemical_name_score,
            "anchors": anchor_score,
            "electrode": electrode_score,
            "interface": interface_score,
        }
