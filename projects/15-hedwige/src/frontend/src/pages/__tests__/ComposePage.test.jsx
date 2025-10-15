import React from 'react';
import { render } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import ComposePage from '../ComposePage';

describe('ComposePage', () => {
  it('correspond au snapshot', () => {
    const { asFragment } = render(
      <MemoryRouter>
        <ComposePage />
      </MemoryRouter>
    );
    expect(asFragment()).toMatchSnapshot();
  });
});
