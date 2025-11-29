from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import List, Optional

from .llm_client import LLMClient
from .parse_prompt import QUERY_PARSER_SYSTEM_PROMPT, build_query_parsing_prompt


@dataclass
class ParsedQuerySystem:
    name: Optional[str]
    core_smiles: Optional[str]
    anchor_groups: List[str]
    electrode_material: Optional[str]
    electrode_surface: Optional[str]
    interface: Optional[str]


@dataclass
class ParsedQuery:
    phenomenon: Optional[str]
    objectives: Optional[str]
    systems: List[ParsedQuerySystem]
    raw_response: str = ""


class QueryParser:
    """Uses an LLM to convert a free-form query into structured retrieval inputs."""

    def __init__(
        self,
        client: LLMClient,
        *,
        system_prompt: str = QUERY_PARSER_SYSTEM_PROMPT,
        temperature: float = 0.0,
    ) -> None:
        self._client = client
        self._system_prompt = system_prompt
        self._temperature = temperature

    def parse(self, query: str) -> ParsedQuery:
        prompt = build_query_parsing_prompt(query)
        raw_response = self._client.complete(
            prompt,
            system_prompt=self._system_prompt,
            temperature=self._temperature,
        )
        payload = self._extract_json(raw_response)
        parsed = self._convert_payload(payload)
        parsed.raw_response = raw_response
        return parsed

    @staticmethod
    def _extract_json(text: str) -> dict:
        text = text.strip()
        if text.startswith("```"):
            # Remove optional fences
            text = re.sub(r"^```(?:json)?", "", text, count=1, flags=re.IGNORECASE).strip()
            if text.endswith("```"):
                text = text[:-3].strip()
        if text.startswith("{") and text.endswith("}"):
            return json.loads(text)
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError(f"Unable to extract JSON from LLM response: {text}")

    def _convert_payload(self, payload: dict) -> ParsedQuery:
        phenomenon = self._normalize_str(payload.get("phenomenon"))
        objectives = self._normalize_str(payload.get("objectives"))
        systems_payload = payload.get("systems") or []
        systems: List[ParsedQuerySystem] = []
        for entry in systems_payload:
            if not isinstance(entry, dict):
                continue
            systems.append(
                ParsedQuerySystem(
                    name=self._normalize_str(entry.get("name")),
                    core_smiles=self._normalize_str(entry.get("core_smiles")),
                    anchor_groups=self._normalize_list(entry.get("anchor_groups")),
                    electrode_material=self._normalize_str(entry.get("electrode_material")),
                    electrode_surface=self._normalize_str(entry.get("electrode_surface")),
                    interface=self._normalize_str(entry.get("interface")),
                )
            )
        return ParsedQuery(phenomenon=phenomenon, objectives=objectives, systems=systems)

    @staticmethod
    def _normalize_str(value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = str(value).strip()
        return value or None

    @staticmethod
    def _normalize_list(value) -> List[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        return []
