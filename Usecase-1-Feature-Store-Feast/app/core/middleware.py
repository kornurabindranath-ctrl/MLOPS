import logging
import time
import uuid

from fastapi import Request

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())

    start = time.perf_counter()

    response = await call_next(request)

    duration_ms = round((time.perf_counter() - start) * 1000, 2)

    logger.info(
        "request_completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "latency_ms": duration_ms,
        },
    )

    response.headers["X-Request-ID"] = request_id

    return response
