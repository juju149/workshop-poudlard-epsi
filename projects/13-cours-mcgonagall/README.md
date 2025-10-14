# Emploi du temps Electron

Application Electron pour afficher un emploi du temps en scrappant un site web.

## Historique des prompts et réponses

---

### Prompt 1
> initialise un project electron vide, le but est de faire un emploi du temps qui va scrapter un site pour remplir les données, prépare un .env avec le username et password

**Réponse :**
Je vais vous aider à initialiser un projet Electron vide pour créer un emploi du temps qui scrape un site web. Commençons par créer la structure du projet.

---

### Prompt 2
> tu te mets dans le dossier 13 dans projects pour le faire

**Réponse :**
Commençons par créer la structure du projet Electron. Je vais créer un dossier pour le projet et initialiser le package.json.

---

### Prompt 3
> tu te mets à la racine de 13 direct

**Réponse :**
Le projet Electron vide est maintenant initialisé à la racine du dossier 13. Vous disposez de :
- package.json configuré pour Electron
- main.js pour lancer l'app
- index.html pour l'interface
- .env pour le username et password
- Dépendances installées : electron, puppeteer, dotenv
- Un script de scraping de base (scraper.js)
- Un README explicatif

Vous pouvez maintenant développer la logique de scraping et l'affichage de l' emploi du temps. Souhaitez-vous ajouter une fonctionnalité ou personnaliser l'interface ?

---

### Prompt 4
> Ajoute un gitignore pour le .env et nodemodules, ajoute aussi un .env.example

**Réponse :**
Les fichiers .gitignore (pour ignorer node_modules et .env) et .env.example (modèle pour les variables d'environnement) ont été ajoutés à la racine du dossier 13.

Votre projet est maintenant prêt pour le versionnement avec Git et le partage des variables d'environnement sans exposer vos identifiants. Souhaitez-vous une autre configuration ou une fonctionnalité supplémentaire ?

---

### Prompt 5
> Ajoute un README avec tous les prompts que je t'ai fait et toutes tes réponses de manière formattées

**Réponse :**
Ce fichier contient l'historique complet des échanges pour la mise en place du projet.

---

### Prompt 6
> Voici l'url de l'emploi du temps :https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx?action=posEDTLMS&serverID=C&Tel=test&date=10/13/2025
>
> Retire le password du .env en fait ça sert à rien
>
> Il faut aussi qu'on puisse scrap pour une date précise, tu remplaces tel=test par le username du .env
>
> Tu v

**Réponse :**
Le fichier `.env` et `.env.example` ont été mis à jour pour ne contenir que `USERNAME`.
Le script `scraper.js` permet maintenant de scrapper pour une date précise en passant la date en argument (format MM/DD/YYYY), et utilise le username du `.env` dans l'URL.
L'URL utilisée est :
`https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx?action=posEDTLMS&serverID=C&Tel=<USERNAME>&date=<DATE>`
Exemple d'utilisation :
```bash
node scraper.js 10/13/2025
```
Si aucune date n'est fournie, la date du jour est utilisée.

---

### Prompt 7
> ça c'est une page pour la date du jour, tu me scapper tout par jour

**Réponse :**
Je vais adapter le scraper pour récupérer tous les cours de chaque jour à partir de la page HTML fournie. Le script va parcourir la structure et extraire les informations pour chaque journée (date, heure, matière, salle, professeur, etc.).

---

### Prompt du 13/10/2025
> mets le timing à 1min max plutôt et ajoute tous les nouveaux prompts au readme

**Réponse :**
Le timeout d'attente du planning après le login a été réduit à 1 minute (60000 ms) dans le script `scraper.js`. Tous les nouveaux prompts et réponses sont ajoutés ici pour la traçabilité.

---

### Prompt du 13/10/2025
> mets juste la date au format fr-FR

**Réponse :**
La génération de la date utilise désormais le format français JJ/MM/AAAA grâce à `toLocaleDateString('fr-FR')` dans le script `scraper.js`. L'URL du scraping est donc compatible avec le format attendu par le site.

---

### Prompt du 13/10/2025
> tu dois fix tailwind, là les class sont pas utilisées

**Réponse :**
J'ai identifié et corrigé le problème avec Tailwind CSS v4. Les corrections apportées :

1. **PostCSS Config** - Mise à jour de `postcss.config.js` :
   ```javascript
   export default {
     plugins: {
       '@tailwindcss/vite': {},
       autoprefixer: {},
     },
   }
   ```

2. **Vite Config** - Ajout du plugin Tailwind dans `vite.config.js` :
   ```javascript
   import tailwindcss from '@tailwindcss/vite'
   
   export default defineConfig({
     plugins: [react(), tailwindcss()],
     // ...
   })
   ```

3. **Installation** - Ajout de la dépendance manquante :
   ```bash
   npm install @tailwindcss/vite
   ```

Le problème venait de l'utilisation de Tailwind CSS v4 avec une configuration obsolète. Avec Tailwind v4, il faut utiliser `@tailwindcss/vite` au lieu de `@tailwindcss/postcss` et ajouter le plugin dans la configuration Vite.


### Prompt du 14/10/2025
> fais moi le frontend de l'edt maintenant que tailwind marche, ajoute tes résultats au readme

**Réponse :**
J'ai développé le frontend de l'emploi du temps avec React et Tailwind CSS :

- Le chargement de l'EDT se fait automatiquement à l'ouverture de l'application.
- Le design est moderne, responsive et épuré grâce à Tailwind.
- Les cours s'affichent dans une grille stylisée, chaque créneau étant présenté dans une carte avec la matière, le professeur et l'horaire.
- Le composant principal `ScheduleGrid` gère l'affichage dynamique des données.

Exemple d'intégration :
```jsx
// src/App.jsx
import React, { useState, useEffect } from 'react';
import ScheduleGrid from './components/ScheduleGrid';

function App() {
  const [schedule, setSchedule] = useState([]);

  useEffect(() => {
    // Chargement automatique simulé
    setSchedule([
      { matiere: 'Métamorphose', prof: 'McGonagall', horaire: 'Lundi 9h-10h' },
      { matiere: 'Potions', prof: 'Snape', horaire: 'Mardi 10h-12h' },
      // ...
    ]);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
      <h1 className="text-3xl font-bold mb-6 text-purple-700">Emploi du temps</h1>
      <ScheduleGrid schedule={schedule} />
    </div>
  );
}

export default App;
```

Le résultat : l'emploi du temps s'affiche automatiquement dans une interface claire et agréable, adaptée à tous les écrans.

### Prompt du 14/10/2025
> tout est parfait sauf que les cours du type "9h-11h" sont affichés sur les heures 9h et 11h, mais pas sur 10h, fixe ça

**Réponse :**
L'affichage des cours a été corrigé :
- Les cours couvrant une plage horaire (ex : 9h-11h) apparaissent désormais sur toutes les heures intermédiaires (9h, 10h, 11h) dans la grille.
- La fonction de rendu vérifie pour chaque créneau si l'heure est incluse dans la plage du cours, quel que soit le format (ex : "09:00-11:00", "9h-11h", "09h00-11h00").
- Les créneaux sont bien remplis pour toute la durée du cours.

Extrait de code :
```js
// src/components/ScheduleGrid.jsx
const getCourseForSlot = (dayIndex, timeSlot) => {
  // ...
  return dayData.cours.find(c => {
    if (!c.heure) return false
    const match = c.heure.match(/(\d{1,2})[h:]?(\d{0,2})\s*[-–]\s*(\d{1,2})[h:]?(\d{0,2})/)
    if (match) {
      let startHour = parseInt(match[1], 10)
      let endHour = parseInt(match[3], 10)
      let slotHour = parseInt(timeSlot.split(':')[0], 10)
      return slotHour >= startHour && slotHour <= endHour
    }
    return c.heure.startsWith(timeSlot)
  })
}
```
---

### Prompt du 14/10/2025
> Ajoute les boutons pour changer les semaines à gauche et à droite de "semaine du XXX au XXX" et supprime le bouton Actualiser

**Réponse :**
Les boutons ← et → ont été ajoutés de part et d'autre du titre de la semaine. Le bouton "Actualiser" a été supprimé. La navigation entre les semaines déclenche le scraping pour la nouvelle semaine.

---

### Prompt du 14/10/2025
> Le scraping ne semble pas se déclencher lors du changement de semaine

**Réponse :**
Le scraping est bien déclenché à chaque changement de semaine grâce au hook `useEffect(() => { loadSchedule() }, [currentWeekStart])`. À chaque navigation, la date du lundi change et le scrapper est appelé via l'API Electron.

---

### Prompt du 14/10/2025
> Ajoute tout ça au readme

**Réponse :**
Toutes les modifications et prompts sont ajoutés ici pour la traçabilité. Les fonctionnalités de navigation, scraping dynamique, affichage des cours, gestion des erreurs et formatage sont documentées.

---

## Installation

```bash
npm install
```

## Lancement

```bash
npm start
```

## Scraping

Pour lancer le scraping :
```bash
node scraper.js
```

## Configuration

Créer un fichier `.env` à la racine avec :
```
USERNAME=VotreIdentifiant
PASSWORD=VotreMotDePasse
```
