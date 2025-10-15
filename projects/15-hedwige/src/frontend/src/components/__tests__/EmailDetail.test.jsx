import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import EmailDetail from '../EmailDetail';
import { vi } from 'vitest';

describe('EmailDetail', () => {
  const email = {
    id: 1,
    from: 'Minerva McGonagall <mcgonagall@poudlard.fr>',
    to: 'Harry Potter <harry@poudlard.fr>',
    subject: 'Bienvenue à Poudlard',
    date: '2025-10-10T10:00:00Z',
    body: 'Cher Harry, bienvenue à Poudlard!'
  };

  it('affiche le message si aucun email n’est sélectionné', () => {
    render(<EmailDetail email={null} onBack={() => {}} />);
    expect(screen.getByText(/Select an email to read/i)).toBeInTheDocument();
  });

  it('affiche les informations de l’email', () => {
    render(<EmailDetail email={email} onBack={() => {}} />);
    // Vérifie que le sujet est bien affiché dans le h2
    const subjects = screen.getAllByText(/Bienvenue à Poudlard/i);
    expect(subjects[0].tagName).toBe('H2');
    expect(screen.getByText(/Minerva McGonagall/i)).toBeInTheDocument();
    expect(screen.getByText(/mcgonagall@poudlard.fr/i)).toBeInTheDocument();
    expect(screen.getByText(/To: Harry Potter <harry@poudlard.fr>/i)).toBeInTheDocument();
    expect(screen.getByText(/Back to Inbox/i)).toBeInTheDocument();
  });

  it('appelle onBack lors du clic sur le bouton', () => {
    const handleBack = vi.fn();
    render(<EmailDetail email={email} onBack={handleBack} />);
    fireEvent.click(screen.getByText(/Back to Inbox/i));
    expect(handleBack).toHaveBeenCalled();
  });

  it('correspond au snapshot', () => {
    const { asFragment } = render(<EmailDetail email={email} onBack={() => {}} />);
    expect(asFragment()).toMatchSnapshot();
  });
});

