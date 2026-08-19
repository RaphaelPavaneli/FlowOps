from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings
from app.core.settings import DatabaseSettings


class Base(DeclarativeBase):
    """Base declarativa dos modelos persistidos."""



def build_database_url(configuracao: DatabaseSettings) -> URL:
    """Constrói a URL SQL Server sem concatenar ou expor credenciais."""
    query = {
        "driver": configuracao.driver,
        "Encrypt": "yes" if configuracao.encrypt else "no",
        "TrustServerCertificate": (
            "yes" if configuracao.trust_server_certificate else "no"
        ),
    }

    return URL.create(
        drivername="mssql+pyodbc",
        username=configuracao.user,
        password=configuracao.password.get_secret_value(),
        host=configuracao.server,
        port=configuracao.port,
        database=configuracao.name,
        query=query,
    )

engine = create_engine(
    build_database_url(settings.db),
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db_session() -> Generator[Session, None, None]:
    """Fornece uma sessão de banco e garante seu fechamento."""
    with SessionLocal() as session:
        yield session
