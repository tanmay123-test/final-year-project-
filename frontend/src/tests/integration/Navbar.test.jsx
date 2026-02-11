import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Navbar from '../../components/Navbar';
import { AuthProvider } from '../../context/AuthContext';

// Mock Lucide icons
vi.mock('lucide-react', async () => {
  const actual = await vi.importActual('lucide-react');
  return {
    ...actual,
    Stethoscope: () => <div data-testid="icon-stethoscope" />,
    Menu: () => <div data-testid="icon-menu" />,
    X: () => <div data-testid="icon-x" />,
    User: () => <div data-testid="icon-user" />,
    LogOut: () => <div data-testid="icon-logout" />,
    LayoutDashboard: () => <div data-testid="icon-dashboard" />,
    Search: () => <div data-testid="icon-search" />,
    Briefcase: () => <div data-testid="icon-briefcase" />,
  };
});

// Mock AuthContext
const mockUser = { user_name: 'Test User', id: 1 };
const mockWorker = { email: 'doctor@example.com', id: 2 };
const mockLogout = vi.fn();

vi.mock('../../context/AuthContext', () => ({
  useAuth: vi.fn(),
  AuthProvider: ({ children }) => <div>{children}</div> 
}));

import { useAuth } from '../../context/AuthContext';

describe('Navbar Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders logo and brand name correctly', () => {
    useAuth.mockReturnValue({ user: null, worker: null, logout: mockLogout });
    
    render(
      <MemoryRouter>
        <Navbar />
      </MemoryRouter>
    );

    expect(screen.getByText('ExpertEase')).toBeInTheDocument();
    expect(screen.getByTestId('icon-stethoscope')).toBeInTheDocument();
  });

  it('renders patient links when user is logged in', () => {
    useAuth.mockReturnValue({ user: mockUser, worker: null, logout: mockLogout });

    render(
      <MemoryRouter>
        <Navbar />
      </MemoryRouter>
    );

    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Find Doctors')).toBeInTheDocument();
    expect(screen.getByText('Hi, Test User')).toBeInTheDocument();
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  it('renders provider links when worker is logged in', () => {
    useAuth.mockReturnValue({ user: null, worker: mockWorker, logout: mockLogout });

    render(
      <MemoryRouter>
        <Navbar />
      </MemoryRouter>
    );

    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Dr. doctor')).toBeInTheDocument(); // split logic test
    expect(screen.getByText('Logout')).toBeInTheDocument();
  });

  it('toggles mobile menu when menu button is clicked', () => {
    useAuth.mockReturnValue({ user: mockUser, worker: null, logout: mockLogout });

    render(
      <MemoryRouter>
        <Navbar />
      </MemoryRouter>
    );

    // Initial state: menu icon visible (simulated logic, CSS controls visibility but React controls state)
    const menuBtn = screen.getByLabelText('Toggle menu');
    expect(screen.getByTestId('icon-menu')).toBeInTheDocument();

    // Click to open
    fireEvent.click(menuBtn);
    expect(screen.getByTestId('icon-x')).toBeInTheDocument();
    
    // Check if class is applied (we need to check the container)
    // In our implementation, the container div gets 'mobile-open' class
    // We can't easily check class on an element unless we select it by testId or role
    // But we can check if the state change triggered the icon swap, which confirms logic works.
  });
});
