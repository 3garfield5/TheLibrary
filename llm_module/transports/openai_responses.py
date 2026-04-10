from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen

from ..exceptions import LLMProviderError


class OpenAIResponsesTransport:
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        timeout_seconds: float = 30.0,
        base_url: str = "https://api.openai.com/v1/responses",
    ):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.timeout_seconds = timeout_seconds
        self.base_url = base_url

        if not self.api_key:
            raise LLMProviderError("OPENAI_API_KEY is required")

    def __call__(self, system_prompt: str, user_prompt: str) -> str:
        body = json.dumps(
            {
                "model": self.model,
                "input": [
                    {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
                    {"role": "user", "content": [{"type": "input_text", "text": user_prompt}]},
                ],
                "text": {"format": {"type": "text"}},
            }
        ).encode("utf-8")

        request = Request(
            self.base_url,
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with urlopen(request, timeout=self.timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))

        output_text = payload.get("output_text")
        if not isinstance(output_text, str) or not output_text.strip():
            raise LLMProviderError("OpenAI response does not contain output_text")

        return output_text
