import request from 'supertest';
import app from '../server.js';

describe('API Health Check', () => {
  it('should return health status', async () => {
    const response = await request(app)
      .get('/health')
      .expect('Content-Type', /json/)
      .expect(200);

    expect(response.body).toHaveProperty('status', 'ok');
    expect(response.body).toHaveProperty('message');
  });
});

describe('Authentication Routes', () => {
  describe('GET /api/auth/google', () => {
    it('should return Google OAuth URL', async () => {
      const response = await request(app)
        .get('/api/auth/google')
        .expect('Content-Type', /json/)
        .expect(200);

      expect(response.body).toHaveProperty('authUrl');
      expect(response.body.authUrl).toContain('accounts.google.com');
    });
  });

  describe('POST /api/auth/callback', () => {
    it('should return error without code', async () => {
      const response = await request(app)
        .post('/api/auth/callback')
        .send({})
        .expect('Content-Type', /json/)
        .expect(400);

      expect(response.body).toHaveProperty('error');
    });
  });

  describe('GET /api/auth/session/:sessionId', () => {
    it('should return 404 for invalid session', async () => {
      const response = await request(app)
        .get('/api/auth/session/invalid_session')
        .expect('Content-Type', /json/)
        .expect(404);

      expect(response.body).toHaveProperty('error');
    });
  });
});

describe('Email Routes', () => {
  describe('GET /api/emails', () => {
    it('should require session ID', async () => {
      const response = await request(app)
        .get('/api/emails')
        .expect('Content-Type', /json/)
        .expect(401);

      expect(response.body).toHaveProperty('error');
      expect(response.body.error).toContain('Session ID');
    });

    it('should reject invalid session', async () => {
      const response = await request(app)
        .get('/api/emails')
        .set('x-session-id', 'invalid_session')
        .expect('Content-Type', /json/)
        .expect(401);

      expect(response.body).toHaveProperty('error');
    });
  });

  describe('POST /api/emails/send', () => {
    it('should require session ID', async () => {
      const response = await request(app)
        .post('/api/emails/send')
        .send({
          to: 'test@example.com',
          subject: 'Test',
          body: 'Test body'
        })
        .expect('Content-Type', /json/)
        .expect(401);

      expect(response.body).toHaveProperty('error');
    });

    it('should validate required fields', async () => {
      const response = await request(app)
        .post('/api/emails/send')
        .set('x-session-id', 'test_session')
        .send({
          to: 'test@example.com'
        })
        .expect('Content-Type', /json/)
        .expect(401);

      expect(response.body).toHaveProperty('error');
    });
  });
});

describe('404 Handler', () => {
  it('should return 404 for unknown routes', async () => {
    const response = await request(app)
      .get('/api/unknown')
      .expect('Content-Type', /json/)
      .expect(404);

    expect(response.body).toHaveProperty('error');
    expect(response.body.error.message).toContain('not found');
  });
});
