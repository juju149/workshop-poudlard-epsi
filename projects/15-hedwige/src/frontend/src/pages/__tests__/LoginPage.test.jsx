import React from 'react';
import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import LoginPage from '../LoginPage';

describe('LoginPage', () => {
  it('correspond au snapshot', () => {
    const { asFragment } = render(
      <MemoryRouter>
        <LoginPage />
      </MemoryRouter>
    );
    expect(asFragment()).toMatchSnapshot();
  });
});
