import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../App';

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
  });

  it('redirects to login page by default', () => {
    render(<App />);
    expect(window.location.pathname).toBe('/');
  });
});
