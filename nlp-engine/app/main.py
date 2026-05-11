from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.routes.analyze_routes import router as analyze_router
from app.config.config import settings
from app.utils.logging import logger

# Rate Limiter Setup
limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"])

app = FastAPI(
    title="ProofNexa NLP Engine",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get("/")
async def root():
    return {"message": "ProofNexa NLP Engine is running", "docs": "/docs"}

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Structured Error Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error on {request.url.path}")
    safe_errors = []
    for error in exc.errors():
        safe_error = {
            "loc": [str(l) for l in error.get("loc", [])],
            "msg": str(error.get("msg", "")),
            "type": str(error.get("type", ""))
        }
        safe_errors.append(safe_error)
        
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "detail": "Validation error",
            "errors": safe_errors
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "detail": "Internal NLP Engine Error"
        }
    )

# CORS Configuration (Production-Ready)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(analyze_router)
