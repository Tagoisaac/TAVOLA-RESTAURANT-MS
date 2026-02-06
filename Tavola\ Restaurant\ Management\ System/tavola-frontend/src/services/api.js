// API Service - handles all communication with the backend

const API_BASE_URL = '/api/v1';

class APIService {
  // Auth endpoints
  async login(username, password) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!response.ok) throw new Error('Login failed');
    return response.json();
  }

  async register(userData) {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    if (!response.ok) throw new Error('Registration failed');
    return response.json();
  }

  // User endpoints
  async getUsers() {
    const response = await fetch(`${API_BASE_URL}/admin/users`);
    return response.json();
  }

  async createUser(userData) {
    const response = await fetch(`${API_BASE_URL}/admin/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return response.json();
  }

  // Menu endpoints
  async getMenuCategories() {
    const response = await fetch(`${API_BASE_URL}/restaurant/categories`);
    return response.json();
  }

  async getMenuItems(categoryId) {
    const url = categoryId 
      ? `${API_BASE_URL}/restaurant/items?category_id=${categoryId}`
      : `${API_BASE_URL}/restaurant/items`;
    const response = await fetch(url);
    return response.json();
  }

  async createMenuItem(itemData) {
    const response = await fetch(`${API_BASE_URL}/restaurant/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(itemData)
    });
    return response.json();
  }

  // Order endpoints
  async getOrders() {
    const response = await fetch(`${API_BASE_URL}/restaurant/orders`);
    return response.json();
  }

  async createOrder(orderData) {
    const response = await fetch(`${API_BASE_URL}/restaurant/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderData)
    });
    return response.json();
  }

  async updateOrderStatus(orderId, status) {
    const response = await fetch(`${API_BASE_URL}/restaurant/orders/${orderId}/status`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    });
    return response.json();
  }

  // Table endpoints
  async getTables() {
    const response = await fetch(`${API_BASE_URL}/restaurant/tables`);
    return response.json();
  }

  // Inventory endpoints
  async getInventoryItems() {
    const response = await fetch(`${API_BASE_URL}/inventory/items`);
    return response.json();
  }

  async getLowStockItems() {
    const response = await fetch(`${API_BASE_URL}/inventory/low-stock`);
    return response.json();
  }

  // Cashier endpoints
  async getInvoice(orderId) {
    const response = await fetch(`${API_BASE_URL}/cashier/orders/${orderId}/invoice`);
    return response.json();
  }

  async processPayment(paymentData) {
    const response = await fetch(`${API_BASE_URL}/cashier/payments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(paymentData)
    });
    return response.json();
  }
}

export default new APIService();
