# Pre-commit hook for running quality checks before committing (PowerShell version)
# This hook calls scripts/pre-commit.ps1

$ErrorActionPreference = "Stop"

# Get the project root directory
$ProjectRoot = git rev-parse --show-toplevel
Set-Location $ProjectRoot

# Run the main pre-commit script
& ./scripts/pre-commit.ps1
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host "Pre-commit checks passed!" -ForegroundColor Green
exit 0
