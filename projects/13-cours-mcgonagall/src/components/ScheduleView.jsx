import CourseCard from './CourseCard';

function ScheduleView({ schedule }) {
  if (!schedule || schedule.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-xl text-purple-200">
          📅 Aucun cours trouvé pour cette date
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {schedule.map((day, dayIndex) => (
        <div key={dayIndex} className="bg-white/10 backdrop-blur-lg rounded-xl p-6 shadow-2xl">
          <h2 className="text-2xl font-bold mb-4 text-purple-100">
            📆 {day.date}
          </h2>
          
          {day.cours && day.cours.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {day.cours.map((course, courseIndex) => (
                <CourseCard key={courseIndex} course={course} />
              ))}
            </div>
          ) : (
            <p className="text-purple-200">Aucun cours ce jour</p>
          )}
        </div>
      ))}
    </div>
  );
}

export default ScheduleView;
