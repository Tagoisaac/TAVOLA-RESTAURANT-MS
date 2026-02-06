from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.session import engine
from app.db import models

# Try to create all database tables, but don't fail if database is unavailable
try:
    models.BaseModel.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not initialize database: {e}")
    print("Running in development mode without database")

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Restaurant Management System API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
        },
    )

@app.get("/")
async def root():
    return {
        "message": "Welcome to Tavola Restaurant Management System API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_STR}/docs",
    }

# API v1 routes
@app.get(f"{settings.API_V1_STR}/")
async def api_v1_root():
    return {
        "message": "API v1",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc",
        },
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
