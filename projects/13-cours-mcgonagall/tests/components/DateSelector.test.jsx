import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import DateSelector from '../../src/components/DateSelector';

describe('DateSelector', () => {
  it('should render date input field', () => {
    render(<DateSelector onDateSelect={vi.fn()} disabled={false} />);
    const input = screen.getByLabelText(/Date/i);
    expect(input).toBeInTheDocument();
  });

  it('should render search and today buttons', () => {
    render(<DateSelector onDateSelect={vi.fn()} disabled={false} />);
    expect(screen.getByText('Rechercher')).toBeInTheDocument();
    expect(screen.getByText('Aujourd\'hui')).toBeInTheDocument();
  });

  it('should call onDateSelect when form is submitted with a date', () => {
    const mockOnDateSelect = vi.fn();
    render(<DateSelector onDateSelect={mockOnDateSelect} disabled={false} />);
    
    const input = screen.getByLabelText(/Date/i);
    const submitButton = screen.getByText('Rechercher');
    
    fireEvent.change(input, { target: { value: '13/10/2025' } });
    fireEvent.click(submitButton);
    
    expect(mockOnDateSelect).toHaveBeenCalledWith('13/10/2025');
  });

  it('should call onDateSelect with today\'s date when today button is clicked', () => {
    const mockOnDateSelect = vi.fn();
    render(<DateSelector onDateSelect={mockOnDateSelect} disabled={false} />);
    
    const todayButton = screen.getByText('Aujourd\'hui');
    fireEvent.click(todayButton);
    
    expect(mockOnDateSelect).toHaveBeenCalled();
    const calledDate = mockOnDateSelect.mock.calls[0][0];
    expect(calledDate).toMatch(/\d{2}\/\d{2}\/\d{4}/);
  });

  it('should disable inputs when disabled prop is true', () => {
    render(<DateSelector onDateSelect={vi.fn()} disabled={true} />);
    
    const input = screen.getByLabelText(/Date/i);
    const submitButton = screen.getByText('Rechercher');
    const todayButton = screen.getByText('Aujourd\'hui');
    
    expect(input).toBeDisabled();
    expect(submitButton).toBeDisabled();
    expect(todayButton).toBeDisabled();
  });

  it('should not submit form if date is empty', () => {
    const mockOnDateSelect = vi.fn();
    render(<DateSelector onDateSelect={mockOnDateSelect} disabled={false} />);
    
    const form = screen.getByRole('button', { name: /Rechercher/i }).closest('form');
    fireEvent.submit(form);
    
    expect(mockOnDateSelect).not.toHaveBeenCalled();
  });
});
