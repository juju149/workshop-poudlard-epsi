import { describe, it, expect } from 'vitest';
import { formatDateToFrench, parseFrenchDate, isValidFrenchDate } from '../../src/utils/dateUtils';

describe('dateUtils', () => {
  describe('formatDateToFrench', () => {
    it('should format a date to French format DD/MM/YYYY', () => {
      const date = new Date(2025, 9, 13); // October 13, 2025
      const formatted = formatDateToFrench(date);
      expect(formatted).toBe('13/10/2025');
    });

    it('should handle single digit days and months', () => {
      const date = new Date(2025, 0, 5); // January 5, 2025
      const formatted = formatDateToFrench(date);
      expect(formatted).toBe('05/01/2025');
    });

    it('should handle leap year dates', () => {
      const date = new Date(2024, 1, 29); // February 29, 2024
      const formatted = formatDateToFrench(date);
      expect(formatted).toBe('29/02/2024');
    });
  });

  describe('parseFrenchDate', () => {
    it('should parse a valid French date string', () => {
      const date = parseFrenchDate('13/10/2025');
      expect(date).toBeInstanceOf(Date);
      expect(date?.getDate()).toBe(13);
      expect(date?.getMonth()).toBe(9); // October is month 9 (0-indexed)
      expect(date?.getFullYear()).toBe(2025);
    });

    it('should return null for invalid date string', () => {
      expect(parseFrenchDate('invalid')).toBe(null);
      expect(parseFrenchDate('32/13/2025')).toBe(null);
      expect(parseFrenchDate('00/01/2025')).toBe(null);
    });

    it('should return null for empty string', () => {
      expect(parseFrenchDate('')).toBe(null);
    });

    it('should return null for undefined', () => {
      expect(parseFrenchDate(undefined)).toBe(null);
    });

    it('should handle leap year dates correctly', () => {
      const leapDate = parseFrenchDate('29/02/2024');
      expect(leapDate).toBeInstanceOf(Date);
      
      const nonLeapDate = parseFrenchDate('29/02/2023');
      expect(nonLeapDate).toBe(null);
    });
  });

  describe('isValidFrenchDate', () => {
    it('should return true for valid dates', () => {
      expect(isValidFrenchDate('13/10/2025')).toBe(true);
      expect(isValidFrenchDate('01/01/2000')).toBe(true);
      expect(isValidFrenchDate('31/12/2025')).toBe(true);
    });

    it('should return false for invalid dates', () => {
      expect(isValidFrenchDate('32/01/2025')).toBe(false);
      expect(isValidFrenchDate('01/13/2025')).toBe(false);
      expect(isValidFrenchDate('invalid')).toBe(false);
      expect(isValidFrenchDate('')).toBe(false);
    });

    it('should validate leap years correctly', () => {
      expect(isValidFrenchDate('29/02/2024')).toBe(true);
      expect(isValidFrenchDate('29/02/2023')).toBe(false);
    });
  });
});
