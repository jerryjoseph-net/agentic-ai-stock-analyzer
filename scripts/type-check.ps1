#!/usr/bin/env pwsh
# PowerShell script to run mypy type checking locally

Write-Host "Running mypy type checking..." -ForegroundColor Cyan

# Ensure we're in the project root
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Virtual environment not detected. Activating .venv..." -ForegroundColor Yellow
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        & ".venv\Scripts\Activate.ps1"
    } else {
        Write-Host "Virtual environment not found. Please create and activate .venv first." -ForegroundColor Red
        exit 1
    }
}

# Run mypy type checking
Write-Host "Running: mypy src/ --ignore-missing-imports" -ForegroundColor Gray
try {
    & mypy src/ --ignore-missing-imports
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Type checking passed!" -ForegroundColor Green
    } else {
        Write-Host "Type checking failed with exit code $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
} catch {
    Write-Host "Error running mypy: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Try: pip install mypy" -ForegroundColor Yellow
    exit 1
}

Write-Host "Type checking complete!" -ForegroundColor Cyan