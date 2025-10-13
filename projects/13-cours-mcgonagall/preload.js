const { contextBridge, ipcRenderer } = require('electron');

// Expose les méthodes protégées au renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  // Fonction pour récupérer l'emploi du temps
  getSchedule: (date) => ipcRenderer.invoke('get-schedule', date),
});
