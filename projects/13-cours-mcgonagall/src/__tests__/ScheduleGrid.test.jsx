import React from 'react';
import { render, screen, waitFor, fireEvent, act } from '@testing-library/react';
import ScheduleGrid from '../components/ScheduleGrid';

// Mock des données de test
const mockScheduleData = [
  {
    date: 'Lundi 14/10/2025',
    cours: [
      { matiere: 'Potions', prof: 'Severus Rogue', salle: 'Cachots', heure: '09:00-11:00' },
      { matiere: 'Défense contre les forces du Mal', prof: 'Remus Lupin', salle: 'Tour Nord', heure: '14:00-16:00' }
    ]
  },
  {
    date: 'Mardi 15/10/2025',
    cours: [
      { matiere: 'Métamorphose', prof: 'Minerva McGonagall', salle: 'Salle 1B', heure: '10:00-12:00' }
    ]
  },
  {
    date: 'Mercredi 16/10/2025',
    cours: []
  },
  {
    date: 'Jeudi 17/10/2025',
    cours: [
      { matiere: 'Sortilèges', prof: 'Filius Flitwick', salle: 'Salle 2E', heure: '08:00-10:00' }
    ]
  },
  {
    date: 'Vendredi 18/10/2025',
    cours: [
      { matiere: 'Histoire de la Magie', prof: 'Cuthbert Binns', salle: 'Amphithéâtre', heure: '13:00-15:00' }
    ]
  }
];

// Fonction utilitaire pour créer une promesse résolue pour les mocks
const createResolvedPromise = (value) => {
  let resolve;
  const promise = new Promise(r => { resolve = r; });
  promise.resolve = () => resolve(value);
  return promise;
};

describe('ScheduleGrid Component', () => {
  beforeEach(() => {
    // Reset des mocks avant chaque test
    jest.clearAllMocks();
    
    // Utiliser une date fixe pour les tests
    jest.useFakeTimers();
    jest.setSystemTime(new Date('2025-10-14'));
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  test('renders loading state initially', async () => {
    const promise = createResolvedPromise({});
    window.electronAPI.getSchedule = jest.fn(() => promise);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    expect(screen.getByText(/Chargement de l'emploi du temps/i)).toBeInTheDocument();
  });

  test('renders error state when API fails', async () => {
    const mockResult = {
      success: false,
      error: 'Erreur de connexion'
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    expect(screen.getByText(/Erreur de connexion/i)).toBeInTheDocument();
  });

  test('renders retry button on error', async () => {
    const mockResult = {
      success: false,
      error: 'Erreur de connexion'
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    const retryButton = screen.getByText(/Réessayer/i);
    expect(retryButton).toBeInTheDocument();
  });

  test('renders schedule when data is loaded successfully', async () => {
    const mockResult = {
      success: true,
      data: mockScheduleData
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    expect(screen.getByText('Potions')).toBeInTheDocument();
    expect(screen.getByText(/Severus Rogue/i)).toBeInTheDocument();
  });

  test('renders all days of the week', async () => {
    const mockResult = {
      success: true,
      data: mockScheduleData
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    expect(screen.getByText('Lundi')).toBeInTheDocument();
    expect(screen.getByText('Mardi')).toBeInTheDocument();
    expect(screen.getByText('Mercredi')).toBeInTheDocument();
    expect(screen.getByText('Jeudi')).toBeInTheDocument();
    expect(screen.getByText('Vendredi')).toBeInTheDocument();
  });

  test('renders time slots correctly', async () => {
    const mockResult = {
      success: true,
      data: mockScheduleData
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    expect(screen.getByText('08:00')).toBeInTheDocument();
    expect(screen.getByText('09:00')).toBeInTheDocument();
    expect(screen.getByText('10:00')).toBeInTheDocument();
  });

  test('changes week when clicking navigation buttons', async () => {
    const mockResult = {
      success: true,
      data: mockScheduleData
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    expect(screen.getByText('Potions')).toBeInTheDocument();

    await act(async () => {
      const nextWeekButton = screen.getByText('→');
      fireEvent.click(nextWeekButton);
    });
    
    // Attendre que toutes les promesses soient résolues après le clic
    await act(async () => {
      await Promise.resolve();
    });
    
    // L'API devrait être appelée une deuxième fois
    expect(window.electronAPI.getSchedule).toHaveBeenCalledTimes(2);
  });

  test('displays course information correctly', async () => {
    const mockResult = {
      success: true,
      data: mockScheduleData
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    // Vérifier qu'un cours est affiché avec toutes ses informations
    expect(screen.getByText('Potions')).toBeInTheDocument();
    expect(screen.getByText(/Severus Rogue/i)).toBeInTheDocument();
    expect(screen.getByText('Cachots')).toBeInTheDocument();
  });

  test('shows warning message when electronAPI is not available', async () => {
    const originalElectronAPI = window.electronAPI;
    window.electronAPI = undefined;
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    expect(screen.getByText(/Veuillez lancer l'application avec Electron/i)).toBeInTheDocument();
    
    window.electronAPI = originalElectronAPI;
  });

  test('displays course count information', async () => {
    const mockResult = {
      success: true,
      data: mockScheduleData
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    expect(screen.getByText(/cours cette semaine/i)).toBeInTheDocument();
  });

  test('handles retry button click', async () => {
    window.electronAPI.getSchedule = jest.fn()
      .mockResolvedValueOnce({
        success: false,
        error: 'Erreur temporaire'
      })
      .mockResolvedValueOnce({
        success: true,
        data: mockScheduleData
      });
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    expect(screen.getByText(/Erreur temporaire/i)).toBeInTheDocument();

    await act(async () => {
      const retryButton = screen.getByText(/Réessayer/i);
      fireEvent.click(retryButton);
    });
    
    // Attendre que toutes les promesses soient résolues après le clic
    await act(async () => {
      await Promise.resolve();
    });
    
    expect(screen.getByText('Potions')).toBeInTheDocument();
  });

  test('formats professor names correctly', async () => {
    const mockResult = {
      success: true,
      data: [
        {
          date: 'Lundi 14/10/2025',
          cours: [
            { matiere: 'Test', prof: 'jean dupont', salle: 'A1', heure: '09:00-11:00' }
          ]
        }
      ]
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    expect(screen.getByText(/Jean Dupont/i)).toBeInTheDocument();
  });

  test('displays week range in header', async () => {
    const mockResult = {
      success: true,
      data: mockScheduleData
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    expect(screen.getByText(/Semaine du/i)).toBeInTheDocument();
  });

  test('fusionne les cours consécutifs sur plusieurs créneaux', async () => {
    const mockResult = {
      success: true,
      data: [
        {
          date: 'Lundi 14/10/2025',
          cours: [
            { matiere: 'Potions', prof: 'Severus Rogue', salle: 'Cachots', heure: '08:00-10:00' },
            { matiere: 'Potions', prof: 'Severus Rogue', salle: 'Cachots', heure: '10:00-12:00' }
          ]
        },
        { date: 'Mardi 15/10/2025', cours: [] },
        { date: 'Mercredi 16/10/2025', cours: [] },
        { date: 'Jeudi 17/10/2025', cours: [] },
        { date: 'Vendredi 18/10/2025', cours: [] }
      ]
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    // Le cours doit être fusionné sur 4h (08:00 à 12:00)
    expect(screen.getByText('Potions')).toBeInTheDocument();
    expect(screen.getByText(/Severus Rogue/)).toBeInTheDocument();
    expect(screen.getByText('Cachots')).toBeInTheDocument();
    
    // Vérifie qu'il n'y a qu'une seule cellule "Potions" affichée
    expect(screen.getAllByText('Potions').length).toBe(1);
  });

  test('affiche une cellule cachée pour les créneaux déjà occupés', async () => {
    const mockResult = {
      success: true,
      data: [
        {
          date: 'Lundi 14/10/2025',
          cours: [
            { matiere: 'Sortilèges', prof: 'Filius Flitwick', salle: 'Salle 2E', heure: '09:00-11:00' }
          ]
        },
        { date: 'Mardi 15/10/2025', cours: [] },
        { date: 'Mercredi 16/10/2025', cours: [] },
        { date: 'Jeudi 17/10/2025', cours: [] },
        { date: 'Vendredi 18/10/2025', cours: [] }
      ]
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    // La cellule "hidden" pour 10:00 doit exister
    const hiddenCells = document.querySelectorAll('.hidden');
    expect(hiddenCells.length).toBeGreaterThan(0);
  });

  test('ne fusionne pas les cours si trou entre deux créneaux', async () => {
    const mockResult = {
      success: true,
      data: [
        {
          date: 'Lundi 14/10/2025',
          cours: [
            { matiere: 'Potions', prof: 'Severus Rogue', salle: 'Cachots', heure: '08:00-09:00' },
            { matiere: 'Potions', prof: 'Severus Rogue', salle: 'Cachots', heure: '10:00-12:00' }
          ]
        },
        { date: 'Mardi 15/10/2025', cours: [] },
        { date: 'Mercredi 16/10/2025', cours: [] },
        { date: 'Jeudi 17/10/2025', cours: [] },
        { date: 'Vendredi 18/10/2025', cours: [] }
      ]
    };
    
    window.electronAPI.getSchedule = jest.fn().mockResolvedValue(mockResult);
    
    await act(async () => {
      render(<ScheduleGrid />);
    });
    
    // Attendre que toutes les promesses soient résolues
    await act(async () => {
      await Promise.resolve();
    });
    
    // Les deux cours doivent être affichés séparément
    expect(screen.getAllByText('Potions').length).toBe(2);
  });
});
