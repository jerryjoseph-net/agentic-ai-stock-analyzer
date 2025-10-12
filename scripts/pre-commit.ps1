#!/usr/bin/env pwsh
# pre-commit.ps1 - Run type checking and tests before commit

Write-Host "Running type check..."
$TypeCheckResult = & ./scripts/type-check.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Type check failed. Aborting commit."
    exit 1
}
Write-Host "Type check passed."



Write-Host "Running unit tests..."
$UnitTestResult = & .venv/Scripts/python.exe -m pytest tests/unit/ -v
if ($LASTEXITCODE -ne 0) {
    Write-Host "Unit tests failed. Aborting commit."
    exit 1
}
Write-Host "Unit tests passed."

Write-Host "Running unit tests with coverage..."
$CoverageResult = & .venv/Scripts/python.exe -m pytest tests/unit/ -v --cov=src --cov-report=term-missing --cov-fail-under=40
if ($LASTEXITCODE -ne 0) {
    Write-Host "Unit test coverage below 40%. Aborting commit."
    exit 1
}
Write-Host "Unit test coverage is above 40%."

Write-Host "Running all tests..."
$AllTestResult = & .venv/Scripts/python.exe -m pytest tests/ -v
if ($LASTEXITCODE -ne 0) {
    Write-Host "Some tests failed. Aborting commit."
    exit 1
}
Write-Host "All tests passed."

Write-Host "Pre-commit checks passed. You may commit now."
exit 0
