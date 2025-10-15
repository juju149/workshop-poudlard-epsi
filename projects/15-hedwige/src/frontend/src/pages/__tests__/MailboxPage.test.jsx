import React from 'react';
import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import MailboxPage from '../MailboxPage';

describe('MailboxPage', () => {
  it('correspond au snapshot', () => {
    const { asFragment } = render(
      <MemoryRouter>
        <MailboxPage />
      </MemoryRouter>
    );
    expect(asFragment()).toMatchSnapshot();
  });
});
