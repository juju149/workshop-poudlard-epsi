import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import LoginPage from '../../src/pages/LoginPage';
import MailboxPage from '../../src/pages/MailboxPage';

// Mock de l'API
const mockFetch = vi.fn();
global.fetch = mockFetch;

describe('Tests d\'intégration - Flux de connexion utilisateur', () => {
  beforeEach(() => {
    mockFetch.mockClear();
    localStorage.clear();
  });

  it('permet à un utilisateur de se connecter avec des informations valides', async () => {
    const user = userEvent.setup();
    const mockOnLogin = vi.fn();
    
    // Mock de la réponse de l'API pour l'authentification
    mockFetch.mockResolvedValue({
      ok: true,
      json: async () => ({
        success: true,
        sessionId: 'mock-session-id',
        user: {
          id: 1,
          username: 'harry.potter@poudlard.fr',
          email: 'harry.potter@poudlard.fr'
        }
      })
    });
    
    render(
      <MemoryRouter>
        <LoginPage onLogin={mockOnLogin} />
      </MemoryRouter>
    );

    // Vérifier que nous sommes sur la page de connexion
    expect(screen.getByText(/connecte-toi/i)).toBeInTheDocument();
    
    // Remplir le formulaire de connexion
    const emailInput = screen.getByLabelText(/adresse outlook/i);
    const passwordInput = screen.getByLabelText(/mot de passe/i);
    const submitButton = screen.getByRole('button', { name: /se connecter/i });

    await user.type(emailInput, 'harry.potter@poudlard.fr');
    await user.type(passwordInput, 'motdepasse123');
    await user.click(submitButton);

    // Attendre que la fonction onLogin soit appelée
    await waitFor(() => {
      expect(mockOnLogin).toHaveBeenCalledWith(
        'mock-session-id',
        {
          id: 1,
          username: 'harry.potter@poudlard.fr',
          email: 'harry.potter@poudlard.fr'
        }
      );
    });

    // Vérifier que l'API d'authentification a été appelée
    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/auth/login'),
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        }),
        body: JSON.stringify({
          email: 'harry.potter@poudlard.fr',
          password: 'motdepasse123'
        })
      })
    );
  });

  it('affiche une erreur en cas d\'échec de connexion', async () => {
    const user = userEvent.setup();
    const mockOnLogin = vi.fn();
    
    // Mock d'une réponse d'erreur
    mockFetch.mockResolvedValue({
      ok: false,
      json: async () => ({
        success: false,
        message: 'Email ou mot de passe incorrect'
      })
    });

    render(
      <MemoryRouter>
        <LoginPage onLogin={mockOnLogin} />
      </MemoryRouter>
    );

    // Remplir le formulaire avec de mauvaises informations
    const emailInput = screen.getByLabelText(/adresse outlook/i);
    const passwordInput = screen.getByLabelText(/mot de passe/i);
    const submitButton = screen.getByRole('button', { name: /se connecter/i });

    await user.type(emailInput, 'mauvais@email.com');
    await user.type(passwordInput, 'mauvais-mot-de-passe');
    await user.click(submitButton);

    // Vérifier que le message d'erreur s'affiche
    await waitFor(() => {
      expect(screen.getByText(/login failed/i)).toBeInTheDocument();
    });

    // Vérifier que onLogin n'a pas été appelée
    expect(mockOnLogin).not.toHaveBeenCalled();

    // Vérifier que nous sommes toujours sur la page de connexion
    expect(screen.getByText(/connecte-toi/i)).toBeInTheDocument();
  });

  it('teste l\'intégration complète - affichage de la boîte mail après connexion', async () => {
    const sessionId = 'test-session-123';
    const userData = {
      id: 1,
      username: 'harry.potter',
      email: 'harry.potter@poudlard.fr'
    };

    render(
      <MemoryRouter>
        <MailboxPage 
          sessionId={sessionId} 
          user={userData} 
          onLogout={vi.fn()} 
        />
      </MemoryRouter>
    );

    // Vérifier que la boîte mail s'affiche avec les éléments principaux
    expect(screen.getByText(/hedwige/i)).toBeInTheDocument();
    expect(screen.getByText(/inbox/i)).toBeInTheDocument();
    expect(screen.getByText(/compose/i)).toBeInTheDocument();
    expect(screen.getByText(/mail reçu/i)).toBeInTheDocument();

    // Vérifier qu'un email est affiché (utiliser les emails par défaut du composant)
    expect(screen.getByText(/minerva mcgonagall/i)).toBeInTheDocument();
    expect(screen.getByText(/bienvenue à poudlard/i)).toBeInTheDocument();
    expect(screen.getByText(/hermione granger/i)).toBeInTheDocument();
    expect(screen.getByText(/devoirs/i)).toBeInTheDocument();
  });
});