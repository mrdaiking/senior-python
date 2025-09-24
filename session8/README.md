# Session 9: Senior Python Development - CI/CD, Logging & Scaling

## 🎯 Mục tiêu
Học các best practices của senior Python developer:
- CI/CD với GitHub Actions
- Structured logging với loguru/structlog  
- Production scaling với Gunicorn + Uvicorn workers

## 🚀 Cải tiến so với Session 8

### 1. GitHub Actions CI/CD Pipeline
- **Linting**: flake8, black, isort, mypy
- **Testing**: pytest với coverage reporting
- **Multi-Python**: Test trên Python 3.9, 3.10, 3.11
- **Database Testing**: PostgreSQL service trong CI
- **Docker Build**: Tự động build và test Docker image

### 2. Production-Ready Logging
- **Loguru**: Human-readable console logs với colors/emojis
- **Structlog**: JSON structured logs cho production
- **Log Decorators**: 
  - `@log_execution_time`: Log thời gian thực thi
  - `@log_api_call`: Log API requests/responses
- **Business Events**: Track user actions cho analytics
- **Log Rotation**: Tự động rotate logs theo ngày

### 3. Production Scaling
- **Multi-stage Dockerfile**: Optimize build size
- **Non-root user**: Security best practice
- **Health checks**: Container và service health monitoring
- **Gunicorn + Uvicorn**: 4 workers cho production
- **Resource limits**: Memory và CPU constraints
- **Graceful shutdown**: Proper signal handling

## 📁 Cấu trúc thư mục

```
session8/
├── .github/workflows/
│   └── ci.yml                 # GitHub Actions CI pipeline
├── tests/
│   ├── conftest.py           # Test configuration
│   └── test_main.py          # Unit tests
├── logs/                     # Log files (auto-created)
├── main.py                   # FastAPI app với logging decorators
├── logging_config.py         # Structured logging setup
├── pyproject.toml           # Poetry dependencies + tools config
├── Dockerfile               # Multi-stage production build
├── docker-compose.yml       # Production-ready compose
├── .env                     # Development environment
├── .env.production          # Production environment
└── .gitignore              # Git ignore patterns
```

## 🛠 Cài đặt và chạy

### 1. Cài dependencies mới
```bash
cd session8
poetry install
```

### 2. Chạy tests
```bash
# Chạy tất cả tests với coverage
poetry run pytest --cov=. --cov-report=html

# Chỉ chạy unit tests
poetry run pytest tests/test_main.py -v

# Chạy với logging output
poetry run pytest -s
```

### 3. Code quality checks
```bash
# Format code
poetry run black .
poetry run isort .

# Lint code  
poetry run flake8 .

# Type checking
poetry run mypy .
```

### 4. Chạy production setup
```bash
# Build và run với production config
docker-compose up --build

# Xem logs real-time
docker-compose logs -f web

# Scale to multiple instances
docker-compose up --scale web=3
```

## 🔍 Logging Features

### Console Logs (Development)
```
10:30:15 | INFO | main:create_user:45 - 👤 Creating new user
10:30:15 | SUCCESS | main:create_user:67 - ✅ User created successfully
```

### Structured Logs (Production)
```json
{
  "event": "api_request_success",
  "timestamp": "2023-10-15T10:30:15.123Z",
  "endpoint": "main.create_user", 
  "execution_time": 0.045,
  "method": "POST",
  "url": "http://localhost:8000/users/"
}
```

### Business Event Tracking
```json
{
  "event": "business_event",
  "event_name": "user_created",
  "timestamp": 1697365815.123,
  "user_id": 1,
  "user_email": "john@example.com"
}
```

## 📊 Performance Optimizations

### 1. Docker Multi-stage Build
- **Builder stage**: Install dependencies
- **Runtime stage**: Copy only necessary files
- **Size reduction**: ~50% smaller images

### 2. Database Connection Pooling
- **Pool size**: 20 connections
- **Max overflow**: 30 additional connections  
- **Timeout**: 30 seconds

### 3. Gunicorn Configuration
- **Workers**: 4 (CPU cores)
- **Worker class**: uvicorn.workers.UvicornWorker
- **Timeout**: 120 seconds
- **Keep-alive**: 5 seconds

## 🚨 Monitoring & Alerting

### Health Checks
- **Application**: `GET /` endpoint
- **Database**: `pg_isready` command
- **Docker**: Built-in healthcheck

### Log Monitoring
- **Error logs**: Separate error log file
- **Business events**: JSON format for analytics
- **Performance**: Request/response times logged

## 🎯 Bài tập hands-on

### Bài 1: Setup CI/CD
1. Push code lên GitHub
2. Xem GitHub Actions chạy
3. Fix linting errors nếu có
4. Đảm bảo all tests pass

### Bài 2: Test Logging
1. Tạo user mới qua API
2. Check console logs (emoji + colors)
3. Check file logs trong `logs/` folder
4. Tìm business event trong structured logs

### Bài 3: Load Testing
1. Scale app: `docker-compose up --scale web=3`
2. Dùng `curl` hoặc `wrk` để test performance
3. Monitor logs của multiple instances
4. Compare performance single vs multiple workers

### Bài 4: Error Handling
1. Thêm intentional error vào code
2. Trigger error qua API call
3. Check error logs và structured format
4. Verify error tracking và alerting

## 📚 Tài liệu tham khảo
- [GitHub Actions for Python](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python)
- [Loguru Documentation](https://loguru.readthedocs.io/)
- [Structlog Guide](https://www.structlog.org/)
- [Gunicorn Deployment](https://docs.gunicorn.org/en/stable/deploy.html)
- [FastAPI Production](https://fastapi.tiangolo.com/deployment/)

---

Bài này bao gồm tất cả essential skills của senior Python developer: CI/CD automation, production logging, và scaling strategies! 🚀