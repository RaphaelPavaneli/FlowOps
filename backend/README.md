# FlowOps Backend

API da plataforma FlowOps construída com FastAPI, SQLAlchemy, Alembic e SQL
Server. Os nomes arquiteturais permanecem em inglês e os conceitos de negócio
são escritos em português brasileiro.

## Responsabilidades das camadas

- `api`: rotas HTTP, dependências e schemas de entrada e saída.
- `application`: casos de uso e contratos de serviços técnicos.
- `domain`: regras de negócio, entidades e contratos de repositórios.
- `infrastructure`: SQLAlchemy, repositórios e mecanismos de segurança.
- `core`: configurações compartilhadas pela aplicação.

## Pré-requisitos

- Python 3.11 ou superior.
- SQL Server 2022 ou superior. O ambiente original usa SQL Server 2025.
- Microsoft ODBC Driver 18 for SQL Server.
- `sqlcmd`, recomendado para executar o bootstrap automatizado.
- Banco local acessível pela conta Windows ou por um login SQL.

## Preparação do ambiente

No PowerShell, dentro da pasta `backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie a chave gerada para `FLOWOPS_JWT_SECRET_KEY` no `.env`.

## Variáveis do banco

Para autenticação integrada do Windows:

```env
FLOWOPS_DB_SERVER=localhost
FLOWOPS_DB_PORT=
FLOWOPS_DB_NAME=DB_FLOWOPS
FLOWOPS_DB_DRIVER=ODBC Driver 18 for SQL Server
FLOWOPS_DB_AUTH_MODE=windows
FLOWOPS_DB_USER=
FLOWOPS_DB_PASSWORD=
FLOWOPS_DB_ENCRYPT=true
FLOWOPS_DB_TRUST_SERVER_CERTIFICATE=true
```

Para um login SQL específico da aplicação:

```env
FLOWOPS_DB_AUTH_MODE=sql
FLOWOPS_DB_USER=flowops_app
FLOWOPS_DB_PASSWORD=defina-uma-senha-local-segura
```

O modo `sql` exige que a instância esteja com autenticação mista habilitada.
Nunca versione o arquivo `.env` ou senhas reais. Em produção, use certificado
confiável e `FLOWOPS_DB_TRUST_SERVER_CERTIFICATE=false`.

## Configuração automatizada do banco

Os scripts em `.scripts/database` preparam o banco. O Alembic é a única fonte
de verdade para schemas, tabelas e índices.

Com autenticação do Windows:

```powershell
.\.scripts\database\setup_database.ps1 -ApplicationAuthMode windows
```

Com login SQL `flowops_app`:

```powershell
.\.scripts\database\setup_database.ps1 -ApplicationAuthMode sql
```

No segundo modo, a senha é solicitada durante a execução e não é gravada. A
ordem automatizada é:

1. Criar `DB_FLOWOPS`, caso não exista.
2. Executar `python -m alembic upgrade head`.
3. Criar opcionalmente o login e o usuário `flowops_app`.
4. Conceder apenas `CONNECT`, `SELECT`, `INSERT`, `UPDATE` e `DELETE` em `auth`.
5. Validar o schema, a tabela, o índice e as permissões.

Para detalhes ou execução manual, consulte
[.scripts/database/README.md](.scripts/database/README.md).

## Execução da aplicação

Depois de configurar o banco:

```powershell
python -m uvicorn app.main:app --reload
```

Também é possível abrir `run.py` no VS Code e usar **Run Python File**.

- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api/v1/health`

## Autenticação

- `POST /api/v1/autenticacao/cadastro`: cria um usuário comum.
- `POST /api/v1/autenticacao/login`: devolve um access token JWT.
- `GET /api/v1/autenticacao/usuario-atual`: exige Bearer token válido.

As senhas são protegidas com Argon2id e nunca são armazenadas em texto puro.

## Gestão de usuários

As rotas abaixo exigem um JWT pertencente a um usuário com perfil
`administrador`:

- `GET /api/v1/usuarios`: lista usuários com `pagina` e `itens_por_pagina`.
- `PATCH /api/v1/usuarios/{id}/perfil`: altera o perfil de acesso.
- `PATCH /api/v1/usuarios/{id}/status`: ativa ou desativa um usuário.

Um administrador não pode remover o próprio perfil administrativo nem
desativar a própria conta. Alterações de perfil ou status entram em vigor na
requisição seguinte porque o usuário do token é consultado novamente no banco.

## Testes

```powershell
python -m pytest
```

Os testes comuns utilizam SQLite em memória e não alteram `DB_FLOWOPS`. A
conexão SQL Server e as migrations são validadas separadamente durante o
bootstrap do ambiente.
