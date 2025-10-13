import { app, BrowserWindow, ipcMain } from 'electron';
import { config } from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import { scrapeSchedule } from '../scraper.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

config();

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // Load the app
  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// IPC handlers
ipcMain.handle('scrape-schedule', async (event, date) => {
  try {
    const schedule = await scrapeSchedule(date);
    return { success: true, data: schedule };
  } catch (error) {
    console.error('Scraping error:', error);
    return { success: false, error: error.message };
  }
});

ipcMain.handle('get-env', async () => {
  return {
    hasCredentials: !!(process.env.USERNAME && process.env.PASSWORD)
  };
});
