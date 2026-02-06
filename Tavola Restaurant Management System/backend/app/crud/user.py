from sqlalchemy.orm import Session
from app.db.models.user import User, Role, Permission
from app.schemas.user import UserCreate, UserUpdate, RoleCreate, PermissionCreate
from app.core.security import get_password_hash, verify_password

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_roles(db: Session):
    return db.query(Role).all()

def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()

def create_role(db: Session, role: RoleCreate):
    db_role = Role(
        name=role.name,
        description=role.description,
    )
    db.add(db_role)
    db.commit()
    
    # Assign permissions if provided
    for perm_id in role.permission_ids:
        permission = db.query(Permission).filter(Permission.id == perm_id).first()
        if permission:
            db_role.permissions.append(permission)
    
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role: RoleCreate):
    db_role = get_role(db, role_id)
    if db_role:
        db_role.name = role.name
        db_role.description = role.description
        db.commit()
        db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int):
    db_role = get_role(db, role_id)
    if db_role:
        db.delete(db_role)
        db.commit()
    return db_role

def get_permissions(db: Session):
    return db.query(Permission).all()

def get_permission(db: Session, permission_id: int):
    return db.query(Permission).filter(Permission.id == permission_id).first()

def create_permission(db: Session, permission: PermissionCreate):
    db_permission = Permission(
        code=permission.code,
        description=permission.description,
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def delete_permission(db: Session, permission_id: int):
    db_permission = get_permission(db, permission_id)
    if db_permission:
        db.delete(db_permission)
        db.commit()
    return db_permission

def assign_permission_to_role(db: Session, role_id: int, permission_id: int):
    role = get_role(db, role_id)
    permission = get_permission(db, permission_id)
    
    if role and permission:
        if permission not in role.permissions:
            role.permissions.append(permission)
            db.commit()
        return role
    return None
