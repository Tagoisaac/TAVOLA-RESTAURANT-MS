from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.menu import MenuCategoryResponse, MenuCategoryCreate, MenuItemResponse, MenuItemCreate
from app.schemas.order import TableResponse, TableCreate, OrderResponse, OrderCreate, OrderStatusUpdate
from app.crud import menu as crud_menu
from app.crud import order as crud_order

router = APIRouter(prefix="/restaurant", tags=["restaurant"])

# Menu Category endpoints
@router.get("/categories", response_model=list[MenuCategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """List all menu categories"""
    return crud_menu.get_categories(db)

@router.post("/categories", response_model=MenuCategoryResponse)
def create_category(category: MenuCategoryCreate, db: Session = Depends(get_db)):
    """Create a new menu category"""
    return crud_menu.create_category(db, category)

@router.get("/categories/{category_id}", response_model=MenuCategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific menu category"""
    category = crud_menu.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/categories/{category_id}", response_model=MenuCategoryResponse)
def update_category(category_id: int, category: MenuCategoryCreate, db: Session = Depends(get_db)):
    """Update a menu category"""
    updated = crud_menu.update_category(db, category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a menu category"""
    deleted = crud_menu.delete_category(db, category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"deleted": True}

# Menu Item endpoints
@router.get("/items", response_model=list[MenuItemResponse])
def list_items(category_id: int = None, db: Session = Depends(get_db)):
    """List all menu items"""
    return crud_menu.get_items(db, category_id)

@router.post("/items", response_model=MenuItemResponse)
def create_item(item: MenuItemCreate, db: Session = Depends(get_db)):
    """Create a new menu item"""
    return crud_menu.create_item(db, item)

@router.get("/items/{item_id}", response_model=MenuItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific menu item"""
    item = crud_menu.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/items/{item_id}", response_model=MenuItemResponse)
def update_item(item_id: int, item: MenuItemCreate, db: Session = Depends(get_db)):
    """Update a menu item"""
    updated = crud_menu.update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a menu item"""
    deleted = crud_menu.delete_item(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"deleted": True}

# Table endpoints
@router.get("/tables", response_model=list[TableResponse])
def list_tables(db: Session = Depends(get_db)):
    """List all tables"""
    return crud_order.get_tables(db)

@router.post("/tables", response_model=TableResponse)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    """Create a new table"""
    return crud_order.create_table(db, table)

@router.get("/tables/{table_id}", response_model=TableResponse)
def get_table(table_id: int, db: Session = Depends(get_db)):
    """Get a specific table"""
    table = crud_order.get_table(db, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    return table

# Order endpoints
@router.get("/orders", response_model=list[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    """List all orders"""
    orders = crud_order.get_orders(db)
    return orders

@router.post("/orders", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order"""
    return crud_order.create_order(db, order)

@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order"""
    order = crud_order.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status_update: OrderStatusUpdate, db: Session = Depends(get_db)):
    """Update order status"""
    updated = crud_order.update_order_status(db, order_id, status_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated
