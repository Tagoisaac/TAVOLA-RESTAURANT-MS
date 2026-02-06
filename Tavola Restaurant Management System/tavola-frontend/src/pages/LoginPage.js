import React, { useState } from 'react';
import APIService from '../services/api';
import './LoginPage.css';

const LoginPage = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await APIService.login(username, password);
      localStorage.setItem('token', response.access_token);
      setUsername('');
      setPassword('');
      onLoginSuccess(response);
    } catch (err) {
      setError(err.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-logo">
          <h1>🍽️ Tavola</h1>
          <p>Restaurant Management System</p>
        </div>

        <form onSubmit={handleLogin}>
          <h2>Login</h2>

          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label>Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={isLoading}
              placeholder="Enter your username"
            />
          </div>

          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
              placeholder="Enter your password"
            />
          </div>

          <button type="submit" disabled={isLoading} className="submit-btn">
            {isLoading ? 'Loading...' : 'Login'}
          </button>
        </form>

        <div className="info-box">
          <p>👤 <strong>Need an account?</strong></p>
          <p>Contact your administrator to create a user account.</p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
