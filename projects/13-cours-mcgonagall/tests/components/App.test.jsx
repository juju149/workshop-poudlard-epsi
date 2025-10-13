import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import App from '../../src/App';

describe('App', () => {
  beforeEach(() => {
    // Mock the window.electronAPI
    global.window.electronAPI = {
      getEnv: vi.fn().mockResolvedValue({ hasCredentials: true }),
      scrapeSchedule: vi.fn().mockResolvedValue({
        success: true,
        data: []
      })
    };
  });

  it('should render main title', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/Emploi du Temps McGonagall/i)).toBeInTheDocument();
    });
  });

  it('should render subtitle', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/Consultez votre emploi du temps magique/i)).toBeInTheDocument();
    });
  });

  it('should show warning when credentials are not configured', async () => {
    global.window.electronAPI.getEnv = vi.fn().mockResolvedValue({ hasCredentials: false });
    
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/Veuillez configurer vos identifiants/i)).toBeInTheDocument();
    });
  });

  it('should render DateSelector component', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByLabelText(/Date/i)).toBeInTheDocument();
    });
  });

  it('should show initial message when no schedule is loaded', async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/Sélectionnez une date/i)).toBeInTheDocument();
    });
  });

  it('should handle missing electronAPI gracefully', async () => {
    delete global.window.electronAPI;
    
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/Emploi du Temps McGonagall/i)).toBeInTheDocument();
    });
  });

  it('should call electronAPI.scrapeSchedule when date is selected', async () => {
    const mockScrape = vi.fn().mockResolvedValue({ success: true, data: [] });
    global.window.electronAPI.scrapeSchedule = mockScrape;

    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText(/Aujourd'hui/i)).toBeInTheDocument();
    });
    
    const todayButton = screen.getByText(/Aujourd'hui/i);
    fireEvent.click(todayButton);

    await waitFor(() => {
      expect(mockScrape).toHaveBeenCalled();
    });
  });

  it('should show error when electronAPI is not available during fetch', async () => {
    // Set up electronAPI initially for the component to mount
    global.window.electronAPI = {
      getEnv: vi.fn().mockResolvedValue({ hasCredentials: true }),
      scrapeSchedule: vi.fn()
    };
    
    render(<App />);
    
    // Now remove it before the fetch
    await waitFor(() => {
      expect(screen.getByLabelText(/Date/i)).toBeInTheDocument();
    });
    
    delete global.window.electronAPI;
    
    const input = screen.getByLabelText(/Date/i);
    fireEvent.change(input, { target: { value: '13/10/2025' } });
    
    const submitButton = screen.getByText('Rechercher');
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/API Electron non disponible/i)).toBeInTheDocument();
    });
  });
});
