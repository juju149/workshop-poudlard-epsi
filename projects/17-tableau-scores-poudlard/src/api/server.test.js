const request = require('supertest');
const { app, db } = require('./server');

describe('API des scores de Poudlard', () => {
  afterAll(() => {
    db.close();
  });

  describe('GET /health', () => {
    it('devrait retourner le statut OK', async () => {
      const response = await request(app).get('/health');
      expect(response.status).toBe(200);
      expect(response.body.status).toBe('OK');
      expect(response.body.timestamp).toBeDefined();
    });
  });

  describe('GET /api/houses', () => {
    it('devrait retourner la liste des 4 maisons', async () => {
      const response = await request(app).get('/api/houses');
      expect(response.status).toBe(200);
      expect(response.body.houses).toBeDefined();
      expect(response.body.houses.length).toBe(4);
    });

    it('devrait inclure les noms des maisons', async () => {
      const response = await request(app).get('/api/houses');
      const houseNames = response.body.houses.map(h => h.name);
      expect(houseNames).toContain('Gryffondor');
      expect(houseNames).toContain('Serpentard');
      expect(houseNames).toContain('Poufsouffle');
      expect(houseNames).toContain('Serdaigle');
    });
  });

  describe('GET /api/houses/:id', () => {
    it('devrait retourner une maison spécifique', async () => {
      const response = await request(app).get('/api/houses/1');
      expect(response.status).toBe(200);
      expect(response.body.house).toBeDefined();
      expect(response.body.house.id).toBe(1);
    });

    it('devrait retourner 404 pour une maison inexistante', async () => {
      const response = await request(app).get('/api/houses/999');
      expect(response.status).toBe(404);
    });

    it('devrait retourner 400 pour un ID invalide', async () => {
      const response = await request(app).get('/api/houses/invalid');
      expect(response.status).toBe(400);
    });
  });

  describe('PUT /api/houses/:id', () => {
    it('devrait mettre à jour les points d\'une maison', async () => {
      const response = await request(app)
        .put('/api/houses/1')
        .send({ points: 100 });
      expect(response.status).toBe(200);
      expect(response.body.message).toContain('mis à jour');
    });

    it('devrait refuser des points négatifs', async () => {
      const response = await request(app)
        .put('/api/houses/1')
        .send({ points: -10 });
      expect(response.status).toBe(400);
    });

    it('devrait refuser des points non numériques', async () => {
      const response = await request(app)
        .put('/api/houses/1')
        .send({ points: "invalid" });
      expect(response.status).toBe(400);
    });

    it('devrait retourner 404 pour une maison inexistante', async () => {
      const response = await request(app)
        .put('/api/houses/999')
        .send({ points: 50 });
      expect(response.status).toBe(404);
    });
  });

  describe('POST /api/houses/:id/add', () => {
    beforeEach(async () => {
      await request(app).put('/api/houses/1').send({ points: 0 });
    });

    it('devrait ajouter des points positifs', async () => {
      const response = await request(app)
        .post('/api/houses/1/add')
        .send({ points: 50 });
      expect(response.status).toBe(200);
      
      const checkResponse = await request(app).get('/api/houses/1');
      expect(checkResponse.body.house.points).toBe(50);
    });

    it('devrait pouvoir retirer des points (nombre négatif)', async () => {
      await request(app).put('/api/houses/1').send({ points: 100 });
      
      const response = await request(app)
        .post('/api/houses/1/add')
        .send({ points: -30 });
      expect(response.status).toBe(200);
      
      const checkResponse = await request(app).get('/api/houses/1');
      expect(checkResponse.body.house.points).toBe(70);
    });

    it('devrait refuser des points non numériques', async () => {
      const response = await request(app)
        .post('/api/houses/1/add')
        .send({ points: "invalid" });
      expect(response.status).toBe(400);
    });
  });

  describe('POST /api/reset', () => {
    beforeEach(async () => {
      await request(app).put('/api/houses/1').send({ points: 100 });
      await request(app).put('/api/houses/2').send({ points: 200 });
    });

    it('devrait réinitialiser tous les scores à 0', async () => {
      const response = await request(app).post('/api/reset');
      expect(response.status).toBe(200);
      expect(response.body.message).toContain('réinitialisés');
      
      const housesResponse = await request(app).get('/api/houses');
      housesResponse.body.houses.forEach(house => {
        expect(house.points).toBe(0);
      });
    });
  });

  describe('Route 404', () => {
    it('devrait retourner 404 pour une route inexistante', async () => {
      const response = await request(app).get('/api/invalid');
      expect(response.status).toBe(404);
    });
  });
});
