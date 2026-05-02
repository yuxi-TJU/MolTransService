from __future__ import annotations

import os
from typing import Dict

from .llm_client import LLMClient, LLMProvider

MODEL_CATALOG: Dict[str, Dict[str, str]] = {
    "gemini-2.5-pro": {
        "provider": "openai",
        "model": "gemini-2.5-pro",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },
    "gemini-3-pro-preview": {
        "provider": "openai",
        "model": "gemini-3-pro-preview",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },

    "gpt-4o": {
        "provider": "openai",
        "model": "gpt-4o",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },
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
    "gpt-5.1": {
        "provider": "openai",
        "model": "gpt-5.1",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },
    "gpt-5.2": {
        "provider": "openai",
        "model": "gpt-5.2",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },
    "gpt-5.2-low": {
        "provider": "openai",
        "model": "gpt-5.2-low",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },    

    "grok-4": {
        "provider": "openai",
        "model": "grok-4",
        "api_key_env": "GROK_API_KEY",
        "api_url_env": "GROK_API_URL",
    },

    "qwen3-max": {
        "provider": "openai",
        "model": "qwen3-max",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },
    "qwen3-max-thinking": {
        "provider": "openai",
        "model": "qwen3-max-2026-01-23",
        "api_key_env": "QWEN_API_KEY_2",
        "api_url_env": "QWEN_API_URL",
        "extra_body": {"enable_thinking": True},
    },

    "deepseek-v3.2-think": {
        "provider": "openai",
        "model": "deepseek-v3.2-think",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },

    "qwen2.5-72b-instruct": {
        "provider": "openai",
        "model": "Qwen/Qwen2.5-72B-Instruct",
        "api_key_env": "LLM_API_KEY",
        "api_url_env": "LLM_API_URL",
    },
    "llama-3.1-70b": {
        "provider": "openai",
        "model": "llama-3.1-70b",
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
    extra_body = cfg.get("extra_body")
    return LLMClient(provider=provider, api_key=api_key, model=cfg["model"], api_url=api_url, extra_body=extra_body)
