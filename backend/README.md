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
- SQL Server em modo de autenticação mista.
- Conta Windows com permissão administrativa para executar o bootstrap. O
  próprio script pode criar o login SQL `flowops_app`.

## Preparação do ambiente

No PowerShell, dentro da pasta `backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie a chave gerada para `JWT_SECRET_KEY` no `.env`.

## Variáveis do banco

O backend usa exclusivamente autenticação SQL com usuário e senha:

```env
DB_SERVER=localhost
DB_PORT=1433
DB_NAME=DB_FLOWOPS
DB_USER=flowops_app
DB_PASSWORD=defina-uma-senha-local-segura
DB_TRUST_SERVER_CERTIFICATE=true
JWT_SECRET_KEY=defina-uma-chave-aleatoria-com-no-minimo-32-caracteres
```

Nunca versione o arquivo `.env` ou senhas reais. Em produção, use certificado
confiável e remova `DB_TRUST_SERVER_CERTIFICATE=true`, pois o padrão seguro no
código é `false`.

Valores estáveis, como o driver ODBC, criptografia, algoritmo, emissor,
audiência e duração do JWT, permanecem versionados no código.

## Configuração automatizada do banco

Os scripts em `.scripts/database` preparam o banco. O Alembic é a única fonte
de verdade para schemas, tabelas e índices.

O bootstrap usa autenticação Windows somente para criar o banco e executar as
migrations administrativas. A aplicação continua usando exclusivamente o
login SQL `flowops_app`:

```powershell
.\.scripts\database\setup_database.ps1
```

A senha do login SQL é solicitada durante a execução e não é gravada. A ordem
automatizada é:

1. Criar `DB_FLOWOPS`, caso não exista.
2. Executar `python -m alembic upgrade head`.
3. Criar o login e o usuário `flowops_app`, caso ainda não existam.
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

### Evidências do motor de execuções

Execute separadamente as regras de domínio:

```powershell
python -m pytest tests/unit/test_execucao.py tests/unit/test_automacao.py -v
```

Execute a persistência e os contratos HTTP:

```powershell
python -m pytest tests/integration/test_sql_execucao_repository.py tests/integration/test_execucoes.py -v
```

Esses testes comprovam estados, transições, criação, histórico, detalhes,
paginação e isolamento entre equipes usando SQLite em memória. Eles não
comprovam ODBC, tipos específicos do SQL Server nem a aplicação real das
migrations.

No ambiente SQL Server, confira primeiro a revisão sem alterar o banco:

```powershell
python -m alembic current
python -m alembic heads
```

A revisão esperada é `20260914_01`. O script
`.scripts/database/validate_database.sql` verifica a tabela
`operacao.execucoes`, seus índices, restrição de status, chaves estrangeiras e
a revisão do Alembic. O comando `alembic upgrade head` altera o banco e deve ser
executado somente no ambiente correto e com aprovação.

O Alembic mantém sua revisão exclusivamente em `dbo.alembic_version`. Essa
localização é declarada no `migrations/env.py` para não depender do schema
padrão do usuário que abre a conexão. Uma tabela `alembic_version` encontrada
em outro schema representa uma divergência histórica e não deve ser apagada ou
sincronizada antes de conferir todos os objetos do banco.
