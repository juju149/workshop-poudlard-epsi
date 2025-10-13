import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ErrorMessage from '../../src/components/ErrorMessage';

describe('ErrorMessage', () => {
  it('should render error message', () => {
    render(<ErrorMessage message="Test error message" />);
    expect(screen.getByText('Test error message')).toBeInTheDocument();
  });

  it('should render error title', () => {
    render(<ErrorMessage message="Test error" />);
    expect(screen.getByText('Erreur')).toBeInTheDocument();
  });

  it('should call onDismiss when close button is clicked', () => {
    const mockOnDismiss = vi.fn();
    render(<ErrorMessage message="Test error" onDismiss={mockOnDismiss} />);
    
    const closeButton = screen.getByLabelText('Fermer');
    fireEvent.click(closeButton);
    
    expect(mockOnDismiss).toHaveBeenCalledTimes(1);
  });

  it('should not render close button when onDismiss is not provided', () => {
    render(<ErrorMessage message="Test error" />);
    expect(screen.queryByLabelText('Fermer')).not.toBeInTheDocument();
  });
});
