import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import LoadingSpinner from '../../src/components/LoadingSpinner';

describe('LoadingSpinner', () => {
  it('should render loading message', () => {
    render(<LoadingSpinner />);
    expect(screen.getByText(/Récupération de l'emploi du temps magique/i)).toBeInTheDocument();
  });

  it('should render spinner element', () => {
    const { container } = render(<LoadingSpinner />);
    const spinner = container.querySelector('.animate-spin');
    expect(spinner).toBeInTheDocument();
  });
});
