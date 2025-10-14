import { app, BrowserWindow, ipcMain } from 'electron';
import { config } from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { scrapeSchedule } from './scraper.js';

config();

const __dirname = dirname(fileURLToPath(import.meta.url));
const isDev = process.env.NODE_ENV === 'development';

// Gérer la récupération de l'emploi du temps
ipcMain.handle('get-schedule', async (event, date) => {
  try {
    console.log(`📅 Récupération de l'emploi du temps pour le ${date || "aujourd'hui"}`);
    const scheduleData = await scrapeSchedule(date);
    return { success: true, data: scheduleData };
  } catch (error) {
    console.error('❌ Erreur lors du scraping:', error);
    return { success: false, error: error.message };
  }
});

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: join(__dirname, 'preload.js')
    }
  });

  // En développement, charge le serveur Vite
  // En production, charge les fichiers buildés
  if (isDev) {
    win.loadURL('http://localhost:3002');
  } else {
    win.loadFile(join(__dirname, 'dist/index.html'));
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