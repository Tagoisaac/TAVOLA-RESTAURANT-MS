from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.config import settings
from app.db.session import get_db
from app.schemas import UserCreate, UserResponse, RoleCreate, RoleResponse, PermissionCreate, PermissionResponse
from app.crud import user as crud_user

router = APIRouter(prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])

# User Management
@router.get("/users", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users"""
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = crud_user.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=UserResponse)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create new user"""
    existing_user = crud_user.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    existing_email = crud_user.get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user = crud_user.create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name,
        role_id=user_data.role_id
    )
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    """Update user"""
    user = crud_user.update_user(db, user_id, **user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete user"""
    user = crud_user.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Role Management
@router.get("/roles", response_model=List[RoleResponse])
def list_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all roles"""
    roles = crud_user.get_roles(db, skip=skip, limit=limit)
    return roles

@router.get("/roles/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get role by ID"""
    role = crud_user.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.post("/roles", response_model=RoleResponse)
def create_role(role_data: RoleCreate, db: Session = Depends(get_db)):
    """Create new role"""
    role = crud_user.create_role(db, role_data.name, role_data.description)
    
    # Assign permissions if provided
    if role_data.permission_ids:
        for permission_id in role_data.permission_ids:
            crud_user.assign_permission_to_role(db, role.id, permission_id)
    
    return role

@router.put("/roles/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role_data: dict, db: Session = Depends(get_db)):
    """Update role"""
    role = crud_user.update_role(db, role_id, **role_data)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    """Delete role"""
    role = crud_user.delete_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deleted successfully"}

# Permission Management
@router.get("/permissions", response_model=List[PermissionResponse])
def list_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all permissions"""
    permissions = crud_user.get_permissions(db, skip=skip, limit=limit)
    return permissions

@router.post("/permissions", response_model=PermissionResponse)
def create_permission(permission_data: PermissionCreate, db: Session = Depends(get_db)):
    """Create new permission"""
    permission = crud_user.create_permission(db, permission_data.name, permission_data.description)
    return permission

@router.delete("/permissions/{permission_id}")
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    """Delete permission"""
    permission = crud_user.delete_permission(db, permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"message": "Permission deleted successfully"}

# Role-Permission Association
@router.post("/roles/{role_id}/permissions/{permission_id}")
def assign_permission(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    """Assign permission to role"""
    role = crud_user.assign_permission_to_role(db, role_id, permission_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Permission assigned successfully"}

@router.delete("/roles/{role_id}/permissions/{permission_id}")
def remove_permission(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    """Remove permission from role"""
    role = crud_user.remove_permission_from_role(db, role_id, permission_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Permission removed successfully"}
