import '@testing-library/jest-dom';

// Mock de l'API Electron pour les tests
global.window.electronAPI = {
  getSchedule: jest.fn(),
};

// Mock global de process.exit pour éviter l'arrêt du process pendant les tests
beforeAll(() => {
  jest.spyOn(process, 'exit').mockImplementation(() => {});
});
