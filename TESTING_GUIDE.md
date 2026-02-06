# Tavola Restaurant Management System - Testing Guide

## System Verification Checklist

Use this guide to verify all modules are working correctly.

---

## Part 1: System Health Check

### Check Backend is Running
```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{"status": "healthy"}
```

### Check Frontend is Running
```bash
curl http://localhost:3000/
```

**Expected**: Returns HTML page with "Tavola" branding

### Check API Documentation Available
🔗 Open http://localhost:8000/docs in browser
- Should show interactive Swagger UI
- All 5 modules visible in left sidebar

---

## Part 2: Authentication Module Testing

### Test 1.1: User Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testadmin",
    "email": "testadmin@tavola.com",
    "password": "SecurePass123!",
    "full_name": "Test Admin User"
  }'
```

**Expected Response**:
```json
{
  "id": 1,
  "username": "testadmin",
  "email": "testadmin@tavola.com",
  "full_name": "Test Admin User",
  "is_active": true,
  "created_at": "2024-02-06T..."
}
```

### Test 1.2: User Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testadmin",
    "password": "SecurePass123!"
  }'
```

**Expected Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

**Save the token**: You'll need it for authenticated requests below. Store in a variable:
```bash
TOKEN="your_access_token_here"
```

### Test 1.3: Frontend Login
1. Open http://localhost:3000
2. Click "Register" tab
3. Enter:
   - Username: `testfrontend`
   - Email: `testfrontend@tavola.com`
   - Password: `Password123!`
   - Full Name: `Frontend Test`
4. Click "Register"
5. Should redirect to login page
6. Login with same credentials
7. **Expected**: Dashboard page loads with sidebar menu
8. Check browser console (F12 → Console) - should see no errors
9. Check localStorage: Open DevTools → Application → LocalStorage → http://localhost:3000
   - Should see key `token` with JWT value

---

## Part 3: Admin Module Testing

### Test 3.1: List All Users
```bash
curl -X GET http://localhost:8000/api/v1/admin/users \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response**: Array of user objects including the registered test user(s)

### Test 3.2: Get Specific User
```bash
curl -X GET http://localhost:8000/api/v1/admin/users/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response**: User object with id=1

### Test 3.3: Create Role
```bash
curl -X POST http://localhost:8000/api/v1/admin/roles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Kitchen Manager",
    "description": "Manages kitchen operations",
    "permission_ids": []
  }'
```

**Expected Response**:
```json
{
  "id": 2,
  "name": "Kitchen Manager",
  "description": "Manages kitchen operations",
  "permissions": []
}
```

### Test 3.4: Create Permission
```bash
curl -X POST http://localhost:8000/api/v1/admin/permissions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "code": "order.create",
    "description": "Can create orders"
  }'
```

**Expected Response**:
```json
{
  "id": 1,
  "code": "order.create",
  "description": "Can create orders"
}
```

### Test 3.5: Assign Permission to Role
```bash
curl -X POST http://localhost:8000/api/v1/admin/roles/2/permissions/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**: 200 OK response

### Test 3.6: Update User
```bash
curl -X PUT http://localhost:8000/api/v1/admin/users/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "username": "testadmin",
    "full_name": "Updated Admin User",
    "is_active": true
  }'
```

**Expected**: User object with updated full_name

---

## Part 4: Restaurant Module Testing

### Test 4.1: Create Menu Category
```bash
curl -X POST http://localhost:8000/api/v1/restaurant/categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Appetizers",
    "description": "Starters and appetizers",
    "is_active": true
  }'
```

**Expected Response**:
```json
{
  "id": 1,
  "name": "Appetizers",
  "description": "Starters and appetizers",
  "is_active": true
}
```

### Test 4.2: Get Menu Categories
```bash
curl -X GET http://localhost:8000/api/v1/restaurant/categories \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**: Array with the category created above

### Test 4.3: Create Menu Item
```bash
curl -X POST http://localhost:8000/api/v1/restaurant/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Bruschetta",
    "description": "Grilled bread with tomatoes and basil",
    "category_id": 1,
    "price": 8.50,
    "cost": 2.50,
    "is_available": true
  }'
```

**Expected Response**:
```json
{
  "id": 1,
  "name": "Bruschetta",
  "description": "Grilled bread with tomatoes and basil",
  "category_id": 1,
  "price": 8.50,
  "cost": 2.50,
  "is_available": true
}
```

### Test 4.4: Get Menu Items
```bash
curl -X GET http://localhost:8000/api/v1/restaurant/items \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**: Array with menu items created

### Test 4.5: Create Table
```bash
curl -X POST http://localhost:8000/api/v1/restaurant/tables \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "table_number": 1,
    "capacity": 4,
    "location": "Main Dining Area"
  }'
```

**Expected Response**:
```json
{
  "id": 1,
  "table_number": 1,
  "capacity": 4,
  "location": "Main Dining Area",
  "status": "available"
}
```

### Test 4.6: Create Order
```bash
curl -X POST http://localhost:8000/api/v1/restaurant/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "table_id": 1,
    "order_type": "dine_in",
    "items": [
      {
        "menu_item_id": 1,
        "quantity": 2,
        "special_instructions": "extra basil"
      }
    ]
  }'
```

**Expected Response**:
```json
{
  "id": 1,
  "order_number": "ORD-ABC123DE",
  "table_id": 1,
  "order_type": "dine_in",
  "status": "pending",
  "items": [...],
  "total_amount": 17.00,
  "created_at": "2024-02-06T..."
}
```

### Test 4.7: Update Order Status
```bash
curl -X PUT http://localhost:8000/api/v1/restaurant/orders/1/status \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "preparing"
  }'
```

**Expected**: Order object with status="preparing"

### Test 4.8: Get Order Details
```bash
curl -X GET http://localhost:8000/api/v1/restaurant/orders/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**: Complete order object with all items

---

## Part 5: Cashier Module Testing

### Test 5.1: Generate Invoice
```bash
curl -X GET http://localhost:8000/api/v1/cashier/orders/1/invoice \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response**:
```json
{
  "order_id": 1,
  "order_number": "ORD-ABC123DE",
  "items": [...],
  "subtotal": 17.00,
  "tax_amount": 1.70,
  "total_amount": 18.70
}
```

### Test 5.2: Process Payment
```bash
curl -X POST http://localhost:8000/api/v1/cashier/payments \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "order_id": 1,
    "amount": 18.70,
    "payment_method": "card",
    "transaction_id": "TXN-20240206-001"
  }'
```

**Expected Response**:
```json
{
  "id": 1,
  "order_id": 1,
  "amount": 18.70,
  "payment_method": "card",
  "status": "completed",
  "transaction_id": "TXN-20240206-001",
  "created_at": "2024-02-06T..."
}
```

### Test 5.3: Process Refund
```bash
curl -X POST http://localhost:8000/api/v1/cashier/payments/1/refund \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**: Payment object with status="refunded"

---

## Part 6: Inventory Module Testing

### Test 6.1: Create Inventory Item
```bash
curl -X POST http://localhost:8000/api/v1/inventory/items \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Tomatoes",
    "unit": "kg",
    "current_stock": 50.0,
    "min_stock_level": 10.0,
    "reorder_level": 20.0,
    "supplier_id": null
  }'
```

**Expected Response**:
```json
{
  "id": 1,
  "name": "Tomatoes",
  "unit": "kg",
  "current_stock": 50.0,
  "min_stock_level": 10.0,
  "reorder_level": 20.0
}
```

### Test 6.2: Get Inventory Items
```bash
curl -X GET http://localhost:8000/api/v1/inventory/items \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**: Array with inventory items

### Test 6.3: Record Stock Movement (Consumption)
```bash
curl -X POST http://localhost:8000/api/v1/inventory/movements \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "ingredient_id": 1,
    "quantity": -5.0,
    "movement_type": "consumption",
    "notes": "Used in menu items"
  }'
```

**Expected Response**:
```json
{
  "id": 1,
  "ingredient_id": 1,
  "quantity": -5.0,
  "movement_type": "consumption",
  "notes": "Used in menu items",
  "created_at": "2024-02-06T..."
}
```

**Note**: This should update ingredient current_stock to 45.0

### Test 6.4: Get Low Stock Items
```bash
curl -X GET http://localhost:8000/api/v1/inventory/items/low-stock \
  -H "Authorization: Bearer $TOKEN"
```

**Expected**: Array of items where current_stock < reorder_level

### Test 6.5: Update Inventory Item
```bash
curl -X PUT http://localhost:8000/api/v1/inventory/items/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Tomatoes (Fresh)",
    "current_stock": 45.0,
    "min_stock_level": 10.0,
    "reorder_level": 20.0
  }'
```

**Expected**: Updated inventory item

---

## Part 7: Frontend Dashboard Testing

### Access Dashboard
1. Open http://localhost:3000 (should redirect to /dashboard if logged in)
2. Or manually navigate to http://localhost:3000/dashboard

### Test 7.1: Orders Tab
- **Expected**: Table showing orders
- Create a few orders first (via API tests above)
- Should display order_number, status, total_amount
- Verify data matches API responses

### Test 7.2: Menu Tab
- Should display menu items in grid format
- Show category, name, price
- Verify data matches API responses

### Test 7.3: Users Tab
- Should display user table with username, email, full_name
- Verify data matches API responses

### Test 7.4: Inventory Tab
- Should display inventory items
- Should show a "Low Stock Items" section with alerts
- Verify matching API responses

### Test 7.5: Logout
- Click "Logout" button
- Should redirect to login page
- Token should be removed from localStorage

---

## Part 8: Error Handling Testing

### Test 8.1: Invalid Credentials
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nonexistent",
    "password": "wrongpass"
  }'
```

**Expected**: 401 Unauthorized error

### Test 8.2: Missing Authentication Token
```bash
curl -X GET http://localhost:8000/api/v1/admin/users
```

**Expected**: 403 Forbidden or 401 Unauthorized error

### Test 8.3: Invalid Token
```bash
curl -X GET http://localhost:8000/api/v1/admin/users \
  -H "Authorization: Bearer invalid_token_here"
```

**Expected**: 401 Unauthorized error

### Test 8.4: Duplicate Username Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testadmin",
    "email": "different@email.com",
    "password": "Pass123!",
    "full_name": "Different User"
  }'
```

**Expected**: 400 Bad Request with error message

### Test 8.5: Invalid Email Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "email": "not_an_email",
    "password": "Pass123!",
    "full_name": "Test User"
  }'
```

**Expected**: 422 Unprocessable Entity (validation error)

---

## Summary Table

| Module | Status | Verified | Date |
|--------|--------|----------|------|
| Authentication | Complete | ☐ | ___ |
| Admin | Complete | ☐ | ___ |
| Restaurant | Complete | ☐ | ___ |
| Cashier | Complete | ☐ | ___ |
| Inventory | Complete | ☐ | ___ |
| Frontend | Complete | ☐ | ___ |

---

## Troubleshooting Test Results

### Tests Failing - Connection Refused
**Solution**: Ensure both servers are running
```bash
# Terminal 1: Backend
cd "Tavola Restaurant Management System/backend"
uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Frontend  
cd "Tavola Restaurant Management System/tavola-frontend"
npm start
```

### Tests Failing - Invalid Token
**Solution**: Regenerate token
- Run Test 1.2 again to get new token
- Update `TOKEN` variable with new token
- Retry test

### Tests Failing - CORS errors in frontend
**Info**: Ensure backend CORS is configured in `main.py`
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- Already configured, but verify no errors in backend logs

### Tests Failing - Port Already in Use
**Solution**: 
```bash
# Find and kill process
lsof -i :8000 -t | xargs kill -9
lsof -i :3000 -t | xargs kill -9

# Or use different ports
# Backend: uvicorn main:app --port 8001
# Frontend: PORT=3001 npm start
```

---

**Test Coverage**: All 5 modules tested with typical workflows
**Estimated Test Time**: 30-45 minutes for complete verification

Good luck testing! 🧪
