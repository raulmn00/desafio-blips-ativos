"""Main FastAPI application module."""
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.routes.lead_routes import router as lead_router
from app.repositories.lead_repository import lead_repository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting application...")
    try:
        await lead_repository.connect()
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down application...")
    try:
        await lead_repository.disconnect()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description=settings.app_description,
    lifespan=lifespan,
)

# Include routers
app.include_router(lead_router)


@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint for health check.

    Returns:
        Application status and information
    """
    return {
        "status": "healthy",
        "application": settings.app_title,
        "version": settings.app_version,
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        Application health status
    """
    return {
        "status": "healthy",
        "database": "connected" if lead_repository.database is not None else "disconnected",
    }
