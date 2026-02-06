from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PermissionResponse(PermissionCreate):
    id: int

    class Config:
        from_attributes = True

class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permission_ids: Optional[List[int]] = []

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    permissions: List[PermissionResponse] = []

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    role_id: int

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    last_login: Optional[datetime] = None
    role: RoleResponse

    class Config:
        from_attributes = True
