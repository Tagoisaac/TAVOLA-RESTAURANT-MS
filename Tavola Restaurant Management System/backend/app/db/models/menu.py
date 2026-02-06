from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel

class MenuCategory(BaseModel):
    __tablename__ = "menu_category"
    
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    items = relationship("MenuItem", back_populates="category")

class MenuItem(BaseModel):
    __tablename__ = "menu_item"
    
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)  # Cost to prepare (for profit calculation)
    is_available = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)
    preparation_time = Column(Integer)  # in minutes
    
    # Foreign Keys
    category_id = Column(Integer, ForeignKey("menu_category.id"), nullable=False)
    
    # Relationships
    category = relationship("MenuCategory", back_populates="items")
    ingredients = relationship("MenuItemIngredient", back_populates="menu_item")

class Ingredient(BaseModel):
    __tablename__ = "ingredient"
    
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    unit = Column(String)  # kg, g, l, ml, pcs, etc.
    current_stock = Column(Float, default=0)
    min_stock_level = Column(Float, default=0)
    reorder_level = Column(Float, default=0)
    
    # Relationships
    menu_items = relationship("MenuItemIngredient", back_populates="ingredient")
    stock_movements = relationship("StockMovement", back_populates="ingredient")

class MenuItemIngredient(BaseModel):
    __tablename__ = "menu_item_ingredient"
    
    menu_item_id = Column(Integer, ForeignKey("menu_item.id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"), primary_key=True)
    quantity = Column(Float, nullable=False)  # Amount of ingredient needed
    
    # Relationships
    menu_item = relationship("MenuItem", back_populates="ingredients")
    ingredient = relationship("Ingredient", back_populates="menu_items")

class StockMovement(BaseModel):
    __tablename__ = "stock_movement"
    
    MOVEMENT_TYPES = ["purchase", "consumption", "adjustment", "waste"]
    
    ingredient_id = Column(Integer, ForeignKey("ingredient.id"), nullable=False)
    quantity = Column(Float, nullable=False)  # Can be positive (addition) or negative (consumption)
    movement_type = Column(String, nullable=False)  # purchase, consumption, adjustment, waste
    reference_id = Column(Integer, nullable=True)  # Can reference order_id, purchase_id, etc.
    notes = Column(String)
    
    # Relationships
    ingredient = relationship("Ingredient", back_populates="stock_movements")
