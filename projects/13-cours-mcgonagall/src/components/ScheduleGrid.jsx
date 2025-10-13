import React from 'react'

const ScheduleGrid = () => {
  const timeSlots = [
    '08:00', '09:00', '10:00', '11:00', '12:00', 
    '13:00', '14:00', '15:00', '16:00', '17:00', '18:00'
  ]
  
  const daysOfWeek = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="grid grid-cols-6 gap-2">
        {/* En-tête vide pour la colonne des heures */}
        <div className="p-3 bg-purple-100 rounded-lg font-semibold text-center text-purple-800">
          Heures
        </div>
        
        {/* En-têtes des jours */}
        {daysOfWeek.map((day) => (
          <div key={day} className="p-3 bg-purple-100 rounded-lg font-semibold text-center text-purple-800">
            {day}
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
            {daysOfWeek.map((day) => (
              <div 
                key={`${day}-${time}`}
                className="p-3 min-h-[60px] border-2 border-dashed border-gray-200 rounded-lg 
                         hover:border-purple-300 hover:bg-purple-50 transition-colors duration-200
                         flex items-center justify-center text-gray-400 text-sm"
              >
                Libre
              </div>
            ))}
          </React.Fragment>
        ))}
      </div>
      
      {/* Légende */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-semibold text-gray-700 mb-2">🎯 Prêt pour vos cours !</h3>
        <p className="text-gray-600">
          Cet emploi du temps est actuellement vide. Les cours apparaîtront ici une fois configurés.
        </p>
      </div>
    </div>
  )
}

export default ScheduleGrid