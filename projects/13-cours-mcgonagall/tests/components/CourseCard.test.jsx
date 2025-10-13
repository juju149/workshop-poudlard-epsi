import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import CourseCard from '../../src/components/CourseCard';

describe('CourseCard', () => {
  const mockCourse = {
    matiere: 'Potions',
    prof: 'Severus Rogue',
    heure: '09:00 - 10:30',
    salle: 'Salle 101'
  };

  it('should render course subject', () => {
    render(<CourseCard course={mockCourse} />);
    expect(screen.getByText('Potions')).toBeInTheDocument();
  });

  it('should render professor name', () => {
    render(<CourseCard course={mockCourse} />);
    expect(screen.getByText('Severus Rogue')).toBeInTheDocument();
  });

  it('should render time slot', () => {
    render(<CourseCard course={mockCourse} />);
    expect(screen.getByText('09:00 - 10:30')).toBeInTheDocument();
  });

  it('should render room information', () => {
    render(<CourseCard course={mockCourse} />);
    expect(screen.getByText('Salle 101')).toBeInTheDocument();
  });

  it('should handle missing professor', () => {
    const courseWithoutProf = { ...mockCourse, prof: '' };
    render(<CourseCard course={courseWithoutProf} />);
    expect(screen.queryByText('Severus Rogue')).not.toBeInTheDocument();
  });

  it('should handle missing time', () => {
    const courseWithoutTime = { ...mockCourse, heure: '' };
    render(<CourseCard course={courseWithoutTime} />);
    expect(screen.queryByText('09:00 - 10:30')).not.toBeInTheDocument();
  });

  it('should handle missing room', () => {
    const courseWithoutRoom = { ...mockCourse, salle: '' };
    render(<CourseCard course={courseWithoutRoom} />);
    expect(screen.queryByText('Salle 101')).not.toBeInTheDocument();
  });

  it('should display default text for missing subject', () => {
    const courseWithoutSubject = { ...mockCourse, matiere: '' };
    render(<CourseCard course={courseWithoutSubject} />);
    expect(screen.getByText('Matière inconnue')).toBeInTheDocument();
  });
});
