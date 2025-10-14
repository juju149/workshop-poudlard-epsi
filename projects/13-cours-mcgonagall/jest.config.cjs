module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
  moduleFileExtensions: ['js', 'jsx'],
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  setupFilesAfterEnv: ['<rootDir>/src/__tests__/setup.js'],
  collectCoverageFrom: [
    'src/**/*.{js,jsx}',
    'scraper.js',
    '!src/main.jsx',
    '!src/**/*.test.{js,jsx}',
    '!src/__tests__/**',
    '!**/node_modules/**',
    '!**/coverage/**',
  ],
  coverageThreshold: {
    global: {
      branches: 63,
      functions: 76,
      lines: 78,
      statements: 76,
    },
  },
  testMatch: [
    '**/__tests__/**/*.test.{js,jsx}',
    '**/*.test.{js,jsx}',
  ],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
};
