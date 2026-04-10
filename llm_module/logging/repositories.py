from __future__ import annotations

from ..contracts import LLMLogRecord


class InMemoryLLMLogRepository:
    def __init__(self) -> None:
        self._records: list[LLMLogRecord] = []

    def save(self, record: LLMLogRecord) -> None:
        self._records.append(record)

    def list_recent(self, limit: int = 100) -> list[LLMLogRecord]:
        return self._records[-max(limit, 0):][::-1]
