const sqlite3 = require('sqlite3').verbose();
const path = require('path');

class Database {
  constructor(dbPath = ':memory:') {
    this.db = new sqlite3.Database(dbPath, (err) => {
      if (err) {
        console.error('Erreur de connexion à la base de données:', err.message);
      } else {
        console.log('Connecté à la base de données SQLite');
      }
    });
    this.initDatabase();
  }

  initDatabase() {
    const createTableQuery = `
      CREATE TABLE IF NOT EXISTS houses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        points INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `;

    this.db.run(createTableQuery, (err) => {
      if (err) {
        console.error('Erreur lors de la création de la table:', err.message);
      } else {
        this.seedData();
      }
    });
  }

  seedData() {
    const houses = ['Gryffondor', 'Serpentard', 'Poufsouffle', 'Serdaigle'];
    const insertQuery = 'INSERT OR IGNORE INTO houses (name, points) VALUES (?, 0)';

    houses.forEach(house => {
      this.db.run(insertQuery, [house], (err) => {
        if (err && !err.message.includes('UNIQUE constraint failed')) {
          console.error('Erreur lors de l\'insertion:', err.message);
        }
      });
    });
  }

  getAllHouses(callback) {
    const query = 'SELECT * FROM houses ORDER BY points DESC';
    this.db.all(query, [], callback);
  }

  getHouseById(id, callback) {
    const query = 'SELECT * FROM houses WHERE id = ?';
    this.db.get(query, [id], callback);
  }

  updateHousePoints(id, points, callback) {
    const query = 'UPDATE houses SET points = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?';
    this.db.run(query, [points, id], function(err) {
      callback(err, this.changes);
    });
  }

  addPoints(id, pointsToAdd, callback) {
    const query = 'UPDATE houses SET points = points + ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?';
    this.db.run(query, [pointsToAdd, id], function(err) {
      callback(err, this.changes);
    });
  }

  resetAllScores(callback) {
    const query = 'UPDATE houses SET points = 0, updated_at = CURRENT_TIMESTAMP';
    this.db.run(query, [], function(err) {
      callback(err, this.changes);
    });
  }

  close() {
    this.db.close((err) => {
      if (err) {
        console.error('Erreur lors de la fermeture de la base de données:', err.message);
      } else {
        console.log('Connexion à la base de données fermée');
      }
    });
  }
}

module.exports = Database;
