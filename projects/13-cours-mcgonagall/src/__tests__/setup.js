import '@testing-library/jest-dom';

// Mock de l'API Electron pour les tests
global.window.electronAPI = {
  getSchedule: jest.fn(),
};
