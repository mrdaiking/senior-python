# AGENTS.md

## Overview
This repository, `senior-python`, is designed to guide developers from intermediate to senior-level Python proficiency through a structured 20-hour roadmap. It includes Pythonic coding practices, OOP, async programming, performance optimization, and deployment with FastAPI and Docker.

## Setup
To set up the development environment:
```bash
# Install Poetry (dependency manager)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

## Code Style
- Follow **PEP 8** guidelines for Python code.
- Use **type hints** for all functions and classes (enforced by `mypy`).
- Format code with **black** (2-space indentation, max line length 88).
- Sort imports with **isort**.
- Prefer **f-strings** for string formatting.
- Use **dataclasses** for simple data models.
- Write **Pythonic code** (e.g., list/dict comprehensions, context managers, generators).
- Avoid Java-style verbose loops; prefer concise, functional patterns.

Example:
```python
# Good (Pythonic)
users = [User(name=name) for name in names]

# Bad (Java-style)
users = []
for name in names:
    users.append(User(name=name))
```

## Testing
To run tests:
```bash
# Run pytest with coverage
poetry run pytest --cov=src --cov-report=html
```

- Write tests in the `tests/` directory.
- Ensure at least 80% test coverage.
- Use `pytest` fixtures for reusable test setups.

## Project Structure
```
senior-python/
├── AGENTS.markdown
├── README.md
├── session
│   ├── *.py

```

## Development Workflow
- **Linting**: Run `poetry run black . && poetry run isort . && poetry run flake8 .` to ensure code quality.
- **Type checking**: Run `poetry run mypy .` to enforce type safety.
- **Testing**: Run tests before committing (see Testing section).
- **Commits**: Use clear commit messages (e.g., "Add User dataclass with type hints").
- **Pull Requests**:
  - Run linters and tests before submitting.
  - Include a description of changes and link to relevant session (e.g., Session 5: Async crawler).
  - Ensure CI/CD pipeline (GitHub Actions) passes.

## Running the FastAPI App
To run the FastAPI application:
```bash
# Run locally with uvicorn
poetry run uvicorn myapp.main:app --reload
```

To run the containerized app:
```bash
# Build and run with Docker
docker-compose up --build
```

## Performance and Debugging
- Use `dis` module to inspect bytecode for performance analysis:
  ```bash
  python -m dis myapp/perf_test.py
  ```
- Use `timeit` for benchmarking:
  ```bash
  python -m timeit -s "from myapp.perf_test import bubble_sort, quicksort" "bubble_sort([1, 3, 2])"
  ```
- For large log files, use generators to minimize memory usage (see `log_parser.py`).

## Additional Notes
- For async tasks (e.g., `crawler_async.py`), use `aiohttp` for HTTP requests and `asyncio.gather` for parallel execution.
- For logging, prefer `loguru` or `structlog` (configured in Session 10).
- Refer to `senior_mindset.md` for best practices and Python-vs-Java comparisons.