# MyTool - Professional Python Project

A professional Python project demonstrating best practices for type hints, testing, and code quality.

## Setup

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## Development

### Code Quality Tools

```bash
# Format code
poetry run black src/ tests/

# Sort imports
poetry run isort src/ tests/

# Lint code
poetry run flake8 src/ tests/

# Type check
poetry run mypy src/
```

### Testing

```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src/mytool --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Project Structure

```
mytool/
├── pyproject.toml          # Project configuration
├── README.md              # This file
├── src/
│   └── mytool/
│       ├── __init__.py    # Package initialization
│       ├── calculator.py  # Calculator class
│       └── text_processor.py  # Text processing utilities
└── tests/
    ├── test_calculator.py     # Calculator tests
    └── test_text_processor.py # Text processor tests
```

## Code Quality Standards

- ✅ **PEP 8** compliance (flake8)
- ✅ **Type hints** for all functions/classes (mypy)
- ✅ **Formatting** with black
- ✅ **Import sorting** with isort
- ✅ **Test coverage** >80% (pytest-cov)

## Hands-on Exercises

1. Thêm function mới vào `utils.py` với type hints và test
2. Viết class mới với docstring và type hints
3. Fix mọi lỗi mypy, flake8
4. Đạt 100% test coverage
