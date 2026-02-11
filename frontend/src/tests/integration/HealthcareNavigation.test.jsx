import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import ServiceSelection from '../../pages/ServiceSelection';
import { commonService } from '../../services/api';

// Mock API
vi.mock('../../services/api', () => ({
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

// Mock DoctorSearch component
const MockDoctorSearch = () => <div>Healthcare Referral Form</div>;

describe('Healthcare Navigation Flow', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('navigates to /doctors when Healthcare is clicked', async () => {
    // Mock Services Fetch with NEW correct path
    const mockServices = [
      { id: 'healthcare', label: 'Healthcare', path: '/doctors' },
      { id: 'housekeeping', label: 'Housekeeping', path: '/worker/housekeeping/login' }
    ];
    
    commonService.getServices.mockResolvedValue({
      data: { services: mockServices }
    });

    render(
      <MemoryRouter initialEntries={['/services']}>
        <Routes>
          <Route path="/services" element={<ServiceSelection />} />
          <Route path="/doctors" element={<MockDoctorSearch />} />
        </Routes>
      </MemoryRouter>
    );

    // Verify initial render (loading from default or waiting for fetch)
    // Wait for API data to populate
    await waitFor(() => {
      expect(commonService.getServices).toHaveBeenCalledTimes(1);
    });

    // Find and click Healthcare card
    const healthcareCard = await screen.findByText('Healthcare');
    fireEvent.click(healthcareCard);

    // Verify navigation to DoctorSearch
    await waitFor(() => {
      expect(screen.getByText('Healthcare Referral Form')).toBeInTheDocument();
    });
  });
});
