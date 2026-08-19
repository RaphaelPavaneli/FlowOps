# Scripts do banco de dados

Esta pasta prepara a infraestrutura do SQL Server. As tabelas e suas evoluções
são controladas exclusivamente pelas migrations Alembic.

## Ordem executada

1. `01_create_database.sql`: cria `DB_FLOWOPS` quando necessário.
2. `python -m alembic upgrade head`: cria `auth.usuarios` e registra a versão.
3. `02_create_application_login.sql`: cria `flowops_app`, caso não exista.
4. `03_grant_application_permissions.sql`: concede permissões mínimas em `auth`.
5. `validate_database.sql`: lista objetos e permissões para conferência.

O script `setup_database.ps1` automatiza essa ordem usando uma conexão
administrativa integrada do Windows.

## Execução

O bootstrap usa a conta Windows somente para as operações administrativas e
para executar as migrations. O backend permanece configurado exclusivamente
com o login SQL `flowops_app`.

```powershell
.\.scripts\database\setup_database.ps1
```

O SQL Server precisa estar em modo misto. O script pede a senha sem gravá-la no
repositório.

O login recebe somente `CONNECT`, `SELECT`, `INSERT`, `UPDATE` e `DELETE` no
schema `auth`. Ele não recebe `sysadmin`, `db_owner` ou permissão de DDL.
