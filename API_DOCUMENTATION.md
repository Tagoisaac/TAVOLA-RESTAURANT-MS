# Tavola Restaurant Management System - API Endpoints

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication Endpoints

### Register New User
- **POST** `/auth/register`
- **Body**: 
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "full_name": "string"
  }
  ```

### Login
- **POST** `/auth/login`
- **Body**: 
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

## Admin Module Endpoints

### Users
- **GET** `/admin/users` - List all users
- **POST** `/admin/users` - Create new user
- **GET** `/admin/users/{user_id}` - Get user details
- **PUT** `/admin/users/{user_id}` - Update user
- **DELETE** `/admin/users/{user_id}` - Delete user

### Roles
- **GET** `/admin/roles` - List all roles
- **POST** `/admin/roles` - Create new role
- **GET** `/admin/roles/{role_id}` - Get role details
- **PUT** `/admin/roles/{role_id}` - Update role
- **DELETE** `/admin/roles/{role_id}` - Delete role

### Permissions
- **GET** `/admin/permissions` - List all permissions
- **POST** `/admin/permissions` - Create new permission
- **DELETE** `/admin/permissions/{permission_id}` - Delete permission

### Role-Permission Assignment
- **POST** `/admin/roles/{role_id}/permissions/{permission_id}` - Assign permission to role
- **DELETE** `/admin/roles/{role_id}/permissions/{permission_id}` - Remove permission from role

## Restaurant Module Endpoints

### Menu Categories
- **GET** `/restaurant/categories` - List all categories
- **POST** `/restaurant/categories` - Create category
- **GET** `/restaurant/categories/{category_id}` - Get category details
- **PUT** `/restaurant/categories/{category_id}` - Update category
- **DELETE** `/restaurant/categories/{category_id}` - Delete category

### Menu Items
- **GET** `/restaurant/items` - List all menu items
- **GET** `/restaurant/items?category_id={id}` - Get items by category
- **POST** `/restaurant/items` - Create menu item
- **GET** `/restaurant/items/{item_id}` - Get menu item details
- **PUT** `/restaurant/items/{item_id}` - Update menu item
- **DELETE** `/restaurant/items/{item_id}` - Delete menu item

### Tables
- **GET** `/restaurant/tables` - List all tables
- **POST** `/restaurant/tables` - Create table
- **GET** `/restaurant/tables/{table_id}` - Get table details
- **PUT** `/restaurant/tables/{table_id}` - Update table
- **DELETE** `/restaurant/tables/{table_id}` - Delete table

### Orders
- **GET** `/restaurant/orders` - List all orders
- **POST** `/restaurant/orders` - Create order
- **GET** `/restaurant/orders/{order_id}` - Get order details
- **PUT** `/restaurant/orders/{order_id}/status` - Update order status
- **DELETE** `/restaurant/orders/{order_id}` - Delete order

## Cashier Module Endpoints

### Invoices
- **GET** `/cashier/orders/{order_id}/invoice` - Get invoice for order

### Payments
- **POST** `/cashier/payments` - Process payment
- **GET** `/cashier/payments/{payment_id}` - Get payment details
- **GET** `/cashier/orders/{order_id}/payments` - Get all payments for order
- **POST** `/cashier/payments/{payment_id}/refund` - Refund payment

## Inventory Module Endpoints

### Inventory Items
- **GET** `/inventory/items` - List all inventory items
- **POST** `/inventory/items` - Create inventory item
- **GET** `/inventory/items/{item_id}` - Get inventory item details
- **PUT** `/inventory/items/{item_id}` - Update inventory item
- **DELETE** `/inventory/items/{item_id}` - Delete inventory item

### Stock Movements
- **POST** `/inventory/movements` - Record stock movement
- **GET** `/inventory/movements` - List stock movements
- **GET** `/inventory/movements?ingredient_id={id}` - Get movements by ingredient

### Stock Alerts
- **GET** `/inventory/low-stock` - Get items below minimum stock level

## Frontend Pages

### Login Page
- **Route**: `/`
- **Features**: User login form, redirect to dashboard on success

### Dashboard
- **Route**: `/dashboard`
- **Features**: 
  - Orders management and tracking
  - Menu item browsing and management
  - User management
  - Inventory tracking with low stock alerts

## Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (optional in dev mode)
- **Authentication**: JWT tokens
- **ORM**: SQLAlchemy

### Frontend
- **Framework**: React 18
- **Routing**: React Router v6
- **HTTP Client**: Fetch API

## Running the Application

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd tavola-frontend
npm install
npm start
```

## API Documentation
Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
