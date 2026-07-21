from fastapi import FastAPI
from prometheus_client import make_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.settings import settings
from app.core.logging import setup_logging
from app.core.middleware import log_requests
from app.api.routes import router

setup_logging()

app = FastAPI(title=settings.app_name)

app.middleware("http")(log_requests)

app.include_router(router)

Instrumentator().instrument(app)

# Mount Prometheus directly
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/health")
def health():
    return {"status": "healthy"}
