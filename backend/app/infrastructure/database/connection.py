from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import Settings, settings


class Base(DeclarativeBase):
    """Base declarativa dos modelos persistidos."""



def build_database_url(configuracao: Settings) -> URL:
    """Constrói a URL SQL Server sem concatenar ou expor credenciais."""
    query = {
        "driver": configuracao.db_driver,
        "Encrypt": "yes" if configuracao.db_encrypt else "no",
        "TrustServerCertificate": (
            "yes" if configuracao.db_trust_server_certificate else "no"
        ),
    }

    usuario = None
    senha = None
    if configuracao.db_auth_mode == "windows":
        query["Trusted_Connection"] = "yes"
    else:
        usuario = configuracao.db_user
        senha = (
            configuracao.db_password.get_secret_value()
            if configuracao.db_password is not None
            else None
        )

    return URL.create(
        drivername="mssql+pyodbc",
        username=usuario,
        password=senha,
        host=configuracao.db_server,
        port=configuracao.db_port,
        database=configuracao.db_name,
        query=query,
    )

engine = create_engine(
    build_database_url(settings),
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
