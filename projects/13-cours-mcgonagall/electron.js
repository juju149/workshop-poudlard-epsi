import { app, BrowserWindow, ipcMain } from 'electron';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { readFileSync, existsSync } from 'fs';
import { scrapeSchedule } from './scraper.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const isDev = process.env.NODE_ENV === 'development';

// Charger .env manuellement pour compatibilité avec asar
const envPath = join(__dirname, '.env');
if (existsSync(envPath)) {
  const envContent = readFileSync(envPath, 'utf8');
  envContent.split('\n').forEach(line => {
    const match = line.match(/^([^=:#]+)=(.*)$/);
    if (match) {
      const key = match[1].trim();
      const value = match[2].trim().replace(/^["']|["']$/g, '');
      process.env[key] = value;
    }
  });
  console.log('✅ .env chargé avec succès');
} else {
  console.warn('⚠️ Fichier .env non trouvé');
}

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
      win.webContents.openDevTools();
    } else {
      win.loadFile(join(__dirname, 'dist', 'index.html'));
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