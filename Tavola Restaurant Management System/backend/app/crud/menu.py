from sqlalchemy.orm import Session
from app.db.models.menu import MenuCategory, MenuItem
from app.schemas.menu import MenuCategoryCreate, MenuItemCreate

def get_categories(db: Session):
    return db.query(MenuCategory).all()

def get_category(db: Session, category_id: int):
    return db.query(MenuCategory).filter(MenuCategory.id == category_id).first()

def create_category(db: Session, category: MenuCategoryCreate):
    db_category = MenuCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: MenuCategoryCreate):
    db_category = get_category(db, category_id)
    if db_category:
        for key, value in category.dict().items():
            setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

def get_items(db: Session, category_id: int = None):
    query = db.query(MenuItem)
    if category_id:
        query = query.filter(MenuItem.category_id == category_id)
    return query.all()

def get_item(db: Session, item_id: int):
    return db.query(MenuItem).filter(MenuItem.id == item_id).first()

def create_item(db: Session, item: MenuItemCreate):
    db_item = MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: MenuItemCreate):
    db_item = get_item(db, item_id)
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
