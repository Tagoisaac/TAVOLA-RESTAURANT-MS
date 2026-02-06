import React, { useState, useEffect } from 'react';
import apiService from '../services/api';
import './Dashboard.css';

function Dashboard() {
  const [activeTab, setActiveTab] = useState('orders');
  const [orders, setOrders] = useState([]);
  const [menuItems, setMenuItems] = useState([]);
  const [users, setUsers] = useState([]);
  const [inventoryItems, setInventoryItems] = useState([]);
  const [lowStockItems, setLowStockItems] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadDashboardData();
  }, [activeTab]);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      switch(activeTab) {
        case 'orders':
          const ordersData = await apiService.getOrders();
          setOrders(ordersData);
          break;
        case 'menu':
          const itemsData = await apiService.getMenuItems();
          setMenuItems(itemsData);
          break;
        case 'users':
          const usersData = await apiService.getUsers();
          setUsers(usersData);
          break;
        case 'inventory':
          const invData = await apiService.getInventoryItems();
          setInventoryItems(invData);
          const lowStockData = await apiService.getLowStockItems();
          setLowStockItems(lowStockData);
          break;
        default:
          break;
      }
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Tavola Restaurant Management System</h1>
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <div className="dashboard-container">
        <nav className="sidebar">
          <ul>
            <li>
              <button 
                className={activeTab === 'orders' ? 'active' : ''} 
                onClick={() => setActiveTab('orders')}
              >
                📦 Orders
              </button>
            </li>
            <li>
              <button 
                className={activeTab === 'menu' ? 'active' : ''} 
                onClick={() => setActiveTab('menu')}
              >
                🍽️ Menu
              </button>
            </li>
            <li>
              <button 
                className={activeTab === 'users' ? 'active' : ''} 
                onClick={() => setActiveTab('users')}
              >
                👥 Users
              </button>
            </li>
            <li>
              <button 
                className={activeTab === 'inventory' ? 'active' : ''} 
                onClick={() => setActiveTab('inventory')}
              >
                📊 Inventory
              </button>
            </li>
          </ul>
        </nav>

        <main className="dashboard-content">
          {isLoading && <div className="loading">Loading...</div>}
          
          {!isLoading && activeTab === 'orders' && (
            <div className="section">
              <h2>Orders</h2>
              {orders.length === 0 ? (
                <p>No orders found</p>
              ) : (
                <table>
                  <thead>
                    <tr>
                      <th>Order #</th>
                      <th>Type</th>
                      <th>Status</th>
                      <th>Total</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orders.map(order => (
                      <tr key={order.id}>
                        <td>{order.order_number}</td>
                        <td>{order.order_type}</td>
                        <td><span className={`status ${order.status}`}>{order.status}</span></td>
                        <td>${order.total_amount}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}

          {!isLoading && activeTab === 'menu' && (
            <div className="section">
              <h2>Menu Items</h2>
              {menuItems.length === 0 ? (
                <p>No menu items found</p>
              ) : (
                <div className="grid">
                  {menuItems.map(item => (
                    <div key={item.id} className="card">
                      <h3>{item.name}</h3>
                      <p>{item.description}</p>
                      <p className="price">${item.price}</p>
                      <p className="availability">{item.is_available ? '✓ Available' : '✗ Unavailable'}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {!isLoading && activeTab === 'users' && (
            <div className="section">
              <h2>Users</h2>
              {users.length === 0 ? (
                <p>No users found</p>
              ) : (
                <table>
                  <thead>
                    <tr>
                      <th>Username</th>
                      <th>Email</th>
                      <th>Role</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map(user => (
                      <tr key={user.id}>
                        <td>{user.username}</td>
                        <td>{user.email}</td>
                        <td>{user.role.name}</td>
                        <td>{user.is_active ? 'Active' : 'Inactive'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}

          {!isLoading && activeTab === 'inventory' && (
            <div className="section">
              <h2>Inventory</h2>
              
              {lowStockItems.length > 0 && (
                <div className="alert">
                  <h3>⚠️ Low Stock Items</h3>
                  <ul>
                    {lowStockItems.map(item => (
                      <li key={item.id}>{item.name}: {item.current_stock} {item.unit} (Min: {item.min_stock_level})</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {inventoryItems.length === 0 ? (
                <p>No inventory items found</p>
              ) : (
                <table>
                  <thead>
                    <tr>
                      <th>Item</th>
                      <th>Unit</th>
                      <th>Current Stock</th>
                      <th>Min Level</th>
                    </tr>
                  </thead>
                  <tbody>
                    {inventoryItems.map(item => (
                      <tr key={item.id}>
                        <td>{item.name}</td>
                        <td>{item.unit}</td>
                        <td>{item.current_stock}</td>
                        <td>{item.min_stock_level}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default Dashboard;
