#!/bin/bash
# Bash script to run mypy type checking locally

echo "🔍 Running mypy type checking..."

# Get the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not detected. Attempting to activate..."
    if [[ -f ".venv/bin/activate" ]]; then
        source .venv/bin/activate
        echo "✅ Virtual environment activated"
    else
        echo "❌ Virtual environment not found. Please create and activate .venv first."
        exit 1
    fi
fi

# Run mypy type checking
echo "Running: mypy src/ --ignore-missing-imports"
if mypy src/ --ignore-missing-imports; then
    echo "✅ Type checking passed!"
else
    exit_code=$?
    echo "❌ Type checking failed with exit code $exit_code"
    echo "💡 Try: pip install mypy"
    exit $exit_code
fi

echo "🎯 Type checking complete!"