"""Main FastAPI application for Finance AI Agent."""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from backend.config import get_settings
from backend.routes import stock, news, analysis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    logger.info("Starting Finance AI Agent API...")
    settings = get_settings()
    logger.info(f"Server running on {settings.host}:{settings.port}")
    yield
    # Shutdown
    logger.info("Shutting down Finance AI Agent API...")


# Create FastAPI app
app = FastAPI(
    title="Finance AI Agent API",
    description="AI-powered financial analysis and investment insights",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=400,
        content={"error": "Bad Request", "detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": "An unexpected error occurred"}
    )


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "status": "ok",
        "message": "Finance AI Agent API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    settings = get_settings()
    return {
        "status": "healthy",
        "services": {
            "stock_data": "available",
            "news": "available" if settings.finnhub_api_key else "unavailable",
            "ai_agent": "available" if settings.anthropic_api_key else "unavailable"
        }
    }


# Include routers
app.include_router(stock.router, prefix="/api", tags=["Stock Data"])
app.include_router(news.router, prefix="/api", tags=["News"])
app.include_router(analysis.router, prefix="/api", tags=["AI Analysis"])


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "backend.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
