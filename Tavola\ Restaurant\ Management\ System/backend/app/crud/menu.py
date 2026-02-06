from sqlalchemy.orm import Session
from app.db import models
from typing import Optional

# MenuCategory CRUD
def get_menu_category(db: Session, category_id: int):
    return db.query(models.MenuCategory).filter(models.MenuCategory.id == category_id).first()

def get_menu_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MenuCategory).offset(skip).limit(limit).all()

def create_menu_category(db: Session, name: str, description: Optional[str] = None, image_url: Optional[str] = None):
    db_category = models.MenuCategory(name=name, description=description, image_url=image_url)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_menu_category(db: Session, category_id: int, **kwargs):
    category = get_menu_category(db, category_id)
    if category:
        for key, value in kwargs.items():
            if value is not None:
                setattr(category, key, value)
        db.commit()
        db.refresh(category)
    return category

def delete_menu_category(db: Session, category_id: int):
    category = get_menu_category(db, category_id)
    if category:
        db.delete(category)
        db.commit()
    return category

# MenuItem CRUD
def get_menu_item(db: Session, item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()

def get_menu_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MenuItem).offset(skip).limit(limit).all()

def get_menu_items_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.MenuItem).filter(models.MenuItem.category_id == category_id).offset(skip).limit(limit).all()

def create_menu_item(db: Session, name: str, price: float, cost: float, category_id: int, 
                    description: Optional[str] = None, image_url: Optional[str] = None, 
                    preparation_time: Optional[int] = None):
    db_item = models.MenuItem(
        name=name,
        price=price,
        cost=cost,
        category_id=category_id,
        description=description,
        image_url=image_url,
        preparation_time=preparation_time
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_menu_item(db: Session, item_id: int, **kwargs):
    item = get_menu_item(db, item_id)
    if item:
        for key, value in kwargs.items():
            if value is not None:
                setattr(item, key, value)
        db.commit()
        db.refresh(item)
    return item

def delete_menu_item(db: Session, item_id: int):
    item = get_menu_item(db, item_id)
    if item:
        db.delete(item)
        db.commit()
    return item
