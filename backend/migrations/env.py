import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import URL, create_engine, pool

from app.core.config import settings
from app.infrastructure.database.connection import Base, build_database_url


config = context.config


def build_migration_database_url() -> URL:
    """Usa credenciais da aplicação ou conexão administrativa do bootstrap."""
    usar_conexao_windows = os.getenv(
        "FLOWOPS_MIGRATION_TRUSTED_CONNECTION",
        "false",
    ).casefold() == "true"

    if not usar_conexao_windows:
        return build_database_url(settings.db)

    return URL.create(
        drivername="mssql+pyodbc",
        host=settings.db.server,
        port=settings.db.port,
        database=settings.db.name,
        query={
            "driver": settings.db.driver,
            "Encrypt": "yes" if settings.db.encrypt else "no",
            "TrustServerCertificate": (
                "yes" if settings.db.trust_server_certificate else "no"
            ),
            "Trusted_Connection": "yes",
        },
    )


database_url = build_migration_database_url()

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
