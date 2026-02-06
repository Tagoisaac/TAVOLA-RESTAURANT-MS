import React, { useState, useEffect } from 'react';
import APIService from '../services/api';
import './Dashboard.css';

const Dashboard = ({ onLogout }) => {
  const [activeTab, setActiveTab] = useState('orders');
  const [orders, setOrders] = useState([]);
  const [menuItems, setMenuItems] = useState([]);
  const [users, setUsers] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [lowStockItems, setLowStockItems] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData(activeTab);
  }, [activeTab]);

  const fetchData = async (tab) => {
    setIsLoading(true);
    setError('');
    try {
      if (tab === 'orders') {
        const data = await APIService.getOrders();
        setOrders(data);
      } else if (tab === 'menu') {
        const data = await APIService.getMenuItems();
        setMenuItems(data);
      } else if (tab === 'users') {
        const data = await APIService.getUsers();
        setUsers(data);
      } else if (tab === 'inventory') {
        const data = await APIService.getInventoryItems();
        const lowData = await APIService.getLowStockItems();
        setInventory(data);
        setLowStockItems(lowData);
      }
    } catch (err) {
      setError(err.message || 'Failed to load data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    onLogout();
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>🍽️ Tavola - Restaurant Management</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </div>

      <div className="dashboard-content">
        <div className="sidebar">
          <button
            className={activeTab === 'orders' ? 'active' : ''}
            onClick={() => setActiveTab('orders')}
          >
            📋 Orders
          </button>
          <button
            className={activeTab === 'menu' ? 'active' : ''}
            onClick={() => setActiveTab('menu')}
          >
            🍴 Menu
          </button>
          <button
            className={activeTab === 'users' ? 'active' : ''}
            onClick={() => setActiveTab('users')}
          >
            👥 Users
          </button>
          <button
            className={activeTab === 'inventory' ? 'active' : ''}
            onClick={() => setActiveTab('inventory')}
          >
            📦 Inventory
          </button>
        </div>

        <div className="main-content">
          {error && <div className="error-message">{error}</div>}

          {isLoading && <div className="loading">Loading...</div>}

          {!isLoading && activeTab === 'orders' && (
            <div className="tab-content">
              <h2>Orders</h2>
              {orders.length === 0 ? (
                <p>No orders yet</p>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Order #</th>
                      <th>Type</th>
                      <th>Status</th>
                      <th>Amount</th>
                      <th>Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orders.map(order => (
                      <tr key={order.id}>
                        <td>{order.order_number}</td>
                        <td>{order.order_type}</td>
                        <td><span className={`status ${order.status}`}>{order.status}</span></td>
                        <td>${order.total_amount.toFixed(2)}</td>
                        <td>{new Date(order.created_at).toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}

          {!isLoading && activeTab === 'menu' && (
            <div className="tab-content">
              <h2>Menu Items</h2>
              {menuItems.length === 0 ? (
                <p>No menu items</p>
              ) : (
                <div className="menu-grid">
                  {menuItems.map(item => (
                    <div key={item.id} className="menu-card">
                      <h3>{item.name}</h3>
                      <p className="description">{item.description}</p>
                      <p className="price">${item.price.toFixed(2)}</p>
                      <span className={`availability ${item.is_available ? 'available' : 'unavailable'}`}>
                        {item.is_available ? 'Available' : 'Unavailable'}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {!isLoading && activeTab === 'users' && (
            <div className="tab-content">
              <h2>Users</h2>
              {users.length === 0 ? (
                <p>No users</p>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Username</th>
                      <th>Email</th>
                      <th>Full Name</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map(user => (
                      <tr key={user.id}>
                        <td>{user.username}</td>
                        <td>{user.email}</td>
                        <td>{user.full_name}</td>
                        <td>{user.is_active ? 'Active' : 'Inactive'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}

          {!isLoading && activeTab === 'inventory' && (
            <div className="tab-content">
              <h2>Inventory Management</h2>
              
              {lowStockItems.length > 0 && (
                <div className="alert-box">
                  <h3>⚠️ Low Stock Items</h3>
                  <ul>
                    {lowStockItems.map(item => (
                      <li key={item.id}>
                        {item.name}: {item.current_stock} {item.unit} (Reorder at: {item.reorder_level})
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <h3 style={{ marginTop: '20px' }}>All Inventory Items</h3>
              {inventory.length === 0 ? (
                <p>No inventory items</p>
              ) : (
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Name</th>
                      <th>Unit</th>
                      <th>Current Stock</th>
                      <th>Min Level</th>
                      <th>Reorder Level</th>
                    </tr>
                  </thead>
                  <tbody>
                    {inventory.map(item => (
                      <tr key={item.id}>
                        <td>{item.name}</td>
                        <td>{item.unit}</td>
                        <td>{item.current_stock}</td>
                        <td>{item.min_stock_level}</td>
                        <td>{item.reorder_level}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
