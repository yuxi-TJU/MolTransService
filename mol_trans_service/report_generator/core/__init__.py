"""High-level helpers for LLM-powered query parsing."""

from .llm_client import LLMClient, LLMProvider
from .parse_prompt import build_query_parsing_prompt, QUERY_PARSER_SYSTEM_PROMPT
from .query_parser import ParsedQuery, ParsedQuerySystem, QueryParser
from .model_registry import MODEL_CATALOG, available_models, build_client_from_key
from .workflow import (
    convert_systems,
    describe_flow,
    load_generation_materials,
    run_parse_and_retrieve,
    generate_report_from_context,
    run_full_workflow,
)

__all__ = [
    "LLMClient",
    "LLMProvider",
    "build_query_parsing_prompt",
    "QUERY_PARSER_SYSTEM_PROMPT",
    "ParsedQuery",
    "ParsedQuerySystem",
    "QueryParser",
    "MODEL_CATALOG",
    "available_models",
    "build_client_from_key",
    "convert_systems",
    "describe_flow",
    "load_generation_materials",
    "run_parse_and_retrieve",
    "generate_report_from_context",
    "run_full_workflow",
]
