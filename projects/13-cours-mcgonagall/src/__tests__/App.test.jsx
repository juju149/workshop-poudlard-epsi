import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App Component', () => {
  test('renders the app with title', () => {
    render(<App />);
    
    // Vérifier que le titre est présent
    const titleElement = screen.getByText(/Emploi du temps - Poudlard/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders with correct styling', () => {
    const { container } = render(<App />);
    
    // Vérifier que le conteneur principal a les bonnes classes
    const mainDiv = container.querySelector('.min-h-screen.bg-gray-100');
    expect(mainDiv).toBeInTheDocument();
  });

  test('renders ScheduleGrid component', () => {
    render(<App />);
    
    // Le ScheduleGrid devrait être présent (on peut vérifier un élément qu'il contient)
    // Par exemple, les boutons de navigation ou le message de chargement
    expect(screen.getByText(/Chargement de l'emploi du temps|←/)).toBeInTheDocument();
  });

  test('has correct container structure', () => {
    const { container } = render(<App />);
    
    const containerDiv = container.querySelector('.container.mx-auto.px-4.py-8');
    expect(containerDiv).toBeInTheDocument();
  });

  test('title has correct styling classes', () => {
    render(<App />);
    
    const titleElement = screen.getByText(/Emploi du temps - Poudlard/i);
    expect(titleElement).toHaveClass('text-4xl', 'font-bold', 'text-center', 'text-gray-800', 'mb-8');
  });
});
