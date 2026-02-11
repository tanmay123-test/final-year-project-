import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ServiceSelection from '../../pages/ServiceSelection';
import DoctorLogin from '../../pages/DoctorLogin';
import * as api from '../../services/api';

// Mock API
vi.mock('../../services/api', () => ({
  commonService: {
    getServices: vi.fn(),
  },
  workerService: {
    login: vi.fn(),
  }
}));

// Mock AuthContext
const mockWorkerLogin = vi.fn();
const mockUseAuth = vi.fn();
vi.mock('../../context/AuthContext', () => ({
  useAuth: () => mockUseAuth(),
}));

describe('Doctor Login Flow Integration', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockUseAuth.mockReturnValue({
      workerLogin: mockWorkerLogin,
    });
  });

  it('navigates from Provide Service to Doctor Login and logs in successfully', async () => {
    // Setup API response for services
    api.commonService.getServices.mockResolvedValue({
      data: {
        services: [
          { id: 'healthcare', label: 'Healthcare', path: '/doctors' }, // Default user path
          { id: 'housekeeping', label: 'Housekeeping', path: '/worker/housekeeping/login' }
        ]
      }
    });

    mockWorkerLogin.mockResolvedValue({});

    render(
      <MemoryRouter initialEntries={['/provide-service']}>
        <Routes>
          <Route path="/provide-service" element={<ServiceSelection mode="worker" />} />
          <Route path="/worker/healthcare/login" element={<DoctorLogin />} />
          <Route path="/worker/dashboard" element={<div>Worker Dashboard</div>} />
        </Routes>
      </MemoryRouter>
    );

    // 1. Verify we are on Service Selection page
    await waitFor(() => {
      expect(screen.getByText('Select Your Service')).toBeInTheDocument();
      expect(screen.getByText('Healthcare')).toBeInTheDocument();
    });

    // 2. Click Healthcare service
    fireEvent.click(screen.getByText('Healthcare'));

    // 3. Verify we are on Doctor Login page (Doctor Portal)
    // The path in API response was /doctors, but mode="worker" should override it to /worker/healthcare/login
    await waitFor(() => {
      expect(screen.getByText('Doctor Portal')).toBeInTheDocument();
    });

    // 4. Fill in login form
    fireEvent.change(screen.getByLabelText('Email Address'), {
      target: { value: 'doctor@test.com' },
    });

    // 5. Submit form
    fireEvent.click(screen.getByRole('button', { name: /login/i }));

    // 6. Verify calls and navigation
    await waitFor(() => {
      expect(mockWorkerLogin).toHaveBeenCalledWith('doctor@test.com');
      expect(screen.getByText('Worker Dashboard')).toBeInTheDocument();
    });
  });
});
