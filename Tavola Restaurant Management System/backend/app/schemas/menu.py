from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MenuCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True

class MenuCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class MenuItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category_id: int
    price: float
    cost: float
    is_available: bool

    class Config:
        from_attributes = True

class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: int
    price: float
    cost: float
    is_available: bool = True
