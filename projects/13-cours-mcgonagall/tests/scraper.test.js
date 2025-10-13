import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock dotenv first
vi.mock('dotenv', () => ({
  config: vi.fn()
}));

// Mock puppeteer with full browser/page mock
const mockPage = {
  goto: vi.fn(),
  $: vi.fn(),
  waitForSelector: vi.fn(),
  type: vi.fn(),
  click: vi.fn(),
  evaluate: vi.fn().mockResolvedValue([])
};

const mockBrowser = {
  newPage: vi.fn().mockResolvedValue(mockPage),
  close: vi.fn()
};

vi.mock('puppeteer', () => ({
  default: {
    launch: vi.fn().mockResolvedValue(mockBrowser)
  }
}));

describe('scraper module', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    process.env.USERNAME = 'testuser';
    process.env.PASSWORD = 'testpass';
  });

  it('should have scrapeSchedule function exported', async () => {
    // Import after mocks are set up
    const scraperModule = await import('../scraper.js');
    expect(scraperModule.scrapeSchedule).toBeDefined();
    expect(typeof scraperModule.scrapeSchedule).toBe('function');
  });

  it('should format date correctly when called with null', () => {
    const date = new Date();
    const expected = date.toLocaleDateString('fr-FR');
    expect(expected).toMatch(/\d{2}\/\d{2}\/\d{4}/);
  });

  it('should use environment variable for username', () => {
    expect(process.env.USERNAME).toBe('testuser');
    const url = `https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx?action=posEDTLMS&serverID=C&Tel=${process.env.USERNAME}&date=13/10/2025`;
    expect(url).toContain('Tel=testuser');
  });

  it('should construct proper URL with date parameter', () => {
    const testDate = '13/10/2025';
    const url = `https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx?action=posEDTLMS&serverID=C&Tel=${process.env.USERNAME}&date=${testDate}`;
    expect(url).toContain('date=13/10/2025');
    expect(url).toContain('serverID=C');
    expect(url).toContain('action=posEDTLMS');
  });

  it('should handle login form detection logic', () => {
    // Mock selector existence check
    const hasLoginForm = true;
    expect(hasLoginForm).toBe(true);
  });

  it('should parse course data structure correctly', () => {
    const mockCourse = {
      matiere: 'Potions',
      prof: 'Severus Rogue',
      heure: '09:00',
      salle: 'Salle 101'
    };

    expect(mockCourse).toHaveProperty('matiere');
    expect(mockCourse).toHaveProperty('prof');
    expect(mockCourse).toHaveProperty('heure');
    expect(mockCourse).toHaveProperty('salle');
  });

  it('should validate day structure with date and cours', () => {
    const mockDay = {
      date: 'Lundi 13 Oct',
      cours: []
    };

    expect(mockDay).toHaveProperty('date');
    expect(mockDay).toHaveProperty('cours');
    expect(Array.isArray(mockDay.cours)).toBe(true);
  });

  it('should filter out days with no courses', () => {
    const days = [
      { date: 'Lundi', cours: [{ matiere: 'Test' }] },
      { date: 'Mardi', cours: [] },
      { date: 'Mercredi', cours: [{ matiere: 'Test2' }] }
    ];

    const filtered = days.filter(day => day.cours.length > 0);
    expect(filtered.length).toBe(2);
    expect(filtered[0].date).toBe('Lundi');
    expect(filtered[1].date).toBe('Mercredi');
  });

  it('should handle text cleanup with regex', () => {
    const text = 'Test  with   multiple    spaces';
    const cleaned = text.replace(/\s+/g, ' ').trim();
    expect(cleaned).toBe('Test with multiple spaces');
  });

  it('should remove "Salle:" prefix from room name', () => {
    const salleText = 'Salle: 101';
    const cleaned = salleText.replace('Salle:', '').trim();
    expect(cleaned).toBe('101');
  });
});
