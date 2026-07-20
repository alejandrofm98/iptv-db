"""SQLAlchemy engine factories. Supports both async and sync sessions."""

from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from iptv_db.exceptions import ConnectionError as DBConnectionError

DEFAULT_DIALECT = "postgresql+psycopg"
DEFAULT_DIALECT_ASYNC = "postgresql+psycopg"


def build_url(
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    *,
    async_driver: bool = False,
) -> str:
    """Build a SQLAlchemy URL from individual connection params."""
    driver = "postgresql+psycopg"
    return f"{driver}://{user}:{password}@{host}:{port}/{database}"


def get_sync_engine(url: str, **kwargs: Any) -> Any:
    """Create a synchronous SQLAlchemy engine."""
    try:
        return create_engine(url, pool_pre_ping=True, pool_recycle=300, **kwargs)
    except Exception as exc:
        raise DBConnectionError(f"Failed to create sync engine: {exc}") from exc


def get_async_engine(url: str, **kwargs: Any) -> Any:
    """Create an async SQLAlchemy engine."""
    try:
        return create_async_engine(url, pool_pre_ping=True, pool_recycle=300, **kwargs)
    except Exception as exc:
        raise DBConnectionError(f"Failed to create async engine: {exc}") from exc


def get_sync_session_factory(engine: Any) -> Any:
    """Return a sessionmaker for sync sessions."""
    return sessionmaker(bind=engine, autocommit=False, expire_on_commit=False)


def get_async_session_factory(engine: Any) -> Any:
    """Return an async sessionmaker."""
    return async_sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def session_scope(factory: Any) -> Iterator[Session]:
    """Context manager for sync sessions with automatic commit/rollback."""
    session: Session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@asynccontextmanager
async def async_session_scope(factory: Any) -> AsyncIterator[AsyncSession]:
    """Async context manager with automatic commit/rollback."""
    session: AsyncSession = factory()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
