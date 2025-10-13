import { useState } from 'react';
import { formatDateToFrench } from '../utils/dateUtils';

function DateSelector({ onDateSelect, disabled }) {
  const [selectedDate, setSelectedDate] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedDate) {
      onDateSelect(selectedDate);
    }
  };

  const handleTodayClick = () => {
    const today = formatDateToFrench(new Date());
    setSelectedDate(today);
    onDateSelect(today);
  };

  return (
    <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 mb-6 shadow-2xl">
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4 items-center justify-center">
        <div className="flex-1 w-full sm:max-w-md">
          <label htmlFor="date-input" className="block text-sm font-medium mb-2">
            Date (JJ/MM/AAAA)
          </label>
          <input
            id="date-input"
            type="text"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            placeholder="13/10/2025"
            disabled={disabled}
            className="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-purple-400 disabled:opacity-50"
          />
        </div>
        <div className="flex gap-2">
          <button
            type="submit"
            disabled={disabled || !selectedDate}
            className="px-6 py-2 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Rechercher
          </button>
          <button
            type="button"
            onClick={handleTodayClick}
            disabled={disabled}
            className="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Aujourd'hui
          </button>
        </div>
      </form>
    </div>
  );
}

export default DateSelector;
