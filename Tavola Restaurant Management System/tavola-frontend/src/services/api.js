class APIService {
  constructor() {
    this.baseURL = '/api/v1';
    this.token = localStorage.getItem('token');
  }

  getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` })
    };
  }

  // Auth endpoints
  async login(username, password) {
    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (!response.ok) {
      throw new Error('Invalid username or password');
    }
    return await response.json();
  }

  // User endpoints
  async getUsers() {
    const response = await fetch(`${this.baseURL}/admin/users`, {
      method: 'GET',
      headers: this.getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch users');
    return await response.json();
  }

  async createUser(username, email, password, full_name) {
    const response = await fetch(`${this.baseURL}/admin/users`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ username, email, password, full_name })
    });
    if (!response.ok) throw new Error('Failed to create user');
    return await response.json();
  }

  // Permission endpoints
  async getPermissions() {
    const response = await fetch(`${this.baseURL}/admin/permissions`, {
      method: 'GET',
      headers: this.getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch permissions');
    return await response.json();
  }

  async createPermission(name, description) {
    const response = await fetch(`${this.baseURL}/admin/permissions`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ name, description })
    });
    if (!response.ok) throw new Error('Failed to create permission');
    return await response.json();
  }

  async deletePermission(permissionId) {
    const response = await fetch(`${this.baseURL}/admin/permissions/${permissionId}`, {
      method: 'DELETE',
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) throw new Error('Failed to delete permission');
    return await response.json();
  }

  async getCurrentUser() {
    const response = await fetch(`${this.baseURL}/auth/me`, {
      method: 'GET',
      headers: this.getAuthHeaders(),
    });
    if (!response.ok) throw new Error('Failed to fetch current user');
    return await response.json();
  }

  // Menu endpoints
  async getMenuCategories() {
    const response = await fetch(`${this.baseURL}/restaurant/categories`, {
      method: 'GET',
      headers: this.getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch categories');
    return await response.json();
  }

  async getMenuItems(categoryId = null) {
    const url = categoryId 
      ? `${this.baseURL}/restaurant/items?category_id=${categoryId}`
      : `${this.baseURL}/restaurant/items`;
    const response = await fetch(url, {
      method: 'GET',
      headers: this.getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch menu items');
    return await response.json();
  }

  async createMenuItem(name, description, category_id, price, cost) {
    const response = await fetch(`${this.baseURL}/restaurant/items`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ name, description, category_id, price, cost, is_available: true })
    });
    if (!response.ok) throw new Error('Failed to create menu item');
    return await response.json();
  }

  // Order endpoints
  async getOrders() {
    const response = await fetch(`${this.baseURL}/restaurant/orders`, {
      method: 'GET',
      headers: this.getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch orders');
    return await response.json();
  }

  async createOrder(table_id, order_type, items) {
    const response = await fetch(`${this.baseURL}/restaurant/orders`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ table_id, order_type, items })
    });
    if (!response.ok) throw new Error('Failed to create order');
    return await response.json();
  }

  async updateOrderStatus(order_id, status) {
    const response = await fetch(`${this.baseURL}/restaurant/orders/${order_id}/status`, {
      method: 'PUT',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ status })
    });
    if (!response.ok) throw new Error('Failed to update order');
    return await response.json();
  }

  // Cashier endpoints
  async generateInvoice(order_id) {
    const response = await fetch(`${this.baseURL}/cashier/orders/${order_id}/invoice`, {
      method: 'GET',
      headers: this.getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to generate invoice');
    return await response.json();
  }

  async processPayment(order_id, amount, payment_method) {
    const response = await fetch(`${this.baseURL}/cashier/payments`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ order_id, amount, payment_method })
    });
    if (!response.ok) throw new Error('Failed to process payment');
    return await response.json();
  }

  // Inventory endpoints
  async getInventoryItems() {
    const response = await fetch(`${this.baseURL}/inventory/items`, {
      method: 'GET',
      headers: this.getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch inventory');
    return await response.json();
  }

  async getLowStockItems() {
    const response = await fetch(`${this.baseURL}/inventory/items/low-stock`, {
      method: 'GET',
      headers: this.getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch low stock items');
    return await response.json();
  }

  async createInventoryItem(name, unit, current_stock, min_stock_level, reorder_level) {
    const response = await fetch(`${this.baseURL}/inventory/items`, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ name, unit, current_stock, min_stock_level, reorder_level })
    });
    if (!response.ok) throw new Error('Failed to create inventory item');
    return await response.json();
  }

  // Tables
  async getTables() {
    const response = await fetch(`${this.baseURL}/restaurant/tables`, {
      method: 'GET',
      headers: this.getAuthHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch tables');
    return await response.json();
  }
}

export default new APIService();
