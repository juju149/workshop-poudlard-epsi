import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('electronAPI', {
  scrapeSchedule: (date) => ipcRenderer.invoke('scrape-schedule', date),
  getEnv: () => ipcRenderer.invoke('get-env')
});
