import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import Login from '../../pages/Login';
import ServiceSelection from '../../pages/ServiceSelection';
import { AuthProvider } from '../../context/AuthContext';
import { authService, commonService } from '../../services/api';

// Mock API
vi.mock('../../services/api', () => ({
  authService: {
    login: vi.fn(),
    getUserInfo: vi.fn(),
  },
  commonService: {
    getServices: vi.fn(),
  }
}));

// Mock icons
vi.mock('lucide-react', async () => {
  const actual = await vi.importActual('lucide-react');
  return {
    ...actual,
    Stethoscope: () => <div data-testid="icon-stethoscope" />,
    Home: () => <div data-testid="icon-home" />,
    Package: () => <div data-testid="icon-package" />,
    Car: () => <div data-testid="icon-car" />,
    Wallet: () => <div data-testid="icon-wallet" />,
    ChevronLeft: () => <div data-testid="icon-chevron-left" />,
  };
});

describe('Login to Service Selection Flow', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('redirects to services page and fetches data after login', async () => {
    // Mock Login Success
    authService.login.mockResolvedValue({
      data: { token: 'fake-token', user_id: 1 }
    });
    authService.getUserInfo.mockResolvedValue({
      data: { id: 1, name: 'Test User' }
    });

    // Mock Services Fetch
    const mockServices = [
      { id: 'healthcare', label: 'Healthcare Service', path: '/worker/healthcare/login' },
      { id: 'housekeeping', label: 'Housekeeping Service', path: '/worker/housekeeping/login' }
    ];
    commonService.getServices.mockResolvedValue({
      data: { services: mockServices }
    });

    render(
      <MemoryRouter initialEntries={['/login']}>
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/services" element={<ServiceSelection />} />
          </Routes>
        </AuthProvider>
      </MemoryRouter>
    );

    // Perform Login
    fireEvent.change(screen.getByLabelText(/username or email/i), { target: { value: 'user' } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'pass' } });
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    // Wait for redirect and service fetch
    await waitFor(() => {
      expect(screen.getByText('Select Your Service')).toBeInTheDocument();
    }, { timeout: 3000 });

    // Verify API call
    expect(commonService.getServices).toHaveBeenCalledTimes(1);

    // Verify Render
    expect(screen.getByText('Healthcare Service')).toBeInTheDocument();
    expect(screen.getByText('Housekeeping Service')).toBeInTheDocument();

    // Verify Cache
    const cached = localStorage.getItem('services_cache');
    expect(cached).toBeTruthy();
    expect(JSON.parse(cached)).toEqual(mockServices);
  });
});
