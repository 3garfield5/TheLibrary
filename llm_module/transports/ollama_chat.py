from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ..exceptions import LLMProviderError


class OllamaChatTransport:
    def __init__(
        self,
        model: str,
        base_url: str | None = None,
        timeout_seconds: float = 60.0,
    ):
        self.model = model
        self.base_url = (base_url or os.getenv("OLLAMA_BASE_URL") or "http://localhost:11434").rstrip("/")
        self.timeout_seconds = timeout_seconds

    def __call__(self, system_prompt: str, user_prompt: str) -> str:
        body = json.dumps(
            {
                "model": self.model,
                "stream": False,
                "format": "json",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            }
        ).encode("utf-8")

        request = Request(
            f"{self.base_url}/api/chat",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            raise LLMProviderError(
                f"Ollama HTTP {exc.code}: {body or exc.reason}. "
                f"Check model '{self.model}' is pulled."
            ) from exc
        except URLError as exc:
            raise LLMProviderError(
                f"Cannot connect to Ollama at {self.base_url}. "
                "Set OLLAMA_BASE_URL correctly or start Ollama."
            ) from exc

        message = payload.get("message")
        if not isinstance(message, dict):
            raise LLMProviderError("Ollama response missing message")

        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise LLMProviderError("Ollama response missing message.content")

        return content
