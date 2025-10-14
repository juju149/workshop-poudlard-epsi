import React from 'react';
import { render, screen, act } from '@testing-library/react';
import App from '../App';

// Mock du composant ScheduleGrid pour éviter les appels asynchrones
jest.mock('../components/ScheduleGrid', () => {
  return function MockScheduleGrid() {
    return <div data-testid="mock-schedule-grid">Contenu mockée de ScheduleGrid</div>;
  };
});

describe('App Component', () => {
  test('renders the app with title', async () => {
    await act(async () => {
      render(<App />);
    });
    
    // Vérifier que le titre est présent
    const titleElement = screen.getByText(/Emploi du temps - Poudlard/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders with correct styling', async () => {
    let container;
    await act(async () => {
      const renderResult = render(<App />);
      container = renderResult.container;
    });
    
    // Vérifier que le conteneur principal a les bonnes classes
    const mainDiv = container.querySelector('.min-h-screen.bg-gray-100');
    expect(mainDiv).toBeInTheDocument();
  });

  test('renders ScheduleGrid component', async () => {
    await act(async () => {
      render(<App />);
    });
    
    // Vérifier que le composant mockée est bien rendu
    expect(screen.getByTestId('mock-schedule-grid')).toBeInTheDocument();
  });

  test('has correct container structure', async () => {
    let container;
    await act(async () => {
      const renderResult = render(<App />);
      container = renderResult.container;
    });
    
    const containerDiv = container.querySelector('.container.mx-auto.px-4.py-8');
    expect(containerDiv).toBeInTheDocument();
  });

  test('title has correct styling classes', async () => {
    await act(async () => {
      render(<App />);
    });
    
    const titleElement = screen.getByText(/Emploi du temps - Poudlard/i);
    expect(titleElement).toHaveClass('text-4xl', 'font-bold', 'text-center', 'text-gray-800', 'mb-8');
  });
});
