# LLM Module

Минимальный модуль с двумя ручками:
- `POST /recommend`
- `POST /chat`

## `/recommend` (простая схема)
1. Из `likes` и `reviews` строится embedding пользователя (`sentence-transformers`).
2. Книги достаются из `catalog_data/books_40.json`.
3. Если включен FAISS (`USE_FAISS=true`) и есть индекс, кандидаты выбираются через FAISS.
4. Иначе кандидаты ранжируются обычным cosine similarity.
5. LLM выбирает финальные книги и формирует `reason`.

## Пример запроса
```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "u1",
    "limit": 5,
    "likes": [
      {"title": "Дюна", "author": "Фрэнк Герберт", "genres": ["фантастика"]}
    ],
    "reviews": [
      {"title": "Преступление и наказание", "author": "Федор Достоевский", "rating": 5, "comment": "нравится глубина"}
    ],
    "community_reviews": [
      {"title": "Гиперион", "author": "Дэн Симмонс", "rating": 4.7, "comment": "сильная фантастика"}
    ]
  }'
```

## FAISS индекс
FAISS не обязателен для запуска API. Если хочешь использовать индекс, установи отдельно:
```bash
pip install faiss-cpu
```

```bash
python3 llm_module/scripts/build_faiss_index.py \
  --catalog llm_module/catalog_data/books_40.json \
  --index-out llm_module/catalog_data/books_40.faiss \
  --meta-out llm_module/catalog_data/books_40.faiss.meta.json
```

Включение индекса в API:
```bash
export USE_FAISS=true
export FAISS_INDEX_PATH=llm_module/catalog_data/books_40.faiss
export FAISS_META_PATH=llm_module/catalog_data/books_40.faiss.meta.json
```
