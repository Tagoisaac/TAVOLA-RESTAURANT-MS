from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.session import engine
from app.db import models
from app.api.v1 import api_router

# Try to create all database tables, but don't fail if database is unavailable
try:
    models.BaseModel.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not initialize database: {e}")
    print("Running in development mode without database")

# Seed default permissions and ensure admin role has permissions
try:
    from app.db.session import SessionLocal
    db = SessionLocal()
    # Default permissions
    default_perms = [
        ("view_users", "View users"),
        ("manage_users", "Create/update/delete users"),
        ("view_roles", "View roles"),
        ("manage_roles", "Create/update/delete roles"),
        ("view_permissions", "View permissions"),
        ("manage_permissions", "Create/delete permissions"),
    ]
    perms = []
    for name, desc in default_perms:
        p = db.query(models.User.__table__.metadata.tables['permission'].c if False else models.Permission).filter(models.Permission.name == name).first()
        if not p:
            p = models.Permission(name=name, description=desc)
            db.add(p)
            db.commit()
            db.refresh(p)
        perms.append(p)

    # Ensure admin role exists and has all permissions
    admin_role = db.query(models.Role).filter(models.Role.name == 'admin').first()
    if not admin_role:
        admin_role = models.Role(name='admin', description='Administrator')
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    # Attach permissions to admin role
    for p in perms:
        if p not in admin_role.permissions:
            admin_role.permissions.append(p)
    db.commit()
    db.close()
except Exception as e:
    print(f"Warning: Failed to seed permissions: {e}")

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

# Include API routers
app.include_router(api_router)

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
        "endpoints": {
            "auth": f"{settings.API_V1_STR}/auth",
            "admin": f"{settings.API_V1_STR}/admin",
            "restaurant": f"{settings.API_V1_STR}/restaurant",
            "cashier": f"{settings.API_V1_STR}/cashier",
            "inventory": f"{settings.API_V1_STR}/inventory",
        }
    }

# API v1 root
@app.get(f"{settings.API_V1_STR}/")
async def api_v1_root():
    return {
        "message": "API v1 - Tavola Restaurant Management System",
        "endpoints": {
            "authentication": "/auth/login",
            "admin": "/admin/users",
            "restaurant": "/restaurant/orders",
            "cashier": "/cashier/payments",
            "inventory": "/inventory/items",
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
