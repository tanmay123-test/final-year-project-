import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import WorkerLogin from '../../pages/WorkerLogin';
import WorkerSignup from '../../pages/WorkerSignup';
import * as AuthContext from '../../context/AuthContext';
import * as api from '../../services/api';

// Mock AuthContext
const mockWorkerLogin = vi.fn();
const mockUseAuth = vi.fn();

vi.mock('../../context/AuthContext', () => ({
  useAuth: () => mockUseAuth(),
}));

// Mock API
vi.mock('../../services/api', () => ({
  doctorService: {
    getSpecializations: vi.fn().mockResolvedValue({ data: { specializations: ['Cardiology', 'Dermatology'] } }),
  },
  workerService: {
    register: vi.fn(),
  }
}));

describe('Worker Auth Pages (Healthcare)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockUseAuth.mockReturnValue({
      workerLogin: mockWorkerLogin,
      loading: false,
    });
  });

  describe('WorkerLogin', () => {
    it('renders healthcare login with correct texts and layout', () => {
      render(
        <MemoryRouter initialEntries={['/worker/healthcare/login']}>
          <Routes>
            <Route path="/worker/:serviceType/login" element={<WorkerLogin serviceType="healthcare" />} />
          </Routes>
        </MemoryRouter>
      );

      // Header and Title
      expect(screen.getByText('Doctor Portal')).toBeInTheDocument();
      expect(screen.getByText('Login with your registered email')).toBeInTheDocument();
      
      // Form Elements
      expect(screen.getByLabelText('Email Address')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
      
      // Footer
      expect(screen.getByText('Not registered as a doctor?')).toBeInTheDocument();
      expect(screen.getByText('Apply here')).toBeInTheDocument();
      
      // Back Button (ChevronLeft) - Check for link
      const links = screen.getAllByRole('link');
      // We expect at least back button and "Apply here"
      expect(links.length).toBeGreaterThanOrEqual(2);
    });
  });

  describe('WorkerSignup', () => {
    it('renders healthcare signup with correct texts and layout', async () => {
      render(
        <MemoryRouter initialEntries={['/worker/healthcare/signup']}>
          <Routes>
            <Route path="/worker/:serviceType/signup" element={<WorkerSignup serviceType="healthcare" />} />
          </Routes>
        </MemoryRouter>
      );

      // Header and Title
      expect(screen.getByText('Join as a Doctor')).toBeInTheDocument();
      expect(screen.getByText('Register to provide healthcare services')).toBeInTheDocument();
      
      // Form Elements
      expect(screen.getByLabelText('Full Name')).toBeInTheDocument();
      expect(screen.getByLabelText('Email')).toBeInTheDocument();
      expect(screen.getByLabelText('Phone')).toBeInTheDocument();
      expect(screen.getByLabelText('Specialization')).toBeInTheDocument();
      expect(screen.getByLabelText('Experience (years)')).toBeInTheDocument();
      expect(screen.getByLabelText('Clinic Location')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /register/i })).toBeInTheDocument();
      
      // Footer
      expect(screen.getByText('Already registered?')).toBeInTheDocument();
      expect(screen.getByText('Login')).toBeInTheDocument();
      
      // Wait for specializations to load
      await waitFor(() => {
        expect(screen.getByText('Cardiology')).toBeInTheDocument();
      });
    });
  });
});
