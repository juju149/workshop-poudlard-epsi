import express from 'express';
import { google } from 'googleapis';

const router = express.Router();

// Store tokens in memory (in production, use a database)
const tokenStore = new Map();

/**
 * @route   GET /api/auth/google
 * @desc    Initiate Google OAuth2 flow
 * @access  Public
 */
router.get('/google', (req, res) => {
  const oauth2Client = new google.auth.OAuth2(
    process.env.GOOGLE_CLIENT_ID,
    process.env.GOOGLE_CLIENT_SECRET,
    process.env.GOOGLE_REDIRECT_URI
  );

  const scopes = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
  ];

  const url = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: scopes,
    prompt: 'consent'
  });

  res.json({ authUrl: url });
});

/**
 * @route   POST /api/auth/google/callback
 * @desc    Handle Google OAuth2 callback
 * @access  Public
 */
router.post('/callback', async (req, res) => {
  try {
    const { code } = req.body;

    if (!code) {
      return res.status(400).json({ error: 'Authorization code is required' });
    }

    const oauth2Client = new google.auth.OAuth2(
      process.env.GOOGLE_CLIENT_ID,
      process.env.GOOGLE_CLIENT_SECRET,
      process.env.GOOGLE_REDIRECT_URI
    );

    const { tokens } = await oauth2Client.getToken(code);
    oauth2Client.setCredentials(tokens);

    // Get user info
    const oauth2 = google.oauth2({ version: 'v2', auth: oauth2Client });
    const { data } = await oauth2.userinfo.get();

    // Store tokens (in production, use a proper session/database)
    const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    tokenStore.set(sessionId, {
      tokens,
      user: {
        id: data.id,
        email: data.email,
        name: data.name,
        picture: data.picture
      }
    });

    res.json({
      sessionId,
      user: {
        id: data.id,
        email: data.email,
        name: data.name,
        picture: data.picture
      }
    });
  } catch (error) {
    console.error('OAuth callback error:', error);
    res.status(500).json({ error: 'Failed to authenticate with Google' });
  }
});

/**
 * @route   GET /api/auth/session/:sessionId
 * @desc    Get session info
 * @access  Public
 */
router.get('/session/:sessionId', (req, res) => {
  const { sessionId } = req.params;
  const session = tokenStore.get(sessionId);

  if (!session) {
    return res.status(404).json({ error: 'Session not found' });
  }

  res.json({ user: session.user });
});

/**
 * @route   DELETE /api/auth/logout/:sessionId
 * @desc    Logout and clear session
 * @access  Public
 */
router.delete('/logout/:sessionId', (req, res) => {
  const { sessionId } = req.params;
  tokenStore.delete(sessionId);
  res.json({ message: 'Logged out successfully' });
});

// Export token store for use in other routes
export { tokenStore };
export default router;
