import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Configuration globale pour tous les tests
global.console = {
  ...console,
  // Désactiver certains logs pendant les tests si nécessaire
  log: vi.fn(),
  debug: vi.fn(),
  info: vi.fn(),
  warn: vi.fn(),
  error: vi.fn(),
};

// Mock pour les variables d'environnement
process.env.VITE_API_BASE_URL = 'http://localhost:3000';