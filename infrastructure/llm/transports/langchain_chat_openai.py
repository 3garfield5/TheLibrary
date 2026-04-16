from __future__ import annotations

import os
from typing import Any

from ..exceptions import LLMProviderError


class LangChainChatOpenAITransport:
    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout_seconds: float = 60.0,
        temperature: float = 0.0,
    ):
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
            from langchain_openai import ChatOpenAI
        except ModuleNotFoundError as exc:
            raise LLMProviderError(
                "langchain-openai is not installed. Install dependencies from requirements.txt"
            ) from exc

        resolved_api_key = api_key or os.getenv("OPENAI_API_KEY") or "EMPTY"
        resolved_base_url = (base_url or os.getenv("OPENAI_BASE_URL") or "").strip() or None

        self.model = model
        self._human_message = HumanMessage
        self._system_message = SystemMessage
        self._llm = ChatOpenAI(
            model=model,
            api_key=resolved_api_key,
            base_url=resolved_base_url,
            timeout=timeout_seconds,
            temperature=temperature,
        )

    def __call__(self, system_prompt: str, user_prompt: str, schema: type) -> Any:
        try:
            structured_llm = self._llm.with_structured_output(
                schema,
                method="json_mode",
                include_raw=False,
            )
            return structured_llm.invoke(
                [
                    self._system_message(content=system_prompt),
                    self._human_message(content=user_prompt),
                ]
            )
        except Exception as exc:
            raise LLMProviderError(f"ChatOpenAI structured call failed: {exc}") from exc

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self._llm.invoke(
                [
                    self._system_message(content=system_prompt),
                    self._human_message(content=user_prompt),
                ]
            )
        except Exception as exc:
            raise LLMProviderError(f"ChatOpenAI call failed: {exc}") from exc

        content = getattr(response, "content", None)
        if isinstance(content, str):
            text = content.strip()
            if text:
                return text
        if isinstance(content, list):
            chunks = [part.get("text", "") for part in content if isinstance(part, dict)]
            merged = " ".join(chunk.strip() for chunk in chunks if chunk.strip())
            if merged:
                return merged

        raise LLMProviderError("ChatOpenAI response is empty")
