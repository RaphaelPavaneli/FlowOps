param(
    [string]$Server = "localhost"
)

$ErrorActionPreference = "Stop"
$backendDirectory = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$pythonPath = Join-Path $backendDirectory ".venv\Scripts\python.exe"
$envPath = Join-Path $backendDirectory ".env"

if (-not (Test-Path -LiteralPath $pythonPath)) {
    throw "Ambiente virtual não encontrado em $pythonPath."
}

if (-not (Test-Path -LiteralPath $envPath)) {
    throw "Crie o arquivo .env a partir do .env.example antes de continuar."
}

function Invoke-SqlScript {
    param([string]$ScriptName)

    $scriptPath = Join-Path $PSScriptRoot $ScriptName
    & sqlcmd -S $Server -E -C -b -i $scriptPath
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao executar $ScriptName."
    }
}

Push-Location $backendDirectory
try {
    Invoke-SqlScript "01_create_database.sql"

    $previousServer = $env:DB_SERVER
    $previousDatabase = $env:DB_NAME
    $previousMigrationConnection = (
        $env:FLOWOPS_MIGRATION_TRUSTED_CONNECTION
    )

    $env:DB_SERVER = $Server
    $env:DB_NAME = "DB_FLOWOPS"
    $env:FLOWOPS_MIGRATION_TRUSTED_CONNECTION = "true"

    & $pythonPath -m alembic upgrade head
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao aplicar as migrations Alembic."
    }

    $securePassword = Read-Host "Senha do login flowops_app" -AsSecureString
    $passwordPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR(
        $securePassword
    )

    try {
        $plainPassword = [Runtime.InteropServices.Marshal]::PtrToStringBSTR(
            $passwordPointer
        )
        $env:FLOWOPS_APPLICATION_PASSWORD = $plainPassword.Replace("'", "''")
        Invoke-SqlScript "02_create_application_login.sql"
        Invoke-SqlScript "03_grant_application_permissions.sql"
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($passwordPointer)
        Remove-Item Env:FLOWOPS_APPLICATION_PASSWORD -ErrorAction SilentlyContinue
        $plainPassword = $null
    }

    Invoke-SqlScript "validate_database.sql"
    Write-Host "Banco configurado e validado com sucesso."
}
finally {
    $env:DB_SERVER = $previousServer
    $env:DB_NAME = $previousDatabase
    $env:FLOWOPS_MIGRATION_TRUSTED_CONNECTION = (
        $previousMigrationConnection
    )
    Pop-Location
}
