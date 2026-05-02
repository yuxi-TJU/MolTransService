from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

from sentence_transformers import SentenceTransformer


@dataclass
class EmbeddingEntry:
    identifier: str
    text: str
    embedding: np.ndarray


class EmbeddingIndex:
    """Lightweight in-memory cosine-similarity index built on sentence-transformers."""

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L12-v2",
        *,
        model: SentenceTransformer | None = None,
        normalize: bool = True,
        batch_size: int = 32,
    ) -> None:
        self.model = model or SentenceTransformer(model_name)
        self.normalize = normalize
        self.batch_size = batch_size
        self._entries: List[EmbeddingEntry] = []

    def add(self, identifier: str, text: str) -> None:
        self.add_many([(identifier, text)])

    def add_many(self, items: Iterable[Tuple[str, str]]) -> None:
        items = list(items)
        if not items:
            return
        ids, texts = zip(*items)
        embeddings = self.model.encode(
            list(texts),
            batch_size=self.batch_size,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize,
            show_progress_bar=False,
        )
        for identifier, text, vector in zip(ids, texts, embeddings):
            self._entries.append(EmbeddingEntry(identifier=identifier, text=text, embedding=vector))

    @staticmethod
    def _normalize_similarity(score: float) -> float:
        normalized = (score + 1.0) / 2.0
        if normalized < 0.0:
            return 0.0
        if normalized > 1.0:
            return 1.0
        return normalized

    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        if not self._entries:
            return []
        query_vec = self.model.encode(
            [query],
            batch_size=1,
            convert_to_numpy=True,
            normalize_embeddings=self.normalize,
            show_progress_bar=False,
        )[0]
        scores = self._cosine_scores(query_vec)
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [
            (
                self._entries[idx].identifier,
                self._normalize_similarity(float(scores[idx])),
            )
            for idx in top_indices
        ]

    def _cosine_scores(self, query_vec: np.ndarray) -> np.ndarray:
        matrix = np.stack([entry.embedding for entry in self._entries])
        if self.normalize:
            return matrix @ query_vec
        norms = np.linalg.norm(matrix, axis=1) * np.linalg.norm(query_vec)
        norms[norms == 0.0] = 1.0
        return (matrix @ query_vec) / norms

    @property
    def entries(self) -> Sequence[EmbeddingEntry]:
        return tuple(self._entries)
