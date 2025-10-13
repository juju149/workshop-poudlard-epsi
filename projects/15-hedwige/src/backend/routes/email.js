import express from 'express';
import { google } from 'googleapis';
import nodemailer from 'nodemailer';
import { tokenStore } from './auth.js';

const router = express.Router();

/**
 * Middleware to verify session
 */
const verifySession = (req, res, next) => {
  const sessionId = req.headers['x-session-id'];
  
  if (!sessionId) {
    return res.status(401).json({ error: 'Session ID is required' });
  }

  const session = tokenStore.get(sessionId);
  if (!session) {
    return res.status(401).json({ error: 'Invalid session' });
  }

  req.session = session;
  next();
};

/**
 * @route   GET /api/emails
 * @desc    List emails from Gmail
 * @access  Private
 */
router.get('/', verifySession, async (req, res) => {
  try {
    const { maxResults = 10 } = req.query;
    
    const oauth2Client = new google.auth.OAuth2(
      process.env.GOOGLE_CLIENT_ID,
      process.env.GOOGLE_CLIENT_SECRET,
      process.env.GOOGLE_REDIRECT_URI
    );
    oauth2Client.setCredentials(req.session.tokens);

    const gmail = google.gmail({ version: 'v1', auth: oauth2Client });
    
    // List messages
    const response = await gmail.users.messages.list({
      userId: 'me',
      maxResults: parseInt(maxResults)
    });

    const messages = response.data.messages || [];
    
    // Get details for each message
    const emailPromises = messages.map(async (msg) => {
      const detail = await gmail.users.messages.get({
        userId: 'me',
        id: msg.id,
        format: 'full'
      });
      
      const headers = detail.data.payload.headers;
      const subject = headers.find(h => h.name === 'Subject')?.value || 'No Subject';
      const from = headers.find(h => h.name === 'From')?.value || 'Unknown';
      const date = headers.find(h => h.name === 'Date')?.value || '';
      const to = headers.find(h => h.name === 'To')?.value || '';
      
      // Get body
      let body = '';
      if (detail.data.payload.body?.data) {
        body = Buffer.from(detail.data.payload.body.data, 'base64').toString('utf-8');
      } else if (detail.data.payload.parts) {
        const textPart = detail.data.payload.parts.find(part => part.mimeType === 'text/plain');
        if (textPart?.body?.data) {
          body = Buffer.from(textPart.body.data, 'base64').toString('utf-8');
        }
      }
      
      return {
        id: msg.id,
        threadId: detail.data.threadId,
        subject,
        from,
        to,
        date,
        snippet: detail.data.snippet,
        body: body.substring(0, 500) // Limit body preview
      };
    });

    const emails = await Promise.all(emailPromises);
    
    res.json({ emails, total: messages.length });
  } catch (error) {
    console.error('Error fetching emails:', error);
    res.status(500).json({ error: 'Failed to fetch emails' });
  }
});

/**
 * @route   GET /api/emails/:id
 * @desc    Get single email by ID
 * @access  Private
 */
router.get('/:id', verifySession, async (req, res) => {
  try {
    const { id } = req.params;
    
    const oauth2Client = new google.auth.OAuth2(
      process.env.GOOGLE_CLIENT_ID,
      process.env.GOOGLE_CLIENT_SECRET,
      process.env.GOOGLE_REDIRECT_URI
    );
    oauth2Client.setCredentials(req.session.tokens);

    const gmail = google.gmail({ version: 'v1', auth: oauth2Client });
    
    const detail = await gmail.users.messages.get({
      userId: 'me',
      id: id,
      format: 'full'
    });
    
    const headers = detail.data.payload.headers;
    const subject = headers.find(h => h.name === 'Subject')?.value || 'No Subject';
    const from = headers.find(h => h.name === 'From')?.value || 'Unknown';
    const date = headers.find(h => h.name === 'Date')?.value || '';
    const to = headers.find(h => h.name === 'To')?.value || '';
    
    // Get body
    let body = '';
    if (detail.data.payload.body?.data) {
      body = Buffer.from(detail.data.payload.body.data, 'base64').toString('utf-8');
    } else if (detail.data.payload.parts) {
      const textPart = detail.data.payload.parts.find(part => part.mimeType === 'text/plain');
      if (textPart?.body?.data) {
        body = Buffer.from(textPart.body.data, 'base64').toString('utf-8');
      }
    }
    
    res.json({
      id: detail.data.id,
      threadId: detail.data.threadId,
      subject,
      from,
      to,
      date,
      snippet: detail.data.snippet,
      body
    });
  } catch (error) {
    console.error('Error fetching email:', error);
    res.status(500).json({ error: 'Failed to fetch email' });
  }
});

/**
 * @route   POST /api/emails/send
 * @desc    Send an email
 * @access  Private
 */
router.post('/send', verifySession, async (req, res) => {
  try {
    const { to, subject, body } = req.body;

    if (!to || !subject || !body) {
      return res.status(400).json({ 
        error: 'Missing required fields: to, subject, body' 
      });
    }

    const oauth2Client = new google.auth.OAuth2(
      process.env.GOOGLE_CLIENT_ID,
      process.env.GOOGLE_CLIENT_SECRET,
      process.env.GOOGLE_REDIRECT_URI
    );
    oauth2Client.setCredentials(req.session.tokens);

    const gmail = google.gmail({ version: 'v1', auth: oauth2Client });

    // Create email in RFC 2822 format
    const email = [
      `From: ${req.session.user.email}`,
      `To: ${to}`,
      `Subject: ${subject}`,
      '',
      body
    ].join('\n');

    const encodedEmail = Buffer.from(email)
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');

    const result = await gmail.users.messages.send({
      userId: 'me',
      requestBody: {
        raw: encodedEmail
      }
    });

    res.json({ 
      message: 'Email sent successfully',
      id: result.data.id,
      threadId: result.data.threadId
    });
  } catch (error) {
    console.error('Error sending email:', error);
    res.status(500).json({ error: 'Failed to send email' });
  }
});

export default router;
