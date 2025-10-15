const Database = require('./database');

describe('Database', () => {
  let db;

  beforeEach(() => {
    db = new Database(':memory:');
  });

  afterEach(() => {
    db.close();
  });

  describe('initDatabase', () => {
    it('devrait créer la table houses', (done) => {
      setTimeout(() => {
        db.getAllHouses((err, rows) => {
          expect(err).toBeNull();
          expect(rows).toBeDefined();
          done();
        });
      }, 100);
    });
  });

  describe('seedData', () => {
    it('devrait insérer les 4 maisons', (done) => {
      setTimeout(() => {
        db.getAllHouses((err, rows) => {
          expect(err).toBeNull();
          expect(rows.length).toBe(4);
          done();
        });
      }, 100);
    });

    it('devrait avoir les noms corrects des maisons', (done) => {
      setTimeout(() => {
        db.getAllHouses((err, rows) => {
          const names = rows.map(r => r.name);
          expect(names).toContain('Gryffondor');
          expect(names).toContain('Serpentard');
          expect(names).toContain('Poufsouffle');
          expect(names).toContain('Serdaigle');
          done();
        });
      }, 100);
    });
  });

  describe('getAllHouses', () => {
    it('devrait retourner toutes les maisons triées par points', (done) => {
      setTimeout(() => {
        db.updateHousePoints(1, 100, () => {
          db.updateHousePoints(2, 50, () => {
            db.getAllHouses((err, rows) => {
              expect(err).toBeNull();
              expect(rows[0].points).toBeGreaterThanOrEqual(rows[1].points);
              done();
            });
          });
        });
      }, 100);
    });
  });

  describe('getHouseById', () => {
    it('devrait retourner une maison par son ID', (done) => {
      setTimeout(() => {
        db.getHouseById(1, (err, row) => {
          expect(err).toBeNull();
          expect(row).toBeDefined();
          expect(row.id).toBe(1);
          done();
        });
      }, 100);
    });

    it('devrait retourner undefined pour un ID inexistant', (done) => {
      setTimeout(() => {
        db.getHouseById(999, (err, row) => {
          expect(err).toBeNull();
          expect(row).toBeUndefined();
          done();
        });
      }, 100);
    });
  });

  describe('updateHousePoints', () => {
    it('devrait mettre à jour les points d\'une maison', (done) => {
      setTimeout(() => {
        db.updateHousePoints(1, 150, (err, changes) => {
          expect(err).toBeNull();
          expect(changes).toBe(1);
          
          db.getHouseById(1, (err, row) => {
            expect(row.points).toBe(150);
            done();
          });
        });
      }, 100);
    });
  });

  describe('addPoints', () => {
    it('devrait ajouter des points à une maison', (done) => {
      setTimeout(() => {
        db.updateHousePoints(1, 100, () => {
          db.addPoints(1, 50, (err, changes) => {
            expect(err).toBeNull();
            expect(changes).toBe(1);
            
            db.getHouseById(1, (err, row) => {
              expect(row.points).toBe(150);
              done();
            });
          });
        });
      }, 100);
    });

    it('devrait pouvoir retirer des points', (done) => {
      setTimeout(() => {
        db.updateHousePoints(1, 100, () => {
          db.addPoints(1, -30, (err, changes) => {
            expect(err).toBeNull();
            expect(changes).toBe(1);
            
            db.getHouseById(1, (err, row) => {
              expect(row.points).toBe(70);
              done();
            });
          });
        });
      }, 100);
    });
  });

  describe('resetAllScores', () => {
    it('devrait réinitialiser tous les scores à 0', (done) => {
      setTimeout(() => {
        db.updateHousePoints(1, 100, () => {
          db.updateHousePoints(2, 200, () => {
            db.resetAllScores((err, changes) => {
              expect(err).toBeNull();
              expect(changes).toBe(4);
              
              db.getAllHouses((err, rows) => {
                rows.forEach(house => {
                  expect(house.points).toBe(0);
                });
                done();
              });
            });
          });
        });
      }, 100);
    });
  });
});
