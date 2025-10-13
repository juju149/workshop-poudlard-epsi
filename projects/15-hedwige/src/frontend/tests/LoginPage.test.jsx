import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import LoginPage from '../src/pages/LoginPage';

describe('LoginPage', () => {
  it('renders login page', () => {
    const mockOnLogin = vi.fn();
    render(
      <BrowserRouter>
        <LoginPage onLogin={mockOnLogin} />
      </BrowserRouter>
    );
    
    expect(screen.getByText('Hedwige')).toBeDefined();
    expect(screen.getByText('Sign in with Google')).toBeDefined();
  });

  it('has Google login button', () => {
    const mockOnLogin = vi.fn();
    render(
      <BrowserRouter>
        <LoginPage onLogin={mockOnLogin} />
      </BrowserRouter>
    );
    
    const loginButton = screen.getByText('Sign in with Google');
    expect(loginButton).toBeDefined();
  });
});
