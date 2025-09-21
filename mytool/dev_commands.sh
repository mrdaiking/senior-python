#!/bin/bash
# Development commands for mytool project

echo "🔧 Development Tools for mytool"
echo "==============================="

# Format code with black
echo "📝 Formatting code with black..."
poetry run black src/ tests/

# Sort imports with isort  
echo "📦 Sorting imports with isort..."
poetry run isort src/ tests/

# Lint with flake8
echo "🔍 Linting with flake8..."
poetry run flake8 src/ tests/

# Type check with mypy
echo "🔎 Type checking with mypy..."
poetry run mypy src/

# Run tests with coverage
echo "🧪 Running tests with coverage..."
poetry run pytest --cov=src/mytool --cov-report=html --cov-report=term-missing

echo "✅ All development checks complete!"
echo ""
echo "📊 Coverage report: htmlcov/index.html"
echo "🐛 Fix any issues above before committing"
