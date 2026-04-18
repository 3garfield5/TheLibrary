from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def build_book_text(book: dict) -> str:
    title = str(book.get("title", "")).strip()
    author = str(book.get("author", "")).strip()
    genres_raw = book.get("genres", [])
    genres = " ".join(str(genre).strip() for genre in genres_raw if str(genre).strip())
    summary = str(book.get("summary", "")).strip()
    return f"{title}\n{author}\n{genres}\n{summary}".strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Build FAISS index from catalog book text.")
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path("infrastructure/llm/catalog_data/books_40.json"),
        help="Path to catalog JSON file.",
    )
    parser.add_argument(
        "--index-out",
        type=Path,
        default=Path("infrastructure/llm/catalog_data/books_40.faiss"),
        help="Output path for FAISS index.",
    )
    parser.add_argument(
        "--meta-out",
        type=Path,
        default=Path("infrastructure/llm/catalog_data/books_40.faiss.meta.json"),
        help="Output path for metadata that maps FAISS ids to book ids.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help="sentence-transformers model name.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=16,
        help="Encoding batch size.",
    )
    parser.add_argument(
        "--no-normalize",
        action="store_true",
        help="Disable normalize_embeddings=True for model.encode.",
    )
    args = parser.parse_args()

    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer

    raw = json.loads(args.catalog.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Catalog JSON must be a list")

    books = [item for item in raw if isinstance(item, dict)]
    if not books:
        raise ValueError("No valid book records found in catalog")

    texts = [build_book_text(book) for book in books]

    model = SentenceTransformer(args.model)
    vectors = model.encode(
        texts,
        batch_size=args.batch_size,
        show_progress_bar=True,
        normalize_embeddings=not args.no_normalize,
    )

    matrix = np.array(vectors, dtype="float32")
    if args.no_normalize:
        faiss.normalize_L2(matrix)

    dimension = int(matrix.shape[1])
    index = faiss.IndexFlatIP(dimension)
    index.add(matrix)
    faiss.write_index(index, str(args.index_out))

    meta = {
        "dimension": dimension,
        "size": len(books),
        "book_ids": [str(book.get("id", "")) for book in books],
        "catalog_path": str(args.catalog),
        "embedding_model": args.model,
    }
    args.meta_out.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Built FAISS index ({dimension}d, {len(books)} vectors) -> {args.index_out}")
    print(f"Saved metadata -> {args.meta_out}")


if __name__ == "__main__":
    main()
