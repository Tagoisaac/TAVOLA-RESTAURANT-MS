from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.core.config import settings
from app.db.session import get_db
from app.schemas import (
    MenuCategoryCreate, MenuCategoryResponse, MenuItemCreate, MenuItemResponse,
    TableCreate, TableResponse, OrderCreate, OrderResponse, OrderItemCreate,
    PaymentCreate, PaymentResponse
)
from app.crud import menu as crud_menu
from app.crud import order as crud_order

router = APIRouter(prefix=f"{settings.API_V1_STR}/restaurant", tags=["restaurant"])

# Menu Category Endpoints
@router.get("/categories", response_model=List[MenuCategoryResponse])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all menu categories"""
    categories = crud_menu.get_menu_categories(db, skip=skip, limit=limit)
    return categories

@router.post("/categories", response_model=MenuCategoryResponse)
def create_category(category_data: MenuCategoryCreate, db: Session = Depends(get_db)):
    """Create menu category"""
    category = crud_menu.create_menu_category(
        db, 
        category_data.name,
        category_data.description,
        category_data.image_url
    )
    return category

@router.get("/categories/{category_id}", response_model=MenuCategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get menu category"""
    category = crud_menu.get_menu_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{category_id}", response_model=MenuCategoryResponse)
def update_category(category_id: int, category_data: MenuCategoryCreate, db: Session = Depends(get_db)):
    """Update menu category"""
    category = crud_menu.update_menu_category(db, category_id, **category_data.dict())
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete menu category"""
    category = crud_menu.delete_menu_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

# Menu Item Endpoints
@router.get("/items", response_model=List[MenuItemResponse])
def list_items(category_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get menu items, optionally filtered by category"""
    if category_id:
        items = crud_menu.get_menu_items_by_category(db, category_id, skip, limit)
    else:
        items = crud_menu.get_menu_items(db, skip, limit)
    return items

@router.post("/items", response_model=MenuItemResponse)
def create_item(item_data: MenuItemCreate, db: Session = Depends(get_db)):
    """Create menu item"""
    item = crud_menu.create_menu_item(
        db,
        item_data.name,
        item_data.price,
        item_data.cost,
        item_data.category_id,
        item_data.description,
        item_data.image_url,
        item_data.preparation_time
    )
    return item

@router.get("/items/{item_id}", response_model=MenuItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get menu item"""
    item = crud_menu.get_menu_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/items/{item_id}", response_model=MenuItemResponse)
def update_item(item_id: int, item_data: MenuItemCreate, db: Session = Depends(get_db)):
    """Update menu item"""
    item = crud_menu.update_menu_item(db, item_id, **item_data.dict())
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete menu item"""
    item = crud_menu.delete_menu_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

# Table Management
@router.get("/tables", response_model=List[TableResponse])
def list_tables(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tables"""
    tables = crud_order.get_tables(db, skip, limit)
    return tables

@router.post("/tables", response_model=TableResponse)
def create_table(table_data: TableCreate, db: Session = Depends(get_db)):
    """Create table"""
    table = crud_order.create_table(db, table_data.table_number, table_data.capacity)
    return table

@router.get("/tables/{table_id}", response_model=TableResponse)
def get_table(table_id: int, db: Session = Depends(get_db)):
    """Get table"""
    table = crud_order.get_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

@router.put("/tables/{table_id}", response_model=TableResponse)
def update_table(table_id: int, table_data: dict, db: Session = Depends(get_db)):
    """Update table"""
    table = crud_order.update_table(db, table_id, **table_data)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

@router.delete("/tables/{table_id}")
def delete_table(table_id: int, db: Session = Depends(get_db)):
    """Delete table"""
    table = crud_order.delete_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return {"message": "Table deleted successfully"}

# Order Management
@router.get("/orders", response_model=List[OrderResponse])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all orders"""
    orders = crud_order.get_orders(db, skip, limit)
    return orders

@router.post("/orders", response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """Create order"""
    order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    order = crud_order.create_order(
        db, 
        order_number, 
        order_data.order_type,
        order_data.table_id,
        order_data.notes
    )
    
    # Add order items
    for item_data in order_data.items:
        crud_order.create_order_item(
            db,
            order.id,
            item_data.menu_item_id,
            item_data.quantity,
            item_data.unit_price,
            item_data.notes
        )
    
    return order

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order"""
    order = crud_order.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status_update: dict, db: Session = Depends(get_db)):
    """Update order status"""
    order = crud_order.update_order_status(db, order_id, status_update.get("status"))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete order"""
    order = crud_order.delete_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}
