#!/usr/bin/env pwsh
# pre-commit.ps1 - Run quality checks and tests before commit

Write-Host "Running type check..."
uv run mypy src/ --ignore-missing-imports
if ($LASTEXITCODE -ne 0) {
    Write-Host "Type check failed. Aborting commit." -ForegroundColor Red
    exit 1
}
Write-Host "Type check passed!" -ForegroundColor Green

Write-Host "Running unit tests..."
uv run pytest tests/unit/ -v
if ($LASTEXITCODE -ne 0) {
    Write-Host "Unit tests failed. Aborting commit." -ForegroundColor Red
    exit 1
}
Write-Host "Unit tests passed!" -ForegroundColor Green

Write-Host "Running unit tests with coverage..."
uv run pytest tests/unit/ -v --cov=src --cov-report=term-missing --cov-fail-under=30
if ($LASTEXITCODE -ne 0) {
    Write-Host "Unit test coverage below 30%. Aborting commit." -ForegroundColor Red
    exit 1
}
Write-Host "Unit test coverage is above 30%." -ForegroundColor Green

Write-Host "Running all tests..."
uv run pytest tests/ -v
if ($LASTEXITCODE -ne 0) {
    Write-Host "All tests failed. Aborting commit." -ForegroundColor Red
    exit 1
}
Write-Host "All tests passed!" -ForegroundColor Green

Write-Host "Pre-commit checks passed. You may commit now." -ForegroundColor Green
exit 0
