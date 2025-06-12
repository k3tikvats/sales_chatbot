import '@testing-library/jest-dom';

// Mock localStorage
const localStorageMock = {
  getItem: () => null,
  setItem: () => {},
  removeItem: () => {},
  clear: () => {},
  length: 0,
  key: () => null,
};

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock
});

// Mock fetch
global.fetch = () => Promise.resolve({
  ok: true,
  json: () => Promise.resolve({}),
} as Response);
