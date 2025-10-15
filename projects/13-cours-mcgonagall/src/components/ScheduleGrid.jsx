import React, { useState, useEffect, useRef, useCallback } from 'react'
import PatronusLoader from './PatronusLoader'

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
  // Utilise une ref isMounted pour protéger les setState et expose loadSchedule
  // via useCallback pour que le bouton "Réessayer" et les tests puissent l'appeler.
  const isMountedRef = useRef(true)

  useEffect(() => {
    isMountedRef.current = true
    return () => {
      isMountedRef.current = false
    }
  }, [])

  const loadSchedule = useCallback(async () => {
    if (!currentWeekStart) return

    try {
      if (isMountedRef.current) {
        setLoading(true)
        setError(null)
      }

      // Formater la date du lundi au format JJ/MM/AAAA
      const mondayFormatted = currentWeekStart.toLocaleDateString('en-US');
      // Vérifier si on est dans Electron
      if (window.electronAPI && window.electronAPI.getSchedule) {
        // Mode Electron - Utiliser l'IPC
        const result = (await window.electronAPI.getSchedule(mondayFormatted)) || {}

        if (result?.success) {
          if (isMountedRef.current) setScheduleData(result.data)
        } else {
          if (isMountedRef.current) setError(result?.error || 'Erreur inconnue')
        }
      } else {
        // Mode développement navigateur - Données mockées
        console.warn('⚠️ Mode développement : Electron API non disponible, utilisation de données mockées')
        if (isMountedRef.current) setError('Veuillez lancer l\'application avec Electron pour récupérer les vraies données (npm run dev)')
      }
    } catch (err) {
      console.error('Erreur lors du chargement des données:', err)
      if (isMountedRef.current) setError(err.message)
    } finally {
      if (isMountedRef.current) setLoading(false)
    }
  }, [currentWeekStart])

  useEffect(() => {
    loadSchedule()
  }, [loadSchedule])

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
    return <PatronusLoader />
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
              const course = getCourseForSlot(dayIndex, time);
              const currentSlotHour = parseInt(time.split(':')[0], 10);
              
              // Vérifier si ce créneau est déjà occupé par un cours précédent (partie d'un cours multi-créneaux)
              if (course) {
                const courseMatch = course.heure.match(/(\d{1,2})[h:]?(\d{0,2})\s*[-–]\s*(\d{1,2})[h:]?(\d{0,2})/);
                const courseStartHour = courseMatch ? parseInt(courseMatch[1], 10) : null;
                
                // Si le cours actuel ne commence pas à ce créneau, c'est qu'il est déjà affiché plus haut
                if (courseStartHour !== null && currentSlotHour > courseStartHour) {
                  return <div key={`${day}-${time}`} className="hidden" />;
                }
              }
              
              // Vérifier si ce cours est une suite d'un cours identique précédent (fusion de cours consécutifs)
              if (course && timeIndex > 0) {
                const courseMatch = course.heure.match(/(\d{1,2})[h:]?(\d{0,2})\s*[-–]\s*(\d{1,2})[h:]?(\d{0,2})/);
                const courseStartHour = courseMatch ? parseInt(courseMatch[1], 10) : null;
                
                // Chercher un cours identique dans les créneaux précédents qui se termine exactement quand celui-ci commence
                if (courseStartHour !== null) {
                  for (let prevIndex = 0; prevIndex < timeIndex; prevIndex++) {
                    const prevCourse = getCourseForSlot(dayIndex, timeSlots[prevIndex]);
                    if (prevCourse &&
                        prevCourse.matiere === course.matiere &&
                        prevCourse.prof === course.prof &&
                        prevCourse.salle === course.salle) {
                      
                      const prevMatch = prevCourse.heure.match(/(\d{1,2})[h:]?(\d{0,2})\s*[-–]\s*(\d{1,2})[h:]?(\d{0,2})/);
                      const prevEndHour = prevMatch ? parseInt(prevMatch[3], 10) : null;
                      
                      // Si le cours précédent se termine exactement quand celui-ci commence
                      if (prevEndHour === courseStartHour) {
                        return <div key={`${day}-${time}`} className="hidden" />;
                      }
                    }
                  }
                }
              }
              
              // Calculer combien de créneaux ce cours occupe (y compris les cours fusionnés)
              let rowSpan = 1;
              let displayEndTime = null;
              
              if (course) {
                const match = course.heure.match(/(\d{1,2})[h:]?(\d{0,2})\s*[-–]\s*(\d{1,2})[h:]?(\d{0,2})/);
                if (match) {
                  const startHour = parseInt(match[1], 10);
                  const endHour = parseInt(match[3], 10);
                  rowSpan = endHour - startHour;
                  displayEndTime = endHour;
                  
                  // Chercher les cours identiques qui suivent directement
                  const dayData = scheduleData[dayIndex];
                  if (dayData && dayData.cours) {
                    const allCourses = [...dayData.cours].sort((a, b) => {
                      const aMatch = a.heure.match(/(\d{1,2})[h:]?/);
                      const bMatch = b.heure.match(/(\d{1,2})[h:]?/);
                      const aHour = aMatch ? parseInt(aMatch[1], 10) : 0;
                      const bHour = bMatch ? parseInt(bMatch[1], 10) : 0;
                      return aHour - bHour;
                    });
                    
                    // Trouver le cours actuel dans la liste
                    const currentIndex = allCourses.findIndex(c => 
                      c.matiere === course.matiere && 
                      c.prof === course.prof && 
                      c.salle === course.salle &&
                      c.heure === course.heure
                    );
                    
                    // Vérifier les cours suivants pour fusion
                    let currentEndHour = endHour;
                    for (let i = currentIndex + 1; i < allCourses.length; i++) {
                      const nextCourse = allCourses[i];
                      const nextMatch = nextCourse.heure.match(/(\d{1,2})[h:]?(\d{0,2})\s*[-–]\s*(\d{1,2})[h:]?(\d{0,2})/);
                      
                      if (nextMatch &&
                          nextCourse.matiere === course.matiere &&
                          nextCourse.prof === course.prof &&
                          nextCourse.salle === course.salle) {
                        
                        const nextStartHour = parseInt(nextMatch[1], 10);
                        const nextEndHour = parseInt(nextMatch[3], 10);
                        
                        // Vérifier si le cours suivant commence exactement quand le précédent se termine
                        if (nextStartHour === currentEndHour) {
                          rowSpan += (nextEndHour - nextStartHour);
                          currentEndHour = nextEndHour;
                          displayEndTime = nextEndHour;
                        } else {
                          // Il y a un trou, arrêter la fusion
                          break;
                        }
                      } else {
                        // Cours différent, arrêter
                        break;
                      }
                    }
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
                      <div className="flex items-center justify-between text-xs mt-1">
                        <span className="text-purple-700">{
                          course.prof
                            .split(' ')
                            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                            .join(' ')
                        }</span>
                        <span className="text-purple-600">{course.salle}</span>
                      </div>
                      <div className="flex items-center justify-between text-gray-500 text-xs mt-1">
                        <span></span>
                        <span>{time}-{displayEndTime ? `${displayEndTime}:00` : timeSlots[timeIndex + rowSpan] || '18:00'}</span>
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
            {(() => {
              if (!scheduleData || scheduleData.length === 0) return 'Aucun cours cette semaine';
              let count = 0;
              daysOfWeek.forEach((_, dayIndex) => {
                let lastEndHour = null;
                let lastCourse = null;
                for (let i = 0; i < timeSlots.length; i++) {
                  const course = getCourseForSlot(dayIndex, timeSlots[i]);
                  if (course) {
                    // Extraire les heures de début et fin
                    const match = course.heure.match(/(\d{1,2})[h:]?(\d{0,2})\s*[-–]\s*(\d{1,2})[h:]?(\d{0,2})/);
                    const startHour = match ? parseInt(match[1], 10) : null;
                    const endHour = match ? parseInt(match[3], 10) : null;
                    // Si ce cours commence à ce créneau et n'est pas une suite directe d'un cours identique
                    if (startHour !== null && parseInt(timeSlots[i].split(':')[0], 10) === startHour) {
                      if (
                        !lastCourse ||
                        course.matiere !== lastCourse.matiere ||
                        course.prof !== lastCourse.prof ||
                        course.salle !== lastCourse.salle ||
                        (lastEndHour !== startHour)
                      ) {
                        count++;
                      }
                      lastCourse = course;
                      lastEndHour = endHour;
                    }
                  } else {
                    lastCourse = null;
                    lastEndHour = null;
                  }
                }
              });
              return `${count} cours cette semaine`;
            })()}
          </p>
      </div>
    </div>
  )
}

export default ScheduleGrid