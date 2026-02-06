from sqlalchemy.orm import Session
from app.db import models
from app.core.security import get_password_hash, verify_password
from typing import Optional

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, username: str, email: str, password: str, full_name: str, role_id: int):
    hashed_password = get_password_hash(password)
    db_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        role_id=role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, **kwargs):
    user = get_user(db, user_id)
    if user:
        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# Role CRUD
def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()

def create_role(db: Session, name: str, description: Optional[str] = None):
    db_role = models.Role(name=name, description=description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, name: Optional[str] = None, description: Optional[str] = None):
    role = get_role(db, role_id)
    if role:
        if name:
            role.name = name
        if description:
            role.description = description
        db.commit()
        db.refresh(role)
    return role

def delete_role(db: Session, role_id: int):
    role = get_role(db, role_id)
    if role:
        db.delete(role)
        db.commit()
    return role

# Permission CRUD
def get_permission(db: Session, permission_id: int):
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()

def get_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Permission).offset(skip).limit(limit).all()

def create_permission(db: Session, name: str, description: Optional[str] = None):
    db_permission = models.Permission(name=name, description=description)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def delete_permission(db: Session, permission_id: int):
    permission = get_permission(db, permission_id)
    if permission:
        db.delete(permission)
        db.commit()
    return permission

# Role-Permission Association
def assign_permission_to_role(db: Session, role_id: int, permission_id: int):
    role = get_role(db, role_id)
    permission = get_permission(db, permission_id)
    if role and permission:
        if permission not in role.permissions:
            role.permissions.append(permission)
            db.commit()
    return role

def remove_permission_from_role(db: Session, role_id: int, permission_id: int):
    role = get_role(db, role_id)
    permission = get_permission(db, permission_id)
    if role and permission and permission in role.permissions:
        role.permissions.remove(permission)
        db.commit()
    return role
