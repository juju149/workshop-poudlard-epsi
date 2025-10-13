const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const Database = require('./database');

const app = express();
const PORT = process.env.PORT || 3000;
const DB_PATH = process.env.DB_PATH || './hogwarts.db';

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Initialisation de la base de données
const db = new Database(DB_PATH);

// Routes

// GET /api/houses - Récupérer toutes les maisons avec leurs scores
app.get('/api/houses', (req, res) => {
  db.getAllHouses((err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json({ houses: rows });
  });
});

// GET /api/houses/:id - Récupérer une maison spécifique
app.get('/api/houses/:id', (req, res) => {
  const id = parseInt(req.params.id);
  
  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID invalide' });
  }

  db.getHouseById(id, (err, row) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    if (!row) {
      return res.status(404).json({ error: 'Maison non trouvée' });
    }
    res.json({ house: row });
  });
});

// PUT /api/houses/:id - Mettre à jour les points d'une maison
app.put('/api/houses/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const { points } = req.body;

  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID invalide' });
  }

  if (typeof points !== 'number' || points < 0) {
    return res.status(400).json({ error: 'Points invalides (doit être un nombre >= 0)' });
  }

  db.updateHousePoints(id, points, (err, changes) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    if (changes === 0) {
      return res.status(404).json({ error: 'Maison non trouvée' });
    }
    res.json({ message: 'Points mis à jour avec succès', changes });
  });
});

// POST /api/houses/:id/add - Ajouter des points à une maison
app.post('/api/houses/:id/add', (req, res) => {
  const id = parseInt(req.params.id);
  const { points } = req.body;

  if (isNaN(id)) {
    return res.status(400).json({ error: 'ID invalide' });
  }

  if (typeof points !== 'number') {
    return res.status(400).json({ error: 'Points invalides (doit être un nombre)' });
  }

  db.addPoints(id, points, (err, changes) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    if (changes === 0) {
      return res.status(404).json({ error: 'Maison non trouvée' });
    }
    res.json({ message: 'Points ajoutés avec succès', changes });
  });
});

// POST /api/reset - Réinitialiser tous les scores
app.post('/api/reset', (req, res) => {
  db.resetAllScores((err, changes) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json({ message: 'Tous les scores ont été réinitialisés', changes });
  });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Gestion des erreurs 404
app.use((req, res) => {
  res.status(404).json({ error: 'Route non trouvée' });
});

// Démarrage du serveur
if (require.main === module) {
  const server = app.listen(PORT, () => {
    console.log(`🧙‍♂️ API des scores de Poudlard démarrée sur le port ${PORT}`);
  });

  // Gestion de l'arrêt propre
  process.on('SIGTERM', () => {
    console.log('Signal SIGTERM reçu, fermeture du serveur...');
    server.close(() => {
      db.close();
      console.log('Serveur fermé');
      process.exit(0);
    });
  });
}

module.exports = { app, db };
