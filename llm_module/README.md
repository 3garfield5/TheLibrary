# LLM Module

Минимальный модуль для сценария: `Запросить рекомендацию у LLM на основе списка`.

## Что есть
- `RecommendationService`
- `ListBasedLLMProvider`
- `LangChainChatOpenAITransport` (`with_structured_output`)
- `OpenAIResponsesTransport`
- `OllamaChatTransport`
- `InMemoryLLMLogRepository`
- FastAPI: `POST /recommend`, `GET /health`

## Docker Compose
Запуск всего стека:
```bash
docker compose up --build
```

Переменные окружения:
- `LLM_MODEL` — имя модели
- `OPENAI_BASE_URL` — OpenAI-compatible endpoint (например, vLLM или Ollama `/v1`)
- `OPENAI_API_KEY` — ключ API (для локального vLLM/Ollama можно передать заглушку)

Swagger UI: `http://localhost:8000/docs`

## Проверка
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u1",
    "list_id": "l1",
    "limit": 3,
    "language": "ru",
    "seeds": [
      {"title": "1984", "author": "George Orwell", "genres": ["dystopia"]},
      {"title": "Brave New World", "author": "Aldous Huxley", "genres": ["dystopia"]}
    ]
  }'
```
