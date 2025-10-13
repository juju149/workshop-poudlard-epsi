/**
 * Format a date object to French format (DD/MM/YYYY)
 * @param {Date} date - The date to format
 * @returns {string} - Formatted date string
 */
export function formatDateToFrench(date) {
  return date.toLocaleDateString('fr-FR');
}

/**
 * Parse a French formatted date string (DD/MM/YYYY) to Date object
 * @param {string} dateString - Date string in DD/MM/YYYY format
 * @returns {Date|null} - Date object or null if invalid
 */
export function parseFrenchDate(dateString) {
  if (!dateString) return null;
  
  const parts = dateString.split('/');
  if (parts.length !== 3) return null;
  
  const day = parseInt(parts[0], 10);
  const month = parseInt(parts[1], 10) - 1; // Month is 0-indexed
  const year = parseInt(parts[2], 10);
  
  const date = new Date(year, month, day);
  
  // Validate the date
  if (
    date.getDate() === day &&
    date.getMonth() === month &&
    date.getFullYear() === year
  ) {
    return date;
  }
  
  return null;
}

/**
 * Validate a French formatted date string
 * @param {string} dateString - Date string to validate
 * @returns {boolean} - True if valid, false otherwise
 */
export function isValidFrenchDate(dateString) {
  return parseFrenchDate(dateString) !== null;
}
