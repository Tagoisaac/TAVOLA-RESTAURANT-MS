from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class MenuCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True

class MenuCategoryResponse(MenuCategoryCreate):
    id: int

    class Config:
        from_attributes = True

class MenuItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    cost: float
    category_id: int
    is_available: bool = True
    image_url: Optional[str] = None
    preparation_time: Optional[int] = None

class MenuItemResponse(MenuItemCreate):
    id: int

    class Config:
        from_attributes = True

class IngredientCreate(BaseModel):
    name: str
    description: Optional[str] = None
    unit: str
    current_stock: float = 0
    min_stock_level: float = 0

class IngredientResponse(IngredientCreate):
    id: int

    class Config:
        from_attributes = True
