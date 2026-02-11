import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MemoryRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Login from '../../pages/Login';
import VerifyEmail from '../../pages/VerifyEmail';
import { AuthProvider, useAuth } from '../../context/AuthContext';
import { ToastProvider } from '../../context/ToastContext';
import { authService } from '../../services/api';

// Mock API
vi.mock('../../services/api', () => ({
  authService: {
    login: vi.fn(),
    verifyLoginOtp: vi.fn(),
    getUserInfo: vi.fn(),
    verifyOtp: vi.fn(), // Needed for signup flow if touched
  }
}));

// Mock Toast
// Note: We don't strictly need to mock ToastContext implementation if we wrap with ToastProvider,
// but mocking the hook return value can be cleaner to avoid implementation details or portal issues.
// However, since we are doing integration test, using real ToastProvider is better if possible.
// But ToastProvider uses portals which might need setup. Let's stick to real provider for now, 
// if it fails we mock. The worker test used ToastProvider, so it should be fine.

describe('User Auth Flow', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('redirects to verification page on 2-step login', async () => {
    // Mock login response requiring OTP
    authService.login.mockResolvedValue({
      data: { 
        msg: "OTP sent",
        email: 'user@example.com',
        username: 'testuser'
      }
    });

    render(
      <MemoryRouter initialEntries={['/login']}>
        <ToastProvider>
          <AuthProvider>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/verify-email" element={<VerifyEmail />} />
            </Routes>
          </AuthProvider>
        </ToastProvider>
      </MemoryRouter>
    );

    // Fill login form
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    // Verify API call
    await waitFor(() => {
      expect(authService.login).toHaveBeenCalledWith({ username: 'testuser', password: 'password123' });
    });

    // Verify navigation to verify-email
    // Check if VerifyEmail component is rendered with correct mode
    await waitFor(() => {
        expect(screen.getByText(/verify login/i)).toBeInTheDocument();
        expect(screen.getByText(/user@example.com/i)).toBeInTheDocument();
    });
  });

  it('completes login after OTP verification', async () => {
      // Mock verifyLoginOtp success
      authService.verifyLoginOtp.mockResolvedValue({
          data: { token: 'fake-token', user_id: 1 }
      });
      authService.getUserInfo.mockResolvedValue({
          data: { username: 'testuser', id: 1 }
      });

      // Render starting at verify-email with state
      const initialEntry = {
          pathname: '/verify-email',
          state: { 
              mode: 'login', 
              email: 'user@example.com', 
              username: 'testuser',
              from: '/dashboard'
          }
      };

      render(
        <MemoryRouter initialEntries={[initialEntry]}>
          <ToastProvider>
            <AuthProvider>
              <Routes>
                <Route path="/verify-email" element={<VerifyEmail />} />
                <Route path="/dashboard" element={<div>Dashboard Page</div>} />
              </Routes>
            </AuthProvider>
          </ToastProvider>
        </MemoryRouter>
      );

      // Verify UI is present
      expect(screen.getByText(/verify login/i)).toBeInTheDocument();

      // Enter OTP
      const inputs = screen.getAllByRole('textbox');
      // Inputs might be 6 separate fields.
      // We can try to paste or type in each.
      inputs.forEach((input) => {
          fireEvent.change(input, { target: { value: '1' } });
      });

      // Submit
      fireEvent.click(screen.getByRole('button', { name: /verify/i }));

      // Verify API call
      await waitFor(() => {
          expect(authService.verifyLoginOtp).toHaveBeenCalledWith({ 
              email: 'user@example.com', 
              otp: '111111', 
              username: 'testuser' 
          });
      });

      // Verify navigation to dashboard
      await waitFor(() => {
          expect(screen.getByText(/dashboard page/i)).toBeInTheDocument();
      });
  });

  it('redirects to protected route after login', async () => {
    // Mock successful direct login (no OTP for this case to keep it simple, or reuse OTP flow)
    // Let's use direct login to test the redirect logic primarily
    authService.login.mockResolvedValue({
        data: { token: 'fake-token', user_id: 1 }
    });
    authService.getUserInfo.mockResolvedValue({
        data: { username: 'testuser', id: 1 }
    });

    render(
      <MemoryRouter initialEntries={['/dashboard']}>
        <ToastProvider>
          <AuthProvider>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/dashboard" element={
                // Simplified ProtectedRoute for testing since we can't easily import the one from App.jsx 
                // without exporting it or refactoring. 
                // But wait, the logic is IN App.jsx ProtectedRoute. 
                // I should probably duplicate the logic here to test if passing state works as expected
                // OR better, I should rely on the fact that I'm testing Login.jsx's ability to read location.state
                // So I can just manually set the location state in initialEntries or a wrapper.
                // But to simulate "Redirect to login from protected route", I need a component that does that.
                // Let's create a test wrapper.
                <MockProtectedRoute><div data-testid="dashboard">Dashboard</div></MockProtectedRoute>
              } />
            </Routes>
          </AuthProvider>
        </ToastProvider>
      </MemoryRouter>
    );

    // Should be redirected to login
    await waitFor(() => {
        expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
    });

    // Login
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'password123' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    // Should be redirected back to dashboard
    await waitFor(() => {
        expect(screen.getByTestId('dashboard')).toBeInTheDocument();
    });
  });
});

const MockProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) return <div>Loading...</div>;
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />;
  return children;
};
