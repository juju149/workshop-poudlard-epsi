import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import EmailList from '../src/components/EmailList';

describe('EmailList', () => {
  it('renders empty state when no emails', () => {
    render(<EmailList emails={[]} onEmailClick={() => {}} />);
    expect(screen.getByText('No emails found')).toBeDefined();
  });

  it('renders email items', () => {
    const emails = [
      {
        id: '1',
        from: 'Test User <test@example.com>',
        subject: 'Test Subject',
        date: new Date().toISOString(),
        snippet: 'Test snippet'
      }
    ];
    
    render(<EmailList emails={emails} onEmailClick={() => {}} />);
    expect(screen.getByText('Test Subject')).toBeDefined();
    expect(screen.getByText('Test snippet')).toBeDefined();
  });

  it('displays inbox count', () => {
    const emails = [
      { id: '1', from: 'test@example.com', subject: 'Test', date: new Date().toISOString(), snippet: 'test' },
      { id: '2', from: 'test2@example.com', subject: 'Test 2', date: new Date().toISOString(), snippet: 'test 2' }
    ];
    
    render(<EmailList emails={emails} onEmailClick={() => {}} />);
    expect(screen.getByText(/Inbox \(2\)/)).toBeDefined();
  });
});
