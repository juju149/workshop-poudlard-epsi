import express from 'express';
import imaps from 'imap-simple';
import jwt from 'jsonwebtoken';

const router = express.Router();
const JWT_SECRET = process.env.JWT_SECRET || 'hedwige_secret';

// Route de login Outlook
router.post('/login', async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: 'Email et mot de passe requis' });
  }
  // On accepte les identifiants pour envoi SMTP uniquement
  try {
    // Génère un token JWT
    const sessionId = jwt.sign({ email, password }, JWT_SECRET, { expiresIn: '2h' });
    res.json({ sessionId, user: { email } });
  } catch (error) {
    res.status(500).json({ error: 'Erreur serveur lors de la connexion' });
  }
});

// Middleware de vérification du token
export function verifyToken(req, res, next) {
  const authHeader = req.headers['authorization'] || req.headers['x-session-id'];
  const token = authHeader && authHeader.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Token manquant' });
  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();
  } catch {
    res.status(403).json({ error: 'Token invalide' });
  }
}

export default router;
