import React, { useState } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { AtSign, Lock, Eye, EyeOff, Plus } from 'lucide-react';
import { apiEvents } from '../services/api';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/services';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    // Simple client-side logging
    console.info(`[Auth] Login attempt started for user: ${username} at ${new Date().toISOString()}`);

    const fingerprint = `${navigator.userAgent}|${navigator.platform}|${navigator.language}|${new Date().getTimezoneOffset()}`;
    try {
      await login(username, password);
      console.info(`[Auth] Login successful for user: ${username}`);
      apiEvents.dispatchEvent(new CustomEvent('api:success', { detail: { message: 'Woohoo! Login successful' } }));
      const key = `device_fp_${username}`;
      const prev = localStorage.getItem(key);
      if (prev && prev !== fingerprint) {
        apiEvents.dispatchEvent(new CustomEvent('toast:info', { detail: { message: 'New device login detected' } }));
      }
      localStorage.setItem(key, fingerprint);
      localStorage.removeItem(`fail_count_${username}`);
      navigate(from, { replace: true });
    } catch (err) {
      console.error(`[Auth] Login failed for user: ${username}`, err);
      const msg = err.response?.data?.error || 'Failed to login. Please check your credentials.';
      setError(msg);
      apiEvents.dispatchEvent(new CustomEvent('api:error', { detail: { message: 'Login failed' } }));
      const k = `fail_count_${username}`;
      const c = parseInt(localStorage.getItem(k) || '0', 10) + 1;
      localStorage.setItem(k, String(c));
      if (c >= 3) {
        apiEvents.dispatchEvent(new CustomEvent('api:error', { detail: { message: 'Suspicious activity: multiple failed logins' } }));
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleForgot = (e) => {
    e.preventDefault();
    apiEvents.dispatchEvent(new CustomEvent('toast:info', { detail: { message: 'Password reset link sent to your email' } }));
  };

  return (
    <div className="auth-container-wrapper">
      <div className="auth-container">
        <div className="auth-header">
          <div className="auth-icon">
            <Plus size={32} strokeWidth={3} />
          </div>
          <h2 className="auth-title">Welcome Back</h2>
          <p className="auth-subtitle">Login to continue to ExpertEase</p>
        </div>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="username">Username or Email</label>
            <div className="input-wrapper">
              <AtSign className="input-icon" size={20} />
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                placeholder="Enter your username or email"
                autoComplete="username"
              />
            </div>
          </div>

          <div className="input-group">
            <label htmlFor="password">Password</label>
            <div className="input-wrapper">
              <Lock className="input-icon" size={20} />
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="••••••••"
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>

          <Link to="#" className="forgot-password" onClick={handleForgot}>Forgot Password?</Link>

          <button type="submit" className="btn-primary" disabled={isLoading}>
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <div className="auth-footer">
          Don't have an account? <Link to="/signup">Sign Up</Link>
          <div style={{ marginTop: '1rem' }}>
            <Link to="/" style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 'normal' }}>
              ← Back to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
