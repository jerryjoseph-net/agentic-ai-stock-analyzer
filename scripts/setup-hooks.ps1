# Install git hooks for this repository (PowerShell version)

Write-Host "Setting up git hooks..." -ForegroundColor Cyan

# Create hooks directory if it doesn't exist
$hooksDir = ".git/hooks"
if (-not (Test-Path $hooksDir)) {
    New-Item -ItemType Directory -Path $hooksDir -Force | Out-Null
}

# Copy hook files
Copy-Item ".githooks/pre-commit.ps1" "$hooksDir/pre-commit.ps1" -Force
Write-Host "Copied pre-commit.ps1 hook" -ForegroundColor Green

# Create a wrapper script that calls the PowerShell hook
$wrapperContent = @"
#!/bin/bash
# Wrapper to call PowerShell pre-commit hook on Windows or bash on Unix
if [[ `$OSTYPE == 'msys' || `$OSTYPE == 'cygwin' || `$OSTYPE == 'win32' ]]; then
    pwsh -NoProfile -ExecutionPolicy Bypass -File ".githooks/pre-commit.ps1"
else
    bash ".githooks/pre-commit"
fi
"@

$wrapperContent | Out-File -FilePath "$hooksDir/pre-commit" -Encoding ASCII -Force
Write-Host "Created pre-commit wrapper script" -ForegroundColor Green

Write-Host "[OK] Git hooks installed successfully!" -ForegroundColor Green
Write-Host "Pre-commit checks will now run automatically before each commit." -ForegroundColor Cyan
