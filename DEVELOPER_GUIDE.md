# Developer Guide - Tavola Restaurant Management System

## Table of Contents
1. [Project Architecture](#project-architecture)
2. [Backend Development](#backend-development)
3. [Frontend Development](#frontend-development)
4. [Adding New Features](#adding-new-features)
5. [Code Style & Standards](#code-style--standards)
6. [Debugging & Troubleshooting](#debugging--troubleshooting)

---

## Project Architecture

### Backend Architecture Pattern

The backend follows a **layered architecture** pattern:

```
Request → Router (endpoints/) → CRUD (crud/) → Models (db/models/)
                                    ↓
                              Schemas (schemas/)
                                    ↓
                              Database
                                    ↓
Response
```

**Layers Explained**:

1. **Endpoints Layer** (`app/api/v1/endpoints/`)
   - HTTP routes and request handlers
   - Input validation via Pydantic schemas
   - Response formatting
   - Auth/permission checks

2. **CRUD Layer** (`app/crud/`)
   - Database operations (Create, Read, Update, Delete)
   - Business logic for data operations
   - Query optimization
   - Reusable across endpoints

3. **Models Layer** (`app/db/models/`)
   - SQLAlchemy ORM definitions
   - Database table schemas
   - Relationships between entities
   - Constraints and validations

4. **Schemas Layer** (`app/schemas/`)
   - Pydantic models for request/response validation
   - Type hints for IDE support
   - Data serialization

### Frontend Architecture Pattern

The frontend uses **component-based architecture**:

```
App.js (Root)
├── Routing Layer (React Router)
├── Page Components (LoginPage, Dashboard)
├── Service Layer (api.js)
└── Terminal Service (HTTP API calls)
```

---

## Backend Development

### Creating a New API Module

Follow these steps to add a new module (e.g., "Reports"):

#### Step 1: Create Schema File
**File**: `backend/app/schemas/reports.py`

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReportBase(BaseModel):
    title: str
    description: Optional[str] = None

class ReportCreate(ReportBase):
    pass

class ReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ReportResponse(ReportBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

#### Step 2: Create Database Model
**File**: `backend/app/db/models/report.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .base import Base

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
```

Add to `backend/app/db/models/__init__.py`:
```python
from .report import Report
```

#### Step 3: Create CRUD Operations
**File**: `backend/app/crud/reports.py`

```python
from sqlalchemy.orm import Session
from app.db.models.report import Report
from app.schemas.reports import ReportCreate, ReportUpdate

def get_reports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Report).offset(skip).limit(limit).all()

def get_report(db: Session, report_id: int):
    return db.query(Report).filter(Report.id == report_id).first()

def create_report(db: Session, report: ReportCreate):
    db_report = Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

def update_report(db: Session, report_id: int, report: ReportUpdate):
    db_report = get_report(db, report_id)
    if not db_report:
        return None
    for key, value in report.dict(exclude_unset=True).items():
        setattr(db_report, key, value)
    db.commit()
    db.refresh(db_report)
    return db_report

def delete_report(db: Session, report_id: int):
    db_report = get_report(db, report_id)
    if db_report:
        db.delete(db_report)
        db.commit()
    return db_report
```

#### Step 4: Create API Endpoints
**File**: `backend/app/api/v1/endpoints/reports.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import reports as crud_reports
from app.schemas.reports import ReportCreate, ReportUpdate, ReportResponse

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/", response_model=list[ReportResponse])
def list_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all reports"""
    return crud_reports.get_reports(db, skip, limit)

@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get a specific report"""
    report = crud_reports.get_report(db, report_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@router.post("/", response_model=ReportResponse)
def create_report(report: ReportCreate, db: Session = Depends(get_db)):
    """Create a new report"""
    return crud_reports.create_report(db, report)

@router.put("/{report_id}", response_model=ReportResponse)
def update_report(report_id: int, report: ReportUpdate, db: Session = Depends(get_db)):
    """Update a report"""
    updated = crud_reports.update_report(db, report_id, report)
    if not updated:
        raise HTTPException(status_code=404, detail="Report not found")
    return updated

@router.delete("/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    """Delete a report"""
    deleted = crud_reports.delete_report(db, report_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"deleted": True}
```

#### Step 5: Register in API Router
**File**: `backend/app/api/v1/__init__.py`

Add import:
```python
from app.api.v1.endpoints.reports import router as reports_router
```

Register router:
```python
api_router.include_router(reports_router)
```

#### Step 6: Update Database Models __init__.py

**File**: `backend/app/db/__init__.py`

```python
from app.db.models.base import Base
from app.db.models.user import User, Role, Permission
from app.db.models.menu import MenuCategory, MenuItem
from app.db.models.order import Table, Order, OrderItem, Payment
from app.db.models.report import Report

__all__ = [
    "Base",
    "User",
    "Role",
    "Permission",
    "MenuCategory",
    "MenuItem",
    "Table",
    "Order",
    "OrderItem",
    "Payment",
    "Report",
]
```

### Backend Best Practices

1. **Error Handling**
   ```python
   try:
       result = crud_function(db)
   except SQLAlchemyError as e:
       raise HTTPException(status_code=500, detail="Database error")
   ```

2. **Input Validation**
   ```python
   # Pydantic handles this automatically
   class ItemCreate(BaseModel):
       price: float  # Will validate as numeric
       name: str     # Will validate as string
   ```

3. **Database Transactions**
   ```python
   db.begin()
   try:
       # Multiple operations
       db.commit()
   except:
       db.rollback()
       raise
   ```

4. **Type Hints**
   ```python
   def get_user(db: Session, user_id: int) -> Optional[User]:
       """Always include type hints for better IDE support"""
       return db.query(User).filter(User.id == user_id).first()
   ```

---

## Frontend Development

### Adding a New Dashboard Tab

#### Step 1: Create Component Page
**File**: `frontend/src/pages/ReportsPage.js`

```javascript
import React, { useState, useEffect } from 'react';
import APIService from '../services/api';

const ReportsPage = () => {
  const [reports, setReports] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      setIsLoading(true);
      const data = await APIService.getReports();
      setReports(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      setReports([]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="reports-page">
      <h2>Reports</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      {isLoading ? (
        <p>Loading reports...</p>
      ) : (
        <table className="reports-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Description</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {reports.map(report => (
              <tr key={report.id}>
                <td>{report.id}</td>
                <td>{report.title}</td>
                <td>{report.description}</td>
                <td>{new Date(report.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ReportsPage;
```

#### Step 2: Create Component Styles
**File**: `frontend/src/pages/ReportsPage.css`

```css
.reports-page {
  padding: 20px;
}

.reports-page h2 {
  margin-bottom: 20px;
  color: #333;
}

.reports-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.reports-table th,
.reports-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.reports-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.reports-table tr:hover {
  background-color: #f9f9f9;
}

.error-message {
  color: #d32f2f;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
}
```

#### Step 3: Add to APIService
**File**: `frontend/src/services/api.js`

Add method to APIService class:
```javascript
async getReports() {
  const response = await fetch(`${this.baseURL}/reports`, {
    method: 'GET',
    headers: this.getAuthHeaders(),
  });
  if (!response.ok) throw new Error('Failed to fetch reports');
  return await response.json();
}

async createReport(title, description) {
  const response = await fetch(`${this.baseURL}/reports`, {
    method: 'POST',
    headers: this.getAuthHeaders(),
    body: JSON.stringify({ title, description }),
  });
  if (!response.ok) throw new Error('Failed to create report');
  return await response.json();
}
```

#### Step 4: Integrate into Dashboard
**File**: `frontend/src/pages/Dashboard.js`

Import:
```javascript
import ReportsPage from './ReportsPage';
```

Update state:
```javascript
const [activeTab, setActiveTab] = useState('orders'); // Change to 'reports' if default

// Destructure data fetching
const [reports, setReports] = useState([]);
```

Add tab button:
```javascript
<button 
  className={activeTab === 'reports' ? 'active' : ''} 
  onClick={() => setActiveTab('reports')}
>
  Reports
</button>
```

Add tab content:
```javascript
{!isLoading && activeTab === 'reports' && (
  <ReportsPage />
)}
```

### Frontend Best Practices

1. **Error Handling**
   ```javascript
   try {
     const data = await APIService.method();
     setState(data);
   } catch (error) {
     console.error('Error:', error);
     setError(error.message);
   }
   ```

2. **Loading States**
   ```javascript
   const [isLoading, setIsLoading] = useState(true);
   
   if (isLoading) return <div>Loading...</div>;
   ```

3. **Token Management**
   ```javascript
   // Automatically handled by APIService
   const token = localStorage.getItem('token');
   headers['Authorization'] = `Bearer ${token}`;
   ```

4. **Component Organization**
   ```
   Each page component should:
   - Have its own CSS file
   - Use descriptive names
   - Handle loading states
   - Handle error states
   - Not exceed 200 lines (break into sub-components if needed)
   ```

---

## Adding New Features

### Feature: Add Email Notifications

#### Backend Changes

1. Create schema:
```python
# app/schemas/email.py
class EmailSchema(BaseModel):
    recipient: str
    subject: str
    body: str
```

2. Create service:
```python
# app/services/email.py
import smtplib
from email.mime.text import MIMEText

def send_email(recipient: str, subject: str, body: str):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "noreply@tavola.com"
    msg['To'] = recipient
    # Configure SMTP and send
```

3. Use in CRUD:
```python
# In crud/order.py
from app.services.email import send_email

def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    # Send confirmation email
    send_email(user.email, "Order Confirmed", f"Your order {db_order.order_number} is confirmed")
    return db_order
```

#### Frontend Changes

No changes needed - email is sent server-side automatically.

---

## Code Style & Standards

### Python Code Style (Backend)

- Use **snake_case** for variables and functions
- Use **PascalCase** for class names
- Maximum line length: 88 characters
- Use type hints for all functions
- Use docstrings for all modules, classes, functions

Example:
```python
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get a user by their email address.
    
    Args:
        db: Database session
        email: User email to search for
        
    Returns:
        User object if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()
```

### JavaScript Code Style (Frontend)

- Use **camelCase** for variables and functions
- Use **PascalCase** for component names
- Use arrow functions: `() => {}`
- Use const unless reassignment needed
- Add comments for complex logic

Example:
```javascript
const getUserData = async (userId) => {
  // Fetch user from API
  const response = await fetch(`/api/users/${userId}`);
  return response.json();
};
```

---

## Debugging & Troubleshooting

### Backend Debugging

#### 1. Enable Debug Logging
```python
# In main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### 2. Use Print Debugging
```python
# In endpoint
print(f"Received request: {request.json()}")
```

#### 3. Check Database State
```python
# In CRUD
user = db.query(User).all()
print([u.username for u in user])
```

#### 4. Use FastAPI Debug Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Debugging

#### 1. Browser Console
Press `F12` → Console tab to see errors

#### 2. React DevTools
Install React DevTools extension for Chrome/Firefox

#### 3. Network Inspection
Press `F12` → Network tab to inspect API calls

#### 4. Breakpoints
Press `F12` → Sources tab, click line number to set breakpoint

### Common Issues

**Issue**: "CORS error: No 'Access-Control-Allow-Origin' header"
- **Solution**: Check CORS configuration in `main.py`

**Issue**: "401 Unauthorized on authenticated request"
- **Solution**: Verify token in localStorage, check token expiry

**Issue**: "Database connection failed"
- **Solution**: Check DATABASE_URL environment variable

**Issue**: "Module not found" in Python
- **Solution**: Ensure all imports use relative paths starting with `app.`

---

## Testing New Features

### Backend Testing Template

```python
# test_new_feature.py
import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

def test_create_item():
    response = client.post(
        "/api/v1/resource/",
        json={"name": "test", "value": 123},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "test"

def test_list_items():
    response = client.get(
        "/api/v1/resource/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### Frontend Testing Template

```javascript
// ReportsPage.test.js
import { render, screen, waitFor } from '@testing-library/react';
import ReportsPage from './ReportsPage';
import APIService from '../services/api';

jest.mock('../services/api');

test('renders reports list', async () => {
  APIService.getReports.mockResolvedValue([
    { id: 1, title: 'Test Report', description: 'Test' }
  ]);

  render(<ReportsPage />);
  
  await waitFor(() => {
    expect(screen.getByText('Test Report')).toBeInTheDocument();
  });
});
```

---

## Performance Optimization

### Backend Optimization

1. **Database Indexing**
```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)  # Good for lookups
```

2. **Query Optimization**
```python
# Use select() for specific columns
from sqlalchemy import select

users = db.execute(
    select(User.id, User.email).where(User.is_active == True)
).fetchall()
```

3. **Caching** (if needed)
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_categories(db: Session):
    return db.query(MenuCategory).all()
```

### Frontend Optimization

1. **Memoization**
```javascript
import React, { useMemo } from 'react';

const Component = ({ data }) => {
  const processedData = useMemo(() => {
    return expensiveCalculation(data);
  }, [data]);
};
```

2. **Code Splitting** (if app grows)
```javascript
import { lazy, Suspense } from 'react';

const ReportsPage = lazy(() => import('./pages/ReportsPage'));

<Suspense fallback={<div>Loading...</div>}>
  <ReportsPage />
</Suspense>
```

---

## Deployment Checklist

- [ ] Backend: All print statements removed, logging configured
- [ ] Frontend: Environment variables set for prod API URL
- [ ] Database: PostgreSQL configured and migrations run
- [ ] Security: SECRET_KEY changed from default
- [ ] Security: CORS whitelist configured
- [ ] Testing: All endpoints tested manually
- [ ] Documentation: Updated API docs
- [ ] Performance: Database indexed properly

---

**Last Updated**: February 2024
**Version**: 1.0.0
