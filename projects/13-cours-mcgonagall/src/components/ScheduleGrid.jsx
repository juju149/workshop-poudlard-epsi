import React, { useState, useEffect } from 'react'

const ScheduleGrid = () => {
  // Changer de semaine
  const changeWeek = (offset) => {
    if (!currentWeekStart) return;
    const newMonday = new Date(currentWeekStart);
    newMonday.setDate(currentWeekStart.getDate() + offset * 7);
    setCurrentWeekStart(newMonday);
  }
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
      const mondayFormatted = currentWeekStart.toLocaleDateString('en-US');
      // Vérifier si on est dans Electron
      if (window.electronAPI && window.electronAPI.getSchedule) {
        // Mode Electron - Utiliser l'IPC
        const result = await window.electronAPI.getSchedule(mondayFormatted);

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
  // Amélioration : affiche le cours sur toute la plage horaire (ex: 9h-11h sur 9h et 10h, mais pas 11h)
  const getCourseForSlot = (dayIndex, timeSlot) => {
    if (!scheduleData || scheduleData.length === 0) return null
    const dayData = scheduleData[dayIndex]
    if (!dayData || !dayData.cours) return null

    // On cherche un cours dont la plage horaire inclut l'heure du créneau
    // Format attendu : "09:00-11:00" ou "9h-11h" ou "09h00-11h00"
    return dayData.cours.find(c => {
      if (!c.heure) return false
      // Extraction des heures de début et fin
      const match = c.heure.match(/(\d{1,2})[h:]?(\d{0,2})\s*[-–]\s*(\d{1,2})[h:]?(\d{0,2})/)
      if (match) {
        let startHour = parseInt(match[1], 10)
        let endHour = parseInt(match[3], 10)
        // Si minutes présentes, on peut les utiliser mais ici on reste à l'heure pleine
        let slotHour = parseInt(timeSlot.split(':')[0], 10)
        return slotHour >= startHour && slotHour < endHour // < au lieu de <= pour exclure l'heure de fin
      }
      // Si le format est juste une heure, on compare directement
      return c.heure.startsWith(timeSlot)
    })
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
      <div className="mb-4 flex justify-center items-center gap-4">
        <button
          onClick={() => changeWeek(-1)}
          className="px-3 py-2 bg-purple-200 text-purple-800 rounded-lg hover:bg-purple-300 transition-colors"
        >
          ←
        </button>
        <h2 className="text-2xl font-bold text-purple-800">
          {(() => {
            if (!currentWeekStart) return '';
            const lundi = currentWeekStart;
            const vendredi = new Date(lundi);
            vendredi.setDate(lundi.getDate() + 4);
            return `Semaine du ${lundi.toLocaleDateString('fr-FR')} au ${vendredi.toLocaleDateString('fr-FR')}`;
          })()}
        </h2>
        <button
          onClick={() => changeWeek(1)}
          className="px-3 py-2 bg-purple-200 text-purple-800 rounded-lg hover:bg-purple-300 transition-colors"
        >
          →
        </button>
      </div>

      <div className="relative grid grid-cols-6 gap-x-2">
        {/* Lignes horizontales pour les heures */}
        <div className="absolute w-full" style={{ zIndex: 0 }}>
          {timeSlots.map((time, index) => (
            <div
              key={time}
              className="border-t border-gray-200 relative"
              style={{
                position: 'absolute',
                left: 0,
                right: 0,
                top: `${48 + (index * 60)}px`, // 48px pour l'en-tête + index * 60px pour chaque ligne
              }}
            >
              <span className="absolute top-1 left-3 text-xs text-gray-500">{time}</span>
            </div>
          ))}
        </div>

        {/* Espace vide pour la colonne des heures */}
        <div className="h-12 relative z-10" />
        
        {/* En-têtes des jours */}
        {daysOfWeek.map((day, index) => (
          <div key={day} className="h-12 relative z-10">
            <div className="absolute top-0 left-0 right-0 bottom-0 bg-purple-100 rounded-lg flex flex-col items-center justify-center p-2">
              <div className="font-semibold text-purple-800">
                {day}
              </div>
              {scheduleData[index]?.date && (
                <div className="text-xs font-normal text-purple-600">
                  {scheduleData[index].date.replace(/^\S+\s*/, '')}
                </div>
              )}
            </div>
          </div>
        ))}
        
        {/* Grille de l'emploi du temps */}
        {timeSlots.map((time, timeIndex) => (
          <React.Fragment key={time}>
            {/* Colonne des heures - maintenant vide car affichée en absolu */}
            <div className="h-[60px]" />
            
            {/* Cellules pour chaque jour */}
            {daysOfWeek.map((day, dayIndex) => {
              // Ne pas afficher si cette cellule fait partie d'un cours fusionné précédent
              if (timeIndex > 0) {
                const currentCourse = getCourseForSlot(dayIndex, time);
                const previousCourse = getCourseForSlot(dayIndex, timeSlots[timeIndex - 1]);
                
                // Fusionner uniquement si les cours sont identiques ET consécutifs (pas de trou)
                if (currentCourse && previousCourse &&
                    currentCourse.matiere === previousCourse.matiere &&
                    currentCourse.prof === previousCourse.prof &&
                    currentCourse.salle === previousCourse.salle &&
                    currentCourse.heure === previousCourse.heure) { // Même plage horaire = consécutifs
                  return null; // Cette cellule est fusionnée avec la précédente
                }
              }
              
              // Calculer combien de créneaux ce cours occupe consécutivement
              const course = getCourseForSlot(dayIndex, time);
              let rowSpan = 1;
              
              if (course) {
                // On compte les créneaux consécutifs avec le même cours (même plage horaire)
                for (let j = timeIndex + 1; j < timeSlots.length; j++) {
                  const nextCourse = getCourseForSlot(dayIndex, timeSlots[j]);
                  if (nextCourse &&
                      nextCourse.matiere === course.matiere &&
                      nextCourse.prof === course.prof &&
                      nextCourse.salle === course.salle &&
                      nextCourse.heure === course.heure) { // Même plage horaire = même bloc de cours
                    rowSpan++;
                  } else {
                    break;
                  }
                }
              }
              
              return (
                <div
                  key={`${day}-${time}`}
                  style={{
                    gridRow: rowSpan > 1 ? `span ${rowSpan}` : undefined,
                    height: course ? `${rowSpan * 60}px` : '60px',
                    zIndex: 1,
                  }}
                  className={`relative p-3 mx-1 rounded-lg transition-colors duration-200 ${
                    course
                      ? 'bg-purple-50 border border-purple-300 hover:bg-purple-100'
                      : ''
                  }`}
                >
                  {course ? (
                    <div className="text-sm">
                      <div className="font-bold text-purple-900">{course.matiere}</div>
                      <div className="text-purple-700 text-xs mt-1">{
                        course.prof
                          .split(' ')
                          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                          .join(' ')
                      }</div>
                      <div className="text-purple-600 text-xs">{course.salle}</div>
                      <div className="text-gray-500 text-xs mt-1">
                        {(() => {
                          // On récupère l'heure de début du premier créneau
                          const startTime = time;
                          // On calcule l'heure de fin en fonction du rowSpan
                          const endTimeIndex = timeIndex + rowSpan; // +rowSpan au lieu de +(rowSpan-1)
                          const endTime = timeSlots[endTimeIndex] || '18:00'; // Ou 18:00 si on dépasse
                          return `${startTime}-${endTime}`;
                        })()}
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center text-gray-400 text-sm h-full">
                      {time !== '18:00' && 'Libre'}
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