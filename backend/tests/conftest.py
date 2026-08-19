from collections.abc import Generator
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

TEST_JWT_SECRET = "chave-exclusiva-dos-testes-com-mais-de-32-caracteres"
os.environ.setdefault("DB_SERVER", "localhost")
os.environ.setdefault("DB_NAME", "DB_FLOWOPS_TEST")
os.environ.setdefault("DB_USER", "flowops_test")
os.environ.setdefault("DB_PASSWORD", "senha-exclusiva-dos-testes")
os.environ.setdefault("JWT_SECRET_KEY", TEST_JWT_SECRET)

from app.api.dependencies.autenticacao import get_token_service  # noqa: E402
from app.infrastructure.database.connection import Base, get_db_session  # noqa: E402
from app.infrastructure.security.jwt_token_service import (  # noqa: E402
    JwtTokenService,
)
from app.main import app  # noqa: E402


@pytest.fixture
def session_factory() -> Generator[sessionmaker[Session], None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    ).execution_options(schema_translate_map={"auth": None})
    TestSession = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )
    Base.metadata.create_all(engine)

    yield TestSession

    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client(
    session_factory: sessionmaker[Session],
) -> Generator[TestClient, None, None]:

    def override_db_session() -> Generator[Session, None, None]:
        with session_factory() as session:
            yield session

    def override_token_service() -> JwtTokenService:
        return JwtTokenService(
            secret_key=TEST_JWT_SECRET,
            algorithm="HS256",
            issuer="flowops-api-test",
            audience="flowops-web-test",
            expire_minutes=15,
        )

    app.dependency_overrides[get_db_session] = override_db_session
    app.dependency_overrides[get_token_service] = override_token_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
