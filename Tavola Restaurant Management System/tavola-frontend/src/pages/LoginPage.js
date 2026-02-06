import React, { useState } from 'react';
import APIService from '../services/api';
import './LoginPage.css';

const LoginPage = ({ onLoginSuccess }) => {
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await APIService.register(username, email, password, fullName);
      setError('');
      setUsername('');
      setEmail('');
      setPassword('');
      setFullName('');
      setIsRegister(false);
      alert('Registration successful! Please login.');
    } catch (err) {
      setError(err.message || 'Registration failed');
    } finally {
      setIsLoading(false);
    }
  };

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

  const handleSubmit = (e) => {
    if (isRegister) {
      handleRegister(e);
    } else {
      handleLogin(e);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <div className="login-logo">
          <h1>🍽️ Tavola</h1>
          <p>Restaurant Management System</p>
        </div>

        <form onSubmit={handleSubmit}>
          <h2>{isRegister ? 'Register' : 'Login'}</h2>

          {error && <div className="error-message">{error}</div>}

          <div className="form-group">
            <label>Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>

          {isRegister && (
            <>
              <div className="form-group">
                <label>Email:</label>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  disabled={isLoading}
                />
              </div>

              <div className="form-group">
                <label>Full Name:</label>
                <input
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  required
                  disabled={isLoading}
                />
              </div>
            </>
          )}

          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>

          <button type="submit" disabled={isLoading} className="submit-btn">
            {isLoading ? 'Loading...' : isRegister ? 'Register' : 'Login'}
          </button>
        </form>

        <div className="toggle-mode">
          {isRegister ? (
            <>
              Already have an account?{' '}
              <button
                type="button"
                onClick={() => {
                  setIsRegister(false);
                  setError('');
                  setEmail('');
                  setFullName('');
                }}
                className="link-button"
              >
                Login
              </button>
            </>
          ) : (
            <>
              Don't have an account?{' '}
              <button
                type="button"
                onClick={() => {
                  setIsRegister(true);
                  setError('');
                }}
                className="link-button"
              >
                Register
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
