import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [apiStatus, setApiStatus] = useState('Loading...');

  useEffect(() => {
    // Check if backend is running using relative path (proxied through package.json)
    fetch('/health')
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('API request failed');
      })
      .then(data => setApiStatus('✓ Backend API is running'))
      .catch(error => {
        console.error('API Error:', error);
        setApiStatus('✗ Backend API is not responding');
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Tavola Restaurant Management System</h1>
        <p>Version 1.0.0</p>
        <div className="status-box">
          <p className="api-status">{apiStatus}</p>
        </div>
        <p>
          Welcome to the Restaurant Management System frontend. The system is under development.
        </p>
        <div className="info-box">
          <p><strong>Frontend:</strong> Running on http://localhost:3000</p>
          <p><strong>Backend API:</strong> Running on http://localhost:8000</p>
          <p><strong>API Docs:</strong> http://localhost:8000/docs</p>
        </div>
      </header>
    </div>
  );
}

export default App;
