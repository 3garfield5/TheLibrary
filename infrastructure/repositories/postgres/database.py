from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def _database_url() -> str:
    host = os.getenv("DB_HOST", "postgres")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME", "thelibrary")
    user = os.getenv("DB_USER", "thelibrary")
    password = os.getenv("DB_PASSWORD", "thelibrary")
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"


engine = create_engine(_database_url(), future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True,
)


@contextmanager
def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_postgres_schema() -> None:
    from .models import Base

    Base.metadata.create_all(bind=engine)
