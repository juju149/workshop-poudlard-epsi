import React, { useState, useEffect } from 'react'

const ScheduleGrid = () => {
  const [scheduleData, setScheduleData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [currentWeekStart, setCurrentWeekStart] = useState(null)
  
  const timeSlots = [
    '08:00', '09:00', '10:00', '11:00', '12:00', 
    '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'
  ]
  
  const daysOfWeek = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']

  // Calculer le lundi de la semaine courante
  useEffect(() => {
    const today = new Date()
    const dayOfWeek = today.getDay()
    const daysToSubtract = dayOfWeek === 0 ? 6 : dayOfWeek - 1
    const monday = new Date(today)
    monday.setDate(today.getDate() - daysToSubtract)
    setCurrentWeekStart(monday)
  }, [])

  // Charger les données de l'emploi du temps via Electron IPC
  const loadSchedule = async () => {
    if (!currentWeekStart) return

    try {
      setLoading(true)
      setError(null)
      
      // Formater la date du lundi au format JJ/MM/AAAA
      const mondayFormatted = currentWeekStart.toLocaleDateString('fr-FR')
      
      // Vérifier si on est dans Electron
      if (window.electronAPI && window.electronAPI.getSchedule) {
        // Mode Electron - Utiliser l'IPC
        const result = await window.electronAPI.getSchedule(mondayFormatted)
        
        if (result.success) {
          setScheduleData(result.data)
        } else {
          setError(result.error || 'Erreur inconnue')
        }
      } else {
        // Mode développement navigateur - Données mockées
        console.warn('⚠️ Mode développement : Electron API non disponible, utilisation de données mockées')
        setError('Veuillez lancer l\'application avec Electron pour récupérer les vraies données (npm run dev)')
      }
    } catch (err) {
      console.error('Erreur lors du chargement des données:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadSchedule()
  }, [currentWeekStart])

  // Fonction pour trouver le cours correspondant à un jour et une heure
  const getCourseForSlot = (dayIndex, timeSlot) => {
    if (!scheduleData || scheduleData.length === 0) return null
    
    // Trouver le jour correspondant
    const dayData = scheduleData[dayIndex]
    if (!dayData || !dayData.cours) return null
    
    // Chercher un cours qui commence à cette heure
    const course = dayData.cours.find(c => c.heure.startsWith(timeSlot))
    return course
  }

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-700 mx-auto"></div>
        <p className="mt-4 text-gray-600">Chargement de l'emploi du temps...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-red-800 mb-2">⚠️ Erreur</h3>
          <p className="text-red-600">{error}</p>
          <button 
            onClick={loadSchedule}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            Réessayer
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="mb-4 flex justify-between items-center">
        <h2 className="text-2xl font-bold text-purple-800">
          Semaine du {currentWeekStart?.toLocaleDateString('fr-FR')}
        </h2>
        <button 
          onClick={loadSchedule}
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          🔄 Actualiser
        </button>
      </div>

      <div className="grid grid-cols-6 gap-2">
        {/* En-tête vide pour la colonne des heures */}
        <div className="p-3 bg-purple-100 rounded-lg font-semibold text-center text-purple-800">
          Heures
        </div>
        
        {/* En-têtes des jours */}
        {daysOfWeek.map((day, index) => (
          <div key={day} className="p-3 bg-purple-100 rounded-lg font-semibold text-center text-purple-800">
            {day}
            {scheduleData[index]?.date && (
              <div className="text-xs font-normal text-purple-600 mt-1">
                {scheduleData[index].date}
              </div>
            )}
          </div>
        ))}
        
        {/* Grille de l'emploi du temps */}
        {timeSlots.map((time) => (
          <React.Fragment key={time}>
            {/* Colonne des heures */}
            <div className="p-3 bg-gray-50 rounded-lg font-medium text-center text-gray-600 border">
              {time}
            </div>
            
            {/* Cellules pour chaque jour */}
            {daysOfWeek.map((day, dayIndex) => {
              const course = getCourseForSlot(dayIndex, time)
              
              return (
                <div 
                  key={`${day}-${time}`}
                  className={`p-3 min-h-[60px] border-2 rounded-lg transition-colors duration-200 ${
                    course 
                      ? 'bg-purple-50 border-purple-300 hover:bg-purple-100' 
                      : 'border-dashed border-gray-200 hover:border-purple-300 hover:bg-purple-50'
                  }`}
                >
                  {course ? (
                    <div className="text-sm">
                      <div className="font-bold text-purple-900">{course.matiere}</div>
                      <div className="text-purple-700 text-xs mt-1">{course.prof}</div>
                      <div className="text-purple-600 text-xs">{course.salle}</div>
                      <div className="text-gray-500 text-xs mt-1">{course.heure}</div>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center text-gray-400 text-sm h-full">
                      Libre
                    </div>
                  )}
                </div>
              )
            })}
          </React.Fragment>
        ))}
      </div>
      
      {/* Légende */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold text-gray-700 mb-2">📖 Informations</h3>
        <p className="text-gray-600">
          {scheduleData.length > 0 
            ? `${scheduleData.reduce((total, day) => total + (day.cours?.length || 0), 0)} cours cette semaine`
            : 'Aucun cours cette semaine'}
        </p>
      </div>
    </div>
  )
}

export default ScheduleGrid