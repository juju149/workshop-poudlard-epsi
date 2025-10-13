import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import ScheduleView from '../../src/components/ScheduleView';

describe('ScheduleView', () => {
  const mockSchedule = [
    {
      date: 'Lundi 13 Oct',
      cours: [
        {
          matiere: 'Potions',
          prof: 'Severus Rogue',
          heure: '09:00',
          salle: '101'
        },
        {
          matiere: 'Défense contre les forces du mal',
          prof: 'Remus Lupin',
          heure: '14:00',
          salle: '202'
        }
      ]
    }
  ];

  it('should render day header with date', () => {
    render(<ScheduleView schedule={mockSchedule} />);
    expect(screen.getByText(/Lundi 13 Oct/i)).toBeInTheDocument();
  });

  it('should render all courses for a day', () => {
    render(<ScheduleView schedule={mockSchedule} />);
    expect(screen.getByText('Potions')).toBeInTheDocument();
    expect(screen.getByText('Défense contre les forces du mal')).toBeInTheDocument();
  });

  it('should display message when no schedule data', () => {
    render(<ScheduleView schedule={[]} />);
    expect(screen.getByText(/Aucun cours trouvé/i)).toBeInTheDocument();
  });

  it('should display message when schedule is null', () => {
    render(<ScheduleView schedule={null} />);
    expect(screen.getByText(/Aucun cours trouvé/i)).toBeInTheDocument();
  });

  it('should handle day with no courses', () => {
    const scheduleWithNoCourses = [
      {
        date: 'Dimanche 15 Oct',
        cours: []
      }
    ];
    render(<ScheduleView schedule={scheduleWithNoCourses} />);
    expect(screen.getByText(/Dimanche 15 Oct/i)).toBeInTheDocument();
    expect(screen.getByText(/Aucun cours ce jour/i)).toBeInTheDocument();
  });

  it('should render multiple days', () => {
    const multiDaySchedule = [
      {
        date: 'Lundi 13 Oct',
        cours: [{ matiere: 'Potions', prof: 'Rogue', heure: '09:00', salle: '101' }]
      },
      {
        date: 'Mardi 14 Oct',
        cours: [{ matiere: 'Sortilèges', prof: 'Flitwick', heure: '10:00', salle: '103' }]
      }
    ];
    render(<ScheduleView schedule={multiDaySchedule} />);
    expect(screen.getByText(/Lundi 13 Oct/i)).toBeInTheDocument();
    expect(screen.getByText(/Mardi 14 Oct/i)).toBeInTheDocument();
  });
});
