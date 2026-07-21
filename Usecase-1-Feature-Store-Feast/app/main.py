from fastapi import FastAPI

from app.core.settings import settings
from app.core.logging import setup_logging
from app.core.middleware import log_requests
from app.api.routes import router

# Configure logging first
setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
)

# Register middleware
app.middleware("http")(log_requests)

# Register routes
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "healthy"}
