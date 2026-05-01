from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

import requests


class LLMProvider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"


@dataclass
class LLMClient:
    """Minimal HTTP client for calling OpenAI / Gemini style text endpoints."""

    provider: LLMProvider
    api_key: str
    model: str
    api_url: Optional[str] = None
    timeout: int = 3000
    extra_body: Optional[Dict[str, Any]] = None  # For model-specific parameters like enable_thinking

    def complete(self, prompt: str, *, system_prompt: Optional[str] = None, temperature: float = 0.0) -> str:
        if self.provider == LLMProvider.OPENAI:
            return self._call_openai(prompt, system_prompt=system_prompt, temperature=temperature)
        if self.provider == LLMProvider.GEMINI:
            return self._call_gemini(prompt, system_prompt=system_prompt, temperature=temperature)
        raise ValueError(f"Unsupported provider: {self.provider}")

    def _call_openai(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str],
        temperature: float,
    ) -> str:
        url = self.api_url or "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        # Add extra_body parameters directly to payload (for models like qwen3-max-thinking)
        if self.extra_body:
            payload.update(self.extra_body)
        
        # Debug: print payload for troubleshooting
        import os
        if os.getenv("DEBUG_LLM"):
            print(f"DEBUG payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
        
        # Debug: print response for troubleshooting
        if os.getenv("DEBUG_LLM") and not response.ok:
            print(f"DEBUG response status: {response.status_code}")
            print(f"DEBUG response body: {response.text}")
        
        response.raise_for_status()
        response.raise_for_status()
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError) as exc:
            raise RuntimeError(f"Unexpected OpenAI response: {json.dumps(data)}") from exc

    # def _call_gemini(
    #     self,
    #     prompt: str,
    #     *,
    #     system_prompt: Optional[str],
    #     temperature: float,
    # ) -> str:
    #     base_url = self.api_url or f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
    #     params = {"key": self.api_key}
    #     combined_prompt = prompt if not system_prompt else f"{system_prompt}\n\nUser Query:\n{prompt}"
    #     payload = {
    #         "contents": [
    #             {
    #                 "parts": [
    #                     {"text": combined_prompt},
    #                 ]
    #             }
    #         ],
    #         "generationConfig": {
    #             "temperature": temperature,
    #         },
    #     }
    #     response = requests.post(base_url, params=params, json=payload, timeout=self.timeout)
    #     response.raise_for_status()
    #     data = response.json()
    #     try:
    #         candidates = data["candidates"]
    #         text = candidates[0]["content"]["parts"][0]["text"]
    #         return text.strip()
    #     except (KeyError, IndexError) as exc:
    #         raise RuntimeError(f"Unexpected Gemini response: {json.dumps(data)}") from exc
