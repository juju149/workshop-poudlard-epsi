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
