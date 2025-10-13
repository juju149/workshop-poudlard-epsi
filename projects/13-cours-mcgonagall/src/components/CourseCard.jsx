function CourseCard({ course }) {
  return (
    <div className="bg-gradient-to-br from-purple-600/30 to-indigo-600/30 rounded-lg p-4 border border-white/20 hover:border-white/40 transition-all hover:shadow-lg">
      <h3 className="text-lg font-bold mb-2 text-white">
        {course.matiere || 'Matière inconnue'}
      </h3>
      
      <div className="space-y-2 text-sm">
        {course.prof && (
          <div className="flex items-start">
            <span className="mr-2">👨‍🏫</span>
            <span className="text-purple-100">{course.prof}</span>
          </div>
        )}
        
        {course.heure && (
          <div className="flex items-start">
            <span className="mr-2">🕐</span>
            <span className="text-purple-100">{course.heure}</span>
          </div>
        )}
        
        {course.salle && (
          <div className="flex items-start">
            <span className="mr-2">📍</span>
            <span className="text-purple-100">{course.salle}</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default CourseCard;
