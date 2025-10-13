export interface ElectronAPI {
  getSchedule: (date?: string) => Promise<{
    success: boolean;
    data?: Array<{
      date: string;
      cours: Array<{
        matiere: string;
        prof: string;
        heure: string;
        salle: string;
      }>;
    }>;
    error?: string;
  }>;
}

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
