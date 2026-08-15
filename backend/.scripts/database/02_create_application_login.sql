:on error exit

USE [master];
GO

IF CAST(SERVERPROPERTY('IsIntegratedSecurityOnly') AS int) = 1
BEGIN
    THROW 51003, N'A instância aceita somente autenticação do Windows. Habilite o modo misto antes de criar um login SQL.', 1;
END;

DECLARE @senha nvarchar(128) = N'$(FLOWOPS_APPLICATION_PASSWORD)';

IF @senha = N'' OR @senha LIKE N'$(%'
BEGIN
    THROW 51000, N'Defina FLOWOPS_APPLICATION_PASSWORD antes de executar o script.', 1;
END;

IF SUSER_ID(N'flowops_app') IS NULL
BEGIN
    DECLARE @comando nvarchar(max) =
        N'CREATE LOGIN [flowops_app] WITH PASSWORD = '
        + QUOTENAME(@senha, '''')
        + N', CHECK_POLICY = ON, CHECK_EXPIRATION = OFF;';

    EXEC sys.sp_executesql @comando;
    PRINT N'Login flowops_app criado.';
END
ELSE
BEGIN
    PRINT N'O login flowops_app já existe; a senha não foi alterada.';
END;
GO

USE [DB_FLOWOPS];
GO

IF USER_ID(N'flowops_app') IS NULL
BEGIN
    CREATE USER [flowops_app] FOR LOGIN [flowops_app];
    PRINT N'Usuário flowops_app criado no DB_FLOWOPS.';
END
ELSE
BEGIN
    PRINT N'O usuário flowops_app já existe no DB_FLOWOPS.';
END;
GO
