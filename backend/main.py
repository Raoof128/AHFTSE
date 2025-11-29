import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api import evaluate
from backend.core.config import settings
from backend.core.logger import logger


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Trust Score Engine & Hallucination Firewall API",
        version=settings.VERSION,
    )

    # CORS for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include Routers
    app.include_router(evaluate.router, prefix=settings.API_V1_STR)

    # Serve Frontend
    # Locate frontend directory relative to this file
    # backend/main.py -> ../frontend
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    frontend_path = os.path.join(base_dir, "frontend")

    if os.path.exists(frontend_path):
        logger.info("Mounting frontend from: %s", frontend_path)
        app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    else:
        logger.warning("Frontend directory not found at: %s", frontend_path)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
