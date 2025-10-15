import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import PatronusLoader from '../PatronusLoader'

describe('PatronusLoader', () => {
  beforeEach(() => {
    jest.useFakeTimers()
  })

  afterEach(() => {
    jest.restoreAllMocks()
    jest.useRealTimers()
  })

  it('devrait afficher le composant avec le texte de chargement', () => {
    render(<PatronusLoader />)
    expect(screen.getByText(/Chargement de l'emploi du temps/i)).toBeInTheDocument()
  })

  it('devrait afficher le conteneur du Patronus', () => {
    const { container } = render(<PatronusLoader />)
    const patronusContainer = container.querySelector('.patronus-container')
    expect(patronusContainer).toBeInTheDocument()
  })

  it('devrait afficher les éléments visuels (foret, fond, blaireau)', () => {
    const { container } = render(<PatronusLoader />)
    
    const foret = container.querySelector('.foret')
    const fond = container.querySelector('.fond')
    const blaireau = container.querySelector('.blaireau')
    
    expect(foret).toBeInTheDocument()
    expect(fond).toBeInTheDocument()
    expect(blaireau).toBeInTheDocument()
  })

  it('devrait créer des éléments "voile" au fil du temps', async () => {
    const { container } = render(<PatronusLoader />)
    const patronusContainer = container.querySelector('.patronus-container')
    
    // Initialement pas de voile
    let voiles = patronusContainer.querySelectorAll('.voile')
    expect(voiles.length).toBe(0)
    
    // Avancer le temps de 150ms (interval = 120ms)
    jest.advanceTimersByTime(150)
    
    await waitFor(() => {
      voiles = patronusContainer.querySelectorAll('.voile')
      expect(voiles.length).toBeGreaterThan(0)
    })
  })

  it('devrait nettoyer les intervalles au démontage', () => {
    const clearIntervalSpy = jest.spyOn(global, 'clearInterval')
    const { unmount } = render(<PatronusLoader />)
    
    unmount()
    
    expect(clearIntervalSpy).toHaveBeenCalled()
  })

  it('devrait correspondre au snapshot', () => {
    const { container } = render(<PatronusLoader />)
    expect(container).toMatchSnapshot()
  })
})
