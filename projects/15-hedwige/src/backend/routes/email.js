import dotenv from 'dotenv';
dotenv.config();
import express from 'express';
import nodemailer from 'nodemailer';
import imaps from 'imap-simple';

const router = express.Router();

// Adresse et mot de passe Outlook via variables d'environnement
const OUTLOOK_EMAIL = process.env.OUTLOOK_EMAIL;
const OUTLOOK_PASSWORD = process.env.OUTLOOK_PASSWORD;


/**
 * @route   GET /api/emails
 * @desc    Liste les emails depuis Outlook (IMAP)
 * @access  Private
 */
router.get('/', async (req, res) => {
  const { maxResults = 10 } = req.query;
  const config = {
    imap: {
      user: OUTLOOK_EMAIL,
      password: OUTLOOK_PASSWORD,
      host: 'outlook.office365.com',
      port: 993,
      tls: true,
      authTimeout: 10000
    }
  };
  try {
    const connection = await imaps.connect(config);
    await connection.openBox('INBOX');
    const searchCriteria = ['ALL'];
    const fetchOptions = {
      bodies: ['HEADER', 'TEXT'],
      struct: true
    };
    const messages = await connection.search(searchCriteria, fetchOptions);
    const emails = messages.slice(0, maxResults).map(item => {
      const header = item.parts.find(part => part.which === 'HEADER');
      const text = item.parts.find(part => part.which === 'TEXT');
      return {
        subject: header?.body.subject?.[0] || '',
        from: header?.body.from?.[0] || '',
        to: header?.body.to?.[0] || '',
        date: header?.body.date?.[0] || '',
        body: text?.body?.substring(0, 500) || '',
        id: item.attributes.uid
      };
    });
    res.json({ emails, total: emails.length });
  } catch (error) {
    console.error('Error fetching emails:', error);
    res.status(500).json({ error: 'Failed to fetch emails' });
  }
});

/**
 * @route   POST /api/emails/send
 * @desc    Send an email
 * @access  Private
 */
router.post('/send', async (req, res) => {
  try {
    const { to, subject, body } = req.body;
    if (!to || !subject || !body) {
      return res.status(400).json({ error: 'Missing required fields: to, subject, body' });
    }

    // Création du transporteur SMTP Outlook
    const transporter = nodemailer.createTransport({
      host: 'smtp.office365.com',
      port: 587,
      secure: false,
      auth: {
        user: OUTLOOK_EMAIL,
        pass: OUTLOOK_PASSWORD
      }
    });

    // Envoi du mail
    const info = await transporter.sendMail({
      from: OUTLOOK_EMAIL,
      to,
      subject,
      text: body
    });

    res.json({ message: 'Email sent successfully', id: info.messageId });
  } catch (error) {
    console.error('Error sending email:', error);
    res.status(500).json({ error: 'Failed to send email' });
  }
});

export default router;
