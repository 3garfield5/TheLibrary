from __future__ import annotations

from dataclasses import dataclass

from thelibrary.domain.repositories.llm_repository import (
    LLMChatRequest,
    LLMChatResponse,
    LLMRepository,
)
from thelibrary.exceptions.domain_exceptions import InvalidLLMRequestError


@dataclass(frozen=True)
class ChatWithAssistantCommand:
    user_id: str
    message: str
    language: str = "ru"
    system_prompt: str | None = None


class ChatWithAssistant:
    def __init__(self, llm_repository: LLMRepository):
        self.llm_repository = llm_repository

    def execute(self, command: ChatWithAssistantCommand) -> LLMChatResponse:
        user_id = command.user_id.strip()
        message = command.message.strip()

        if not user_id:
            raise InvalidLLMRequestError("user_id is required")
        if not message:
            raise InvalidLLMRequestError("message is required")

        request = LLMChatRequest(
            user_id=user_id,
            message=message,
            language=command.language,
            system_prompt=command.system_prompt,
        )
        return self.llm_repository.chat(request)
