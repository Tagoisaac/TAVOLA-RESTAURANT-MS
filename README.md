# 🍽️ Tavola Restaurant Management System

A comprehensive, full-stack restaurant management system built with **FastAPI** (backend) and **React** (frontend). Manage orders, inventory, staff, payments, and more from a single integrated platform.

## ✨ Features (Phase 1 Complete)

### 🔐 Authentication & Authorization
- User registration and secure login with JWT tokens
- Role-based access control (RBAC) system
- Password hashing with bcrypt
- Session management via localStorage

### 👨‍💼 Admin Module
- User management (create, edit, delete users)
- Role and permission management
- Multi-level access control
- User activation/deactivation

### 🍴 Restaurant Module
- **Menu Management**: Categories and items with pricing
- **Table Management**: Capacity and status tracking
- **Order Management**: Create orders, track status (pending → preparing → served → completed)
- **Order Items**: Track individual items with special instructions

### 💳 Cashier Module
- Invoice generation with automatic calculations
- Multiple payment methods (cash, card, mobile)
- Payment processing and tracking
- Refund handling with order status rollback

### 📦 Inventory Management
- Stock tracking with real-time updates
- Stock movement recording (purchase, consumption, waste, adjustment)
- Low-stock alerts and automatic reorder level warnings
- Multi-unit support (kg, g, liters, pieces, etc.)

## 🏗️ Technology Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Database ORM**: SQLAlchemy 2.0.23
- **Authentication**: JWT + PassLib + bcrypt
- **Data Validation**: Pydantic 2.12.5
- **Server**: Uvicorn 0.27.0
- **Database**: PostgreSQL (optional, dev mode without DB)

### Frontend
- **Framework**: React 18.2.0
- **Routing**: React Router DOM 6.11.0
- **HTTP Client**: Fetch API
- **Build Tool**: Create React App

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- npm or yarn

### 1️⃣ Start Backend Server
```bash
cd "Tavola Restaurant Management System/backend"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Backend will run on: **http://localhost:8000**
- API docs: http://localhost:8000/docs (interactive Swagger UI)
- Alternative docs: http://localhost:8000/redoc

### 2️⃣ Start Frontend Server
```bash
cd "Tavola Restaurant Management System/tavola-frontend"
npm install  # First time only
npm start
```

Frontend will run on: **http://localhost:3000**

### 3️⃣ Test the System
1. Open **http://localhost:3000** in your browser
2. Register a new user account
3. Login with your credentials
4. Explore the dashboard with all 5 modules

## 📚 Documentation

- **[Quick Start Guide](./QUICKSTART.md)** - 5-minute setup and usage guide
- **[Implementation Summary](./IMPLEMENTATION_SUMMARY.md)** - Detailed overview of all features and architecture
- **[API Documentation](./API_DOCUMENTATION.md)** - Complete API endpoint reference with examples
- **[Testing Guide](./TESTING_GUIDE.md)** - Comprehensive testing procedures for all modules

## 📂 Project Structure

```
Tavola Restaurant Management System/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── endpoints/          # API route handlers (5 modules)
│   │   │   │   ├── auth.py         # Authentication endpoints
│   │   │   │   ├── admin.py        # User/Role/Permission management
│   │   │   │   ├── restaurant.py   # Menu, Tables, Orders
│   │   │   │   ├── cashier.py      # Payments and invoices
│   │   │   │   └── inventory.py    # Stock management
│   │   │   └── __init__.py
│   │   ├── crud/                   # Database operations (CRUD)
│   │   │   ├── user.py
│   │   │   ├── menu.py
│   │   │   ├── order.py
│   │   │   └── inventory.py
│   │   ├── schemas/                # Pydantic validation models
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── menu.py
│   │   │   ├── order.py
│   │   │   └── inventory.py
│   │   ├── db/
│   │   │   ├── models/             # SQLAlchemy ORM models
│   │   │   │   ├── base.py
│   │   │   │   ├── user.py
│   │   │   │   ├── menu.py
│   │   │   ├── session.py
│   │   │   └── __init__.py
│   │   └── core/
│   │       ├── config.py           # Configuration settings
│   │       └── security.py         # JWT and auth functions
│   ├── main.py                     # FastAPI app entry point
│   └── requirements.txt
│
├── tavola-frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LoginPage.js        # Login form page
│   │   │   ├── LoginPage.css
│   │   │   ├── Dashboard.js        # Main dashboard (5 tabs)
│   │   │   └── Dashboard.css
│   │   ├── services/
│   │   │   └── api.js              # API service client
│   │   ├── App.js                  # Root component with routing
│   │   ├── App.css
│   │   └── index.js
│   └── package.json
│
├── QUICKSTART.md                   # Quick start guide 👈 START HERE
├── IMPLEMENTATION_SUMMARY.md       # Feature overview
├── API_DOCUMENTATION.md            # Complete API reference
├── TESTING_GUIDE.md               # Testing procedures
└── README.md                       # This file
```

## 🔌 API Endpoints Summary

All endpoints require JWT authentication (except `/auth` endpoints).

### Authentication (Public)
```
POST   /api/v1/auth/register  - Register new user
POST   /api/v1/auth/login     - Login and get JWT token
```

### Admin (16 endpoints)
```
GET    /api/v1/admin/users
POST   /api/v1/admin/users
PUT    /api/v1/admin/users/{id}
DELETE /api/v1/admin/users/{id}
... (roles, permissions, assignments)
```

### Restaurant (24+ endpoints)
```
GET/POST   /api/v1/restaurant/categories       - Menu categories
GET/POST   /api/v1/restaurant/items            - Menu items
GET/POST   /api/v1/restaurant/tables           - Dining tables
GET/POST   /api/v1/restaurant/orders           - Guest orders
PUT        /api/v1/restaurant/orders/{id}/status - Update order status
```

### Cashier (4 endpoints)
```
GET    /api/v1/cashier/orders/{id}/invoice     - Generate invoice
POST   /api/v1/cashier/payments                - Process payment
POST   /api/v1/cashier/payments/{id}/refund    - Refund payment
```

### Inventory (8+ endpoints)
```
GET    /api/v1/inventory/items                     - All items
GET    /api/v1/inventory/items/low-stock           - Low stock alerts
POST   /api/v1/inventory/items                     - Create item
POST   /api/v1/inventory/movements                 - Record stock movement
```

**See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for complete endpoint reference with request/response examples.**

## 🧪 Testing

### Frontend Testing
```bash
# Login at http://localhost:3000
# Create test account: username/password/email/name
# Navigate through 5 dashboard tabs
```

### API Testing
Use the interactive API docs at **http://localhost:8000/docs**

Or test via curl (see [TESTING_GUIDE.md](./TESTING_GUIDE.md) for detailed examples):
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"pass123","full_name":"Test"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'

# Use token for authenticated requests
curl -X GET http://localhost:8000/api/v1/admin/users \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🗄️ Database Setup (Optional)

### Development (Default)
Application runs in dev mode without requiring a database. Tables are created in memory.

### Production with PostgreSQL
1. Set environment variable:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/tavola"
```

2. Or create `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost:5432/tavola
```

3. Restart backend - tables will auto-create

## 🛠️ Configuration

Edit `Tavola Restaurant Management System/backend/app/core/config.py`:

```python
# Database URL
DATABASE_URL = "postgresql://user:password@localhost/tavola"

# JWT Settings
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 8

# CORS Settings
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8080"]
```

## 🚨 Troubleshooting

### Frontend shows blank page
- Check if backend is running on http://localhost:8000
- Open browser console (F12) for error messages
- Verify Node.js and npm are installed: `node -v && npm -v`

### Backend connection refused
- Ensure backend is running: `uvicorn main:app --host 0.0.0.0 --port 8000`
- Check if port 8000 is in use: `lsof -i :8000`

### Port 8000 already in use
```bash
# Kill process using port 8000
lsof -i :8000 -t | xargs kill -9

# Or use different port
uvicorn main:app --port 8001
```

### CORS errors
- Backend CORS is pre-configured for localhost:3000
- If issues persist, check `main.py` app settings

### Database connection error
- Dev mode has graceful fallback (no DB required)
- For PostgreSQL, ensure DATABASE_URL environment variable is set
- Check PostgreSQL is running if using it

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Browser                              │
├─────────────────────────────────────────────────────────────┤
│  React Frontend (http://localhost:3000)                      │
│  ├── LoginPage (Authentication)                              │
│  ├── Dashboard (Multi-tab interface)                         │
│  └── APIService (HTTP Client)                               │
├─────────────────────────────────────────────────────────────┤
│              HTTP/CORS                                       │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Backend (http://localhost:8000)                     │
│  ├── 5 API Modules                                          │
│  │   ├── auth.py (Register/Login)                          │
│  │   ├── admin.py (Users/Roles/Permissions)                │
│  │   ├── restaurant.py (Menu/Tables/Orders)                │
│  │   ├── cashier.py (Payments/Invoices)                    │
│  │   └── inventory.py (Stock/Movements)                    │
│  ├── CRUD Layer (Data Access)                              │
│  ├── Pydantic Schemas (Validation)                         │
│  └── SQLAlchemy Models (Database)                          │
├─────────────────────────────────────────────────────────────┤
│  Optional: PostgreSQL Database                              │
└─────────────────────────────────────────────────────────────┘
```

## 📈 Roadmap (Phase 2+)

- [ ] Mobile POS Application (React Native/Flutter)
- [ ] Advanced reporting and analytics dashboard
- [ ] Customer loyalty and rewards program
- [ ] Multi-branch/multi-location support
- [ ] Third-party integrations (Stripe, PayPal payments)
- [ ] Real-time kitchen display system (KDS)
- [ ] Employee scheduling system
- [ ] Table reservation system with online booking
- [ ] Customer management and feedback
- [ ] Advanced inventory forecasting with AI

## 📝 License

This project is part of the Tavola Restaurant Management System Suite.

## 👥 Support

For issues, feature requests, or questions:
1. Check the documentation files (QUICKSTART.md, API_DOCUMENTATION.md, TESTING_GUIDE.md)
2. Review API docs at http://localhost:8000/docs
3. Check the IMPLEMENTATION_SUMMARY.md for architecture details

## 🎯 Next Steps

1. **First Time?** → Read [QUICKSTART.md](./QUICKSTART.md)
2. **Want to test?** → Follow [TESTING_GUIDE.md](./TESTING_GUIDE.md)
3. **Need API details?** → Check [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
4. **Exploring codebase?** → See [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)

---

**Happy restaurant managing! 🍽️✨**
