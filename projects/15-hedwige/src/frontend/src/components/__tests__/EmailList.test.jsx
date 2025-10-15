import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import EmailList from '../EmailList';
import { vi } from 'vitest';

describe('EmailList', () => {
  const emails = [
    { id: 1, from: 'Harry Potter <harry@poudlard.fr>', subject: 'Bienvenue à Poudlard', date: '2025-10-10T10:00:00Z' },
    { id: 2, from: 'Hermione Granger <hermione@poudlard.fr>', subject: 'Devoirs', date: '2025-10-11T12:00:00Z' },
  ];

  it('affiche le message si la liste est vide', () => {
    render(<EmailList emails={[]} onEmailClick={() => {}} />);
    expect(screen.getByText(/No emails found/i)).toBeInTheDocument();
  });

  it('affiche la liste des emails', () => {
    render(<EmailList emails={emails} onEmailClick={() => {}} />);
    expect(screen.getByText(/Inbox \(2\)/i)).toBeInTheDocument();
    expect(screen.getByText(/Bienvenue à Poudlard/i)).toBeInTheDocument();
    expect(screen.getByText(/Devoirs/i)).toBeInTheDocument();
  });

  it('appelle onEmailClick lors du clic', () => {
    const handleClick = vi.fn();
    render(<EmailList emails={emails} onEmailClick={handleClick} />);
    fireEvent.click(screen.getByText(/Bienvenue à Poudlard/i));
    expect(handleClick).toHaveBeenCalledWith(1);
  });

  it('correspond au snapshot', () => {
    const { asFragment } = render(<EmailList emails={emails} onEmailClick={() => {}} />);
    expect(asFragment()).toMatchSnapshot();
  });
});

