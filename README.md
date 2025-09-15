
# senior-python

* 🎯 **Goal**: main objective
* 📚 **Topics**: essential knowledge
* 🛠 **Hands-on**: practical exercises
* ✅ **Deliverable**: end-of-session product

---

# 🗓️ 20h Roadmap to Becoming a Senior Python Developer

---

## **Session 1 (2h) – Pythonic Mindset vs Java**

🎯 Goal: Understand Pythonic style and differences from Java  
📚 Topics:
* Zen of Python (`import this`)
* List/dict comprehension
* Context manager (`with`)
* f-strings

🛠 Hands-on:
* Write a script to read a CSV file → filter rows by condition (Java → Pythonic).
* Compare the same logic written in Java-style loop and Pythonic-style.

✅ Deliverable: `csv_parser.py` with 2 versions (imperative vs pythonic).

---

## **Session 2 (2h) – OOP and Code Organization**

🎯 Goal: Write Pythonic classes and organize modules/packages  
📚 Topics:
* Class, dataclass, `__str__`, `__repr__`
* Package, `__init__.py`
* Basic typing

🛠 Hands-on:
* Create `models/` containing a `User` class (dataclass).
* Create a `services/` module for in-memory CRUD user operations.

✅ Deliverable: project skeleton `myapp/` with `models` + `services` packages.

---

## **Session 3 (2h) – Generators & Iterators**

🎯 Goal: Understand lazy evaluation and pipelines  
📚 Topics:
* `yield`, generator expression
* `itertools`
* Comparison with Java Stream API

🛠 Hands-on:
* Write a generator to read a huge log file → yield each error line.
* Write a pipeline: filter → transform → aggregate.

✅ Deliverable: `log_parser.py` able to process logs >100MB without high RAM usage.

---

## **Session 4 (2h) – Decorators & Metaprogramming**

🎯 Goal: Understand decorators and basic metaclasses  
📚 Topics:
* Function decorator (`@log_time`, `@cache`)
* Class decorator
* Metaclass (simple registry example)

🛠 Hands-on:
* Write a `@benchmark` decorator to measure function execution time.
* Create a metaclass to automatically register all `Service` classes in a registry.

✅ Deliverable: `decorators.py` + `registry.py`.

---

## **Session 5 (2h) – Async & Concurrency**

🎯 Goal: Write async programs (compare with Java threads)  
📚 Topics:
* `async/await`, `asyncio`
* Task scheduling, gather
* `aiohttp` for URL fetching

🛠 Hands-on:
* Write an async crawler to download 10 URLs in parallel.
* Compare with a multi-threaded version.

✅ Deliverable: `crawler_async.py`.

---

## **Session 6 (2h) – Python Runtime & Performance**

🎯 Goal: Understand GIL, memory, bytecode  
📚 Topics:
* GIL, threading vs multiprocessing
* Reference counting, GC
* `dis` module to view bytecode
* `timeit`, big-O analysis

🛠 Hands-on:
* Benchmark bubble sort vs quicksort (Python implementation).
* Use `dis.dis` to view a function's bytecode.

✅ Deliverable: `perf_test.py` + `notes.md` explaining GIL/bytecode.

---

## **Session 7 (2h) – Clean Code & Tooling**

🎯 Goal: Set up a professional environment  
📚 Topics:
* PEP 8, type hints
* `mypy`, `flake8`, `black`, `isort`
* `pytest`

🛠 Hands-on:
* Create a poetry project `mytool/`.
* Add 2–3 functions with type hints + tests.
* Run `black` + `mypy`.

✅ Deliverable: repo with `pyproject.toml`, `tests/`, local CI lint/test.

---

## **Session 8 (2h) – Frameworks: FastAPI & Pandas**

🎯 Goal: Get familiar with main frameworks  
📚 Topics:
* FastAPI (router, dependency, pydantic)
* Pandas basics (read CSV, groupby)

🛠 Hands-on:
* Write a CRUD API for `User` using FastAPI.
* Write a script to analyze a CSV dataset with Pandas.

✅ Deliverable: `main.py` running FastAPI CRUD + `analysis.py` for dataset processing.

---

## **Session 9 (2h) – Deployment Mindset**

🎯 Goal: Deploy app to production  
📚 Topics:
* Dockerize Python app
* Uvicorn + Gunicorn
* Config via `.env`

🛠 Hands-on:
* Write a `Dockerfile` for the FastAPI app.
* Run `docker-compose up`.

✅ Deliverable: Containerized FastAPI app.

---

## **Session 10 (2h) – Senior Practices & Scalability**

🎯 Goal: Senior dev mindset in large projects  
📚 Topics:
* CI/CD basics (GitHub Actions test + build)
* Logging (structlog/loguru)
* Scale (async workers, distributed)

🛠 Hands-on:
* Add GitHub Actions workflow (lint + test).
* Add logging decorator to the app.

✅ Deliverable: Repo with CI/CD + logs + dockerized app.

---

# 📦 Final result after 20h

* Complete `myapp/` repo:
  * Pythonic code (generators, decorators, async, OOP)
  * Test + lint + type hints
  * FastAPI CRUD API
  * Dockerized + basic CI/CD
* Note `senior_mindset.md`: mapping Java → Python, best practices, performance tips.

