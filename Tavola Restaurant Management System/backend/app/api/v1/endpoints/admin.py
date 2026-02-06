from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserResponse, UserCreate, UserUpdate, RoleResponse, RoleCreate, PermissionResponse, PermissionCreate
from app.crud import user as crud_user

router = APIRouter(prefix="/admin", tags=["admin"])

# User endpoints
@router.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """List all users"""
    return crud_user.get_users(db)

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    existing = crud_user.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud_user.create_user(db, user)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user"""
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """Update a user"""
    updated = crud_user.update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    deleted = crud_user.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"deleted": True}

# Role endpoints
@router.get("/roles", response_model=list[RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    """List all roles"""
    return crud_user.get_roles(db)

@router.post("/roles", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    """Create a new role"""
    return crud_user.create_role(db, role)

@router.get("/roles/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get a specific role"""
    role = crud_user.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/roles/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role: RoleCreate, db: Session = Depends(get_db)):
    """Update a role"""
    updated = crud_user.update_role(db, role_id, role)
    if not updated:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated

@router.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    """Delete a role"""
    deleted = crud_user.delete_role(db, role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"deleted": True}

# Permission endpoints
@router.get("/permissions", response_model=list[PermissionResponse])
def list_permissions(db: Session = Depends(get_db)):
    """List all permissions"""
    return crud_user.get_permissions(db)

@router.post("/permissions", response_model=PermissionResponse)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    """Create a new permission"""
    return crud_user.create_permission(db, permission)

@router.delete("/permissions/{permission_id}")
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    """Delete a permission"""
    deleted = crud_user.delete_permission(db, permission_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"deleted": True}

# Role-Permission assignment
@router.post("/roles/{role_id}/permissions/{permission_id}")
def assign_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    """Assign a permission to a role"""
    result = crud_user.assign_permission_to_role(db, role_id, permission_id)
    if not result:
        raise HTTPException(status_code=404, detail="Role or Permission not found")
    return {"status": "permission assigned"}
