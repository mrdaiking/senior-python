"""
Senior-level logging configuration with structured logging.
"""
import asyncio
import functools
import time
from typing import Any, Callable

import structlog
from loguru import logger

# Configure structlog for structured JSON logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    context_class=dict,
    cache_logger_on_first_use=True,
)

# Configure loguru for human-readable console logging
logger.remove()  # Remove default handler
logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
)
logger.add(
    "logs/error_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
)

# Console logging for development
logger.add(
    lambda msg: print(msg, end=""),
    level="DEBUG",
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>\n",
)


def log_execution_time(func: Callable) -> Callable:
    """
    Decorator để log thời gian thực thi của function.

    Usage:
        @log_execution_time
        def my_function():
            pass
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        function_name = f"{func.__module__}.{func.__name__}"

        logger.info(f"🚀 Starting {function_name}")

        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time

            logger.success(f"✅ Completed {function_name} in {execution_time:.3f}s")

            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"❌ Failed {function_name} after {execution_time:.3f}s: {str(e)}"
            )
            raise

    return wrapper


def log_api_call(func: Callable) -> Callable:
    """
    Decorator chuyên dụng cho API endpoints.
    Log request info, response time, status.
    """

    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        endpoint = f"{func.__module__}.{func.__name__}"

        # Extract request info if available
        request_info = {}
        for arg in args:
            if hasattr(arg, "url"):  # FastAPI Request object
                request_info = {
                    "method": arg.method,
                    "url": str(arg.url),
                    "client": arg.client.host if arg.client else None,
                }

        struct_logger = structlog.get_logger()
        struct_logger.info("api_request_start", endpoint=endpoint, **request_info)

        try:
            result = (
                await func(*args, **kwargs)
                if asyncio.iscoroutinefunction(func)
                else func(*args, **kwargs)
            )
            execution_time = time.time() - start_time

            struct_logger.info(
                "api_request_success",
                endpoint=endpoint,
                execution_time=execution_time,
                **request_info,
            )

            return result
        except Exception as e:
            execution_time = time.time() - start_time
            struct_logger.error(
                "api_request_error",
                endpoint=endpoint,
                execution_time=execution_time,
                error=str(e),
                **request_info,
            )
            raise

    return async_wrapper


def get_logger(name: str) -> Any:
    """
    Factory function để tạo logger cho từng module.

    Args:
        name: Tên module (thường dùng __name__)

    Returns:
        Logger instance
    """
    return logger.bind(module=name)


# Business metrics logging
def log_business_event(event_name: str, **kwargs: Any) -> None:
    """
    Log business events cho analytics/monitoring.

    Args:
        event_name: Tên event (user_created, order_placed, etc.)
        **kwargs: Additional metadata
    """
    struct_logger = structlog.get_logger()
    struct_logger.info(
        "business_event",
        event_name=event_name,
        timestamp=time.time(),
        **kwargs,
    )
