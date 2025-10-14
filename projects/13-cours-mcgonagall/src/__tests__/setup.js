import '@testing-library/jest-dom';

// Mock de l'API Electron pour les tests
global.window.electronAPI = {
  getSchedule: jest.fn(),
};

// Mock global de process.exit pour éviter l'arrêt du process pendant les tests
beforeAll(() => {
  jest.spyOn(process, 'exit').mockImplementation(() => {});
});

// Désactiver les messages console pendant les tests
// Pour réactiver les messages console, exécuter avec VERBOSE=true npm test
if (process.env.VERBOSE !== 'true') {
  // Stocker les fonctions originales
  const originalError = console.error;
  const originalWarn = console.warn;
  const originalLog = console.log;
  
  // Remplacer par des mocks
  beforeAll(() => {
    console.error = jest.fn();
    console.warn = jest.fn();
    console.log = jest.fn();
  });
  
  // Restaurer après tous les tests
  afterAll(() => {
    console.error = originalError;
    console.warn = originalWarn;
    console.log = originalLog;
  });
}
