# Run every check that CI runs. Usage: .\scripts\check.ps1
$ErrorActionPreference = "Stop"
foreach ($cmd in @("ruff check .", "ruff format --check .", "mypy", "pytest --cov --cov-report=term-missing")) {
    Write-Host "==> $cmd"
    Invoke-Expression $cmd
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
