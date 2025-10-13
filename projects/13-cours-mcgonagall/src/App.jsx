import React from 'react'
import ScheduleGrid from './components/ScheduleGrid'

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-8">
          📚 Emploi du temps - Poudlard
        </h1>
        <ScheduleGrid />
      </div>
    </div>
  )
}

export default App