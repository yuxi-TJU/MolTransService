from __future__ import annotations

import ast
import dataclasses
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional


SECTION_PATTERN = re.compile(r"^#\s*(\d+)(?:\\\.)?\s+(.*)$", re.MULTILINE)
SYSTEM_PATTERN = re.compile(r"^##\s*System\s*\d+\s*:\s*(.+)$", re.MULTILINE)


@dataclass(slots=True)
class ParsedSystem:
    """Structured representation of a single system block within a report."""

    name: str
    raw_text: str
    core_smiles: Optional[str] = None
    anchor_groups: List[str] = field(default_factory=list)
    electrode_material: Optional[str] = None
    electrode_surface: Optional[str] = None
    interface_geometry_text: Optional[str] = None
    variation_notes: Optional[str] = None
    charge: Optional[str] = None
    other_fields: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ParsedReport:
    """Container describing a parsed report and its sections."""

    path: Path
    sections: Dict[str, str]
    systems: List[ParsedSystem]

    @property
    def metadata(self) -> str:
        return self.sections.get("0", "")

    @property
    def literature_summary(self) -> str:
        return self.sections.get("1", "")

    @property
    def computational_objectives(self) -> str:
        return self.sections.get("2", "")

    @property
    def involved_systems_text(self) -> str:
        return self.sections.get("3", "")


class ReportParser:
    """Parses markdown reports into structured objects used by the retriever."""

    def parse(self, path: Path) -> ParsedReport:
        text = path.read_text(encoding="utf-8")
        sections = self._split_sections(text)
        systems = self._parse_systems(sections.get("3", ""))
        return ParsedReport(path=path, sections=sections, systems=systems)

    def parse_many(self, paths: Iterable[Path]) -> List[ParsedReport]:
        return [self.parse(path) for path in paths]

    @staticmethod
    def _split_sections(text: str) -> Dict[str, str]:
        matches = list(SECTION_PATTERN.finditer(text))
        if not matches:
            return {}

        sections: Dict[str, str] = {}
        for idx, match in enumerate(matches):
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            number = match.group(1).strip()
            content = text[start:end].strip()
            sections[number] = content
        return sections

    def _parse_systems(self, text: str) -> List[ParsedSystem]:
        systems: List[ParsedSystem] = []
        matches = list(SYSTEM_PATTERN.finditer(text))
        if not matches:
            return systems
        for idx, match in enumerate(matches):
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            system_text = text[start:end].strip()
            name = match.group(1).strip()
            systems.append(self._parse_single_system(name=name, block=system_text))
        return systems

    def _parse_single_system(self, name: str, block: str) -> ParsedSystem:
        fields = self._extract_key_values(block)
        system = ParsedSystem(
            name=name,
            raw_text=block,
            core_smiles=fields.get("core_smiles"),
            anchor_groups=self._parse_list(fields.get("anchor_groups")),
            electrode_material=fields.get("electrode_material"),
            electrode_surface=fields.get("electrode_surface"),
            interface_geometry_text=fields.get("interface_geometry_text"),
            variation_notes=fields.get("variation_notes"),
            charge=fields.get("charge"),
            other_fields={
                key: value
                for key, value in fields.items()
                if key
                not in {
                    "core_smiles",
                    "anchor_groups",
                    "electrode_material",
                    "electrode_surface",
                    "interface_geometry_text",
                    "variation_notes",
                    "charge",
                }
            },
        )
        return system

    @staticmethod
    def _extract_key_values(block: str) -> Dict[str, str]:
        fields: Dict[str, str] = {}
        for raw_line in block.splitlines():
            line = raw_line.strip()
            if not line or ":" not in line:
                continue

            key_part, value_part = line.split(":", 1)
            key = key_part.strip(" -*\t").lower().replace(" ", "_").replace("\\_", "_")
            value = value_part.strip()
            if not value:
                continue
            # Normalize quotes
            if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
                value = value[1:-1]
            fields[key] = value
        return fields

    @staticmethod
    def _parse_list(value: Optional[str]) -> List[str]:
        if value is None:
            return []
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            try:
                parsed = ast.literal_eval(value)
            except (SyntaxError, ValueError):
                parsed = [item.strip() for item in value.strip("[]").split(",") if item.strip()]
            if isinstance(parsed, (list, tuple)):
                return [str(item) for item in parsed]
            return [str(parsed)]
        return [value] if value else []
