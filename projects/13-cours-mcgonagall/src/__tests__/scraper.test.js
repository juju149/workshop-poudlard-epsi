import puppeteer from 'puppeteer';

jest.mock('puppeteer');

describe('scrapeSchedule', () => {
  let launchMock;

  beforeEach(() => {
    jest.resetAllMocks();
    // Default fake page
    const page = {
      goto: jest.fn().mockResolvedValue(undefined),
      $: jest.fn().mockResolvedValue(null),
      waitForSelector: jest.fn().mockResolvedValue(undefined),
      type: jest.fn().mockResolvedValue(undefined),
      click: jest.fn().mockResolvedValue(undefined),
      evaluate: jest.fn().mockResolvedValue([]),
    };

    const browser = {
      newPage: jest.fn().mockResolvedValue(page),
      close: jest.fn().mockResolvedValue(undefined),
    };

    launchMock = puppeteer.launch.mockResolvedValue(browser);
  });

  test('returns parsed schedule when page contains days and cases', async () => {
    // Build fake DOM evaluation result
    const fakeResult = [
      {
        date: '13/10/2025',
        cours: [
          { matiere: 'Potions', prof: 'Severus Snape', heure: '08:00', salle: '101' },
        ],
      },
    ];

    // Make evaluate return our fake result
    puppeteer.launch.mockImplementationOnce(async () => ({
      newPage: async () => ({
        goto: async () => {},
        $: async () => null,
        waitForSelector: async () => {},
        type: async () => {},
        click: async () => {},
        evaluate: async () => fakeResult,
      }),
      close: async () => {},
    }));

    const { scrapeSchedule } = await import('../../scraper.js');
    const res = await scrapeSchedule('13/10/2025');
    expect(res).toEqual(fakeResult);
    expect(puppeteer.launch).toHaveBeenCalled();
  });

  test('handles login flow and times out when schedule does not load', async () => {
    // Mock page.$ to return a truthy value to simulate login form
    const page = {
      goto: jest.fn().mockResolvedValue(undefined),
      $: jest.fn().mockResolvedValue(true),
      waitForSelector: jest.fn().mockImplementation(selector => {
        if (selector === '.Jour') {
          // Simulate timeout by rejecting
          return Promise.reject(new Error('timeout'));
        }
        return Promise.resolve();
      }),
      type: jest.fn().mockResolvedValue(undefined),
      click: jest.fn().mockResolvedValue(undefined),
      evaluate: jest.fn().mockResolvedValue([]),
    };

    puppeteer.launch.mockResolvedValue({ newPage: async () => page, close: async () => {} });

    // spy on process.exit to ensure it's called
    const exitSpy = jest.spyOn(process, 'exit').mockImplementation(() => {});

    const { scrapeSchedule } = await import('../../scraper.js');
    await expect(scrapeSchedule('13/10/2025')).rejects.toThrow();
    expect(exitSpy).toHaveBeenCalledWith(1);
    exitSpy.mockRestore();
  });
});
