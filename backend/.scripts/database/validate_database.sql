:on error exit

USE [DB_FLOWOPS];
GO

SET NOCOUNT ON;

IF SCHEMA_ID(N'auth') IS NULL
BEGIN
    THROW 51010, N'O schema auth não foi encontrado.', 1;
END;

IF OBJECT_ID(N'auth.usuarios', N'U') IS NULL
BEGIN
    THROW 51011, N'A tabela auth.usuarios não foi encontrada.', 1;
END;

IF OBJECT_ID(N'auth.equipes', N'U') IS NULL
BEGIN
    THROW 51014, N'A tabela auth.equipes não foi encontrada.', 1;
END;

IF COL_LENGTH(N'auth.usuarios', N'equipe_id') IS NULL
BEGIN
    THROW 51015, N'A coluna auth.usuarios.equipe_id não foi encontrada.', 1;
END;

IF SCHEMA_ID(N'operacao') IS NULL
BEGIN
    THROW 51016, N'O schema operacao não foi encontrado.', 1;
END;

IF OBJECT_ID(N'operacao.automacoes', N'U') IS NULL
BEGIN
    THROW 51017, N'A tabela operacao.automacoes não foi encontrada.', 1;
END;

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE object_id = OBJECT_ID(N'auth.usuarios')
        AND name = N'uq_auth_usuarios_email'
        AND is_unique = 1
)
BEGIN
    THROW 51012, N'O índice único uq_auth_usuarios_email não foi encontrado.', 1;
END;

IF OBJECT_ID(N'dbo.alembic_version', N'U') IS NULL
BEGIN
    THROW 51013, N'A tabela de controle do Alembic não foi encontrada.', 1;
END;

IF NOT EXISTS (
    SELECT 1
    FROM dbo.alembic_version
    WHERE version_num = N'20260825_01'
)
BEGIN
    THROW 51018, N'O banco não está na revisão Alembic 20260825_01.', 1;
END;

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE object_id = OBJECT_ID(N'operacao.automacoes')
        AND name = N'uq_operacao_automacoes_equipe_nome'
        AND is_unique = 1
)
BEGIN
    THROW 51019, N'O índice único de automações por equipe não foi encontrado.', 1;
END;

SELECT
    DB_NAME() AS banco,
    CAST(SERVERPROPERTY('ProductVersion') AS nvarchar(128)) AS versao_servidor,
    compatibility_level AS nivel_compatibilidade
FROM sys.databases
WHERE name = DB_NAME();

SELECT
    s.name AS schema_nome,
    t.name AS tabela_nome
FROM sys.tables AS t
INNER JOIN sys.schemas AS s ON s.schema_id = t.schema_id
WHERE s.name IN (N'auth', N'operacao')
ORDER BY s.name, t.name;

SELECT
    i.name AS indice_nome,
    i.is_unique
FROM sys.indexes AS i
WHERE i.object_id IN (
    OBJECT_ID(N'auth.usuarios'),
    OBJECT_ID(N'auth.equipes'),
    OBJECT_ID(N'operacao.automacoes')
)
    AND i.name IS NOT NULL
ORDER BY OBJECT_NAME(i.object_id), i.name;

SELECT version_num AS revisao_alembic
FROM dbo.alembic_version;

SELECT
    dp.name AS usuario_banco,
    permission_name,
    state_desc
FROM sys.database_permissions AS permissao
INNER JOIN sys.database_principals AS dp
    ON dp.principal_id = permissao.grantee_principal_id
WHERE dp.name = N'flowops_app'
ORDER BY permission_name;

SELECT
    membro.name AS usuario_banco,
    papel.name AS papel_banco
FROM sys.database_role_members AS associacao
INNER JOIN sys.database_principals AS papel
    ON papel.principal_id = associacao.role_principal_id
INNER JOIN sys.database_principals AS membro
    ON membro.principal_id = associacao.member_principal_id
WHERE membro.name = N'flowops_app'
ORDER BY papel.name;
GO
