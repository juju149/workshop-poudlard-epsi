import { useState, useEffect } from 'react';
import DateSelector from './components/DateSelector';
import ScheduleView from './components/ScheduleView';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';

function App() {
  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [hasCredentials, setHasCredentials] = useState(false);

  useEffect(() => {
    // Check if credentials are configured
    const checkEnv = async () => {
      if (window.electronAPI) {
        const env = await window.electronAPI.getEnv();
        setHasCredentials(env.hasCredentials);
      }
    };
    checkEnv();
  }, []);

  const handleDateSelect = async (date) => {
    setLoading(true);
    setError(null);
    
    try {
      if (window.electronAPI) {
        const result = await window.electronAPI.scrapeSchedule(date);
        if (result.success) {
          setSchedule(result.data);
        } else {
          setError(result.error || 'Erreur lors de la récupération de l\'emploi du temps');
        }
      } else {
        // Fallback for development without Electron
        setError('API Electron non disponible');
      }
    } catch (err) {
      setError(err.message || 'Une erreur est survenue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">
            📚 Emploi du Temps McGonagall
          </h1>
          <p className="text-purple-200">
            Consultez votre emploi du temps magique
          </p>
        </header>

        {!hasCredentials && (
          <div className="bg-yellow-500 text-yellow-900 p-4 rounded-lg mb-6 text-center">
            ⚠️ Veuillez configurer vos identifiants dans le fichier .env
          </div>
        )}

        <DateSelector onDateSelect={handleDateSelect} disabled={loading || !hasCredentials} />

        {loading && <LoadingSpinner />}
        {error && <ErrorMessage message={error} onDismiss={() => setError(null)} />}
        {schedule && !loading && <ScheduleView schedule={schedule} />}

        {!schedule && !loading && !error && (
          <div className="text-center mt-12 text-purple-200">
            <p className="text-xl">
              🔮 Sélectionnez une date pour voir votre emploi du temps
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
