import React, { useEffect, useRef } from 'react'
import './PatronusLoader.css'

const PatronusLoader = () => {
  const containerRef = useRef(null)

  useEffect(() => {
    const container = containerRef.current
    if (!container) return

    const createVoile = () => {
      const voile = document.createElement('div')
      voile.className = 'voile'
      
      // Position aléatoire autour du blaireau (évite le centre)
      const rMax = 210 - 90 // rayon max = rayon cercle - moitié largeur voile
      const rMin = 110 // rayon min = bord du blaireau (80% du cercle ~200px, donc ~100px du centre)
      const angle = Math.random() * 2 * Math.PI
      const radius = rMin + Math.random() * (rMax - rMin)
      const cx = 250, cy = 250
      const x = cx + Math.cos(angle) * radius - 90
      const y = cy + Math.sin(angle) * radius - 45
      
      voile.style.left = `${x}px`
      voile.style.top = `${y}px`
      
      container.appendChild(voile)
      setTimeout(() => voile.remove(), 3500)
    }

    const interval = setInterval(createVoile, 120)

    return () => {
      clearInterval(interval)
    }
  }, [])

  return (
    <div className="patronus-loader-wrapper">
      <div className="patronus-container" id="container" ref={containerRef}>
        <div className="foret"></div>
        <div className="fond"></div>
        <div className="blaireau"></div>
      </div>
      <p className="patronus-text">Chargement de l'emploi du temps...</p>
    </div>
  )
}

export default PatronusLoader
