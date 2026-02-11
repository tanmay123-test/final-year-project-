import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MemoryRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Login from '../../pages/Login';
import Dashboard from '../../pages/Dashboard';
import { AuthProvider, useAuth } from '../../context/AuthContext';
import { authService, appointmentService } from '../../services/api';
import ProtectedRoute from '../../components/ProtectedRoute';

// Mock API
vi.mock('../../services/api', () => ({
  authService: {
    login: vi.fn(),
    getUserInfo: vi.fn(),
  },
  appointmentService: {
    getUserAppointments: vi.fn(),
  },
  // We need to mock other services if AuthProvider or Dashboard calls them
  workerService: {
    login: vi.fn(),
  }
}));

// Mock console methods to verify logging
const consoleInfoSpy = vi.spyOn(console, 'info').mockImplementation(() => {});
const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

describe('Simple Login Flow', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('renders login form with correct fields', () => {
    render(
      <MemoryRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </MemoryRouter>
    );

    expect(screen.getByLabelText(/username or email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
  });

  it('handles successful login and redirects to dashboard', async () => {
    // Mock successful login
    authService.login.mockResolvedValue({
      data: { token: 'fake-jwt-token', user_id: 123 }
    });
    authService.getUserInfo.mockResolvedValue({
      data: { id: 123, user_name: 'Test User' }
    });
    appointmentService.getUserAppointments.mockResolvedValue({
      data: { appointments: [] }
    });

    render(
      <MemoryRouter initialEntries={['/login']}>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    );

    // Fill form
    fireEvent.change(screen.getByLabelText(/username or email/i), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    
    // Submit
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    // Check loading state (might be too fast to catch, but we can try)
    const submitButton = screen.getByRole('button', { name: /logging in/i });
    expect(submitButton).toBeDisabled();
    expect(submitButton).toHaveTextContent(/logging in/i);

    // Verify API call
    await waitFor(() => {
      expect(authService.login).toHaveBeenCalledWith({ username: 'testuser', password: 'password123' });
    });

    // Verify Logging
    expect(consoleInfoSpy).toHaveBeenCalledWith(expect.stringContaining('Login attempt started'));
    expect(consoleInfoSpy).toHaveBeenCalledWith(expect.stringContaining('Login successful'));

    // Verify Redirect
    await waitFor(() => {
      expect(screen.getByText(/welcome, test user/i)).toBeInTheDocument();
    });
  });

  it('displays error message on failed login', async () => {
    // Mock failed login
    authService.login.mockRejectedValue({
      response: { data: { error: 'Invalid credentials' } }
    });

    render(
      <MemoryRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/username or email/i), { target: { value: 'wrong' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'wrong' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });

    // Verify Logging
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Login failed'), expect.anything());
  });

  it('redirects to login from protected route and back after login', async () => {
    authService.login.mockResolvedValue({
      data: { token: 'fake-jwt-token', user_id: 123 }
    });
    authService.getUserInfo.mockResolvedValue({
      data: { id: 123, user_name: 'Test User' }
    });
    appointmentService.getUserAppointments.mockResolvedValue({
      data: { appointments: [] }
    });

    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    );

    // Should be redirected to login because we are not authenticated
    await waitFor(() => {
      expect(screen.getByLabelText(/username or email/i)).toBeInTheDocument();
    });

    // Login
    fireEvent.change(screen.getByLabelText(/username or email/i), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    // Should be redirected back to dashboard
    await waitFor(() => {
      expect(screen.getByText(/welcome, test user/i)).toBeInTheDocument();
    });
  });
});
