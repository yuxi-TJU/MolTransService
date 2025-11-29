from __future__ import annotations

import os
from typing import Dict

from .llm_client import LLMClient, LLMProvider

MODEL_CATALOG: Dict[str, Dict[str, str]] = {
    "gpt5-nano": {
        "provider": "openai",
        "model": "gpt-5-nano",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },
    "gpt5": {
        "provider": "openai",
        "model": "gpt-5",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },
    "gemini-2.5-pro": {
        "provider": "openai",
        "model": "gemini-2.5-pro",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },
}


def available_models():
    return list(MODEL_CATALOG.keys())


def build_client_from_key(model_key: str) -> LLMClient:
    if model_key not in MODEL_CATALOG:
        raise ValueError(f"Unsupported model key: {model_key}")
    cfg = MODEL_CATALOG[model_key]
    api_key_env = cfg.get("api_key_env", "LLM_API_KEY")
    api_url_env = cfg.get("api_url_env", "LLM_API_URL")
    api_key = os.getenv(api_key_env)
    if not api_key:
        raise ValueError(f"Missing API key for model '{model_key}'. Set {api_key_env}.")
    api_url = os.getenv(api_url_env)
    provider = LLMProvider(cfg["provider"])
    return LLMClient(provider=provider, api_key=api_key, model=cfg["model"], api_url=api_url)
