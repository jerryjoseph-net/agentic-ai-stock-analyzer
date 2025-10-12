#!/usr/bin/env pwsh
# pre-commit.ps1 - Run type checking and tests before commit

Write-Host "Running type check..."
$TypeCheckResult = & ./scripts/type-check.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Type check failed. Aborting commit."
    exit 1
}
Write-Host "Type check passed."

Write-Host "Running tests..."
$TestResult = & .venv/Scripts/python.exe -m pytest tests/
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tests failed. Aborting commit."
    exit 1
}
Write-Host "All tests passed."

Write-Host "Pre-commit checks passed. You may commit now."
exit 0
