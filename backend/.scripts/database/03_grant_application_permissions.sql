:on error exit

USE [DB_FLOWOPS];
GO

IF SCHEMA_ID(N'auth') IS NULL
BEGIN
    THROW 51001, N'O schema auth não existe. Execute a migration Alembic primeiro.', 1;
END;

IF SCHEMA_ID(N'operacao') IS NULL
BEGIN
    THROW 51004, N'O schema operacao não existe. Execute a migration Alembic primeiro.', 1;
END;

IF USER_ID(N'flowops_app') IS NULL
BEGIN
    THROW 51002, N'O usuário flowops_app não existe no DB_FLOWOPS.', 1;
END;

GRANT CONNECT TO [flowops_app];
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::[auth] TO [flowops_app];
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::[operacao] TO [flowops_app];

PRINT N'Permissões mínimas em auth e operacao concedidas ao usuário flowops_app.';
PRINT N'Papéis já existentes, como db_owner, não foram removidos por este script.';
GO
