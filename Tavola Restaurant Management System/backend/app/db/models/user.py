from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import BaseModel

# Association table for many-to-many relationship between Role and Permission
role_permission = Table(
    'role_permission',
    BaseModel.metadata,
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('permission_id', Integer, ForeignKey('permission.id'))
)

class Permission(BaseModel):
    __tablename__ = "permission"
    
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    
    # Relationships
    roles = relationship("Role", secondary=role_permission, back_populates="permissions")

class Role(BaseModel):
    __tablename__ = "role"
    
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    
    # Relationships
    permissions = relationship("Permission", secondary=role_permission, back_populates="roles")
    users = relationship("User", back_populates="role")

class User(BaseModel):
    __tablename__ = "user"
    
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean(), default=True)
    last_login = Column(DateTime, nullable=True)
    
    # Foreign Keys
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    
    # Relationships
    role = relationship("Role", back_populates="users")
    
    def __repr__(self):
        return f"<User {self.username}>"

class Employee(BaseModel):
    __tablename__ = "employee"
    
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    phone = Column(String)
    address = Column(String)
    hire_date = Column(DateTime, default=datetime.utcnow)
    position = Column(String)
    salary = Column(Integer, nullable=True)
    
    # Relationships
    user = relationship("User", backref="employee_profile")
    attendances = relationship("Attendance", back_populates="employee")
    leaves = relationship("Leave", back_populates="employee")

class Attendance(BaseModel):
    __tablename__ = "attendance"
    
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    check_in = Column(DateTime, default=datetime.utcnow)
    check_out = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)
    
    # Relationships
    employee = relationship("Employee", back_populates="attendances")

class Leave(BaseModel):
    __tablename__ = "leave"
    
    employee_id = Column(Integer, ForeignKey("employee.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, approved, rejected
    
    # Relationships
    employee = relationship("Employee", back_populates="leaves")
