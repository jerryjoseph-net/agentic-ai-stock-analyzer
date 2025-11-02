#!/bin/bash
# Install git hooks for this repository

echo "Setting up git hooks..."

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy hook files
cp .githooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# For Windows/PowerShell support, create a wrapper
if command -v pwsh &> /dev/null; then
    cp .githooks/pre-commit.ps1 .git/hooks/pre-commit.ps1
fi

echo "✓ Git hooks installed successfully!"
echo "Pre-commit checks will now run automatically before each commit."
