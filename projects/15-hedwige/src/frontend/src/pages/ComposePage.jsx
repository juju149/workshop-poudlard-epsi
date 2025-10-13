import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/ComposePage.css';

function ComposePage({ sessionId, user, onLogout }) {
  const [to, setTo] = useState('');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!to || !subject || !body) {
      setError('Please fill in all fields');
      return;
    }

    try {
      setSending(true);
      setError(null);
      setSuccess(false);

      const response = await fetch('/api/emails/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-session-id': sessionId
        },
        body: JSON.stringify({ to, subject, body })
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(true);
        setTimeout(() => {
          navigate('/mailbox');
        }, 2000);
      } else {
        setError(data.error || 'Failed to send email');
      }
    } catch (err) {
      setError('Failed to send email');
    } finally {
      setSending(false);
    }
  };

  const handleCancel = () => {
    navigate('/mailbox');
  };

  return (
    <div className="compose-page">
      <header className="compose-header">
        <div className="header-left">
          <h1>🦉 Hedwige</h1>
        </div>
        <div className="header-right">
          {user && (
            <div className="user-info">
              {user.picture && <img src={user.picture} alt={user.name} />}
              <span>{user.name}</span>
            </div>
          )}
          <button onClick={onLogout} className="logout-btn">Logout</button>
        </div>
      </header>

      <div className="compose-content">
        <div className="compose-container">
          <h2>New Message</h2>

          {error && <div className="error-message">{error}</div>}
          {success && <div className="success-message">Email sent successfully!</div>}

          <form onSubmit={handleSubmit} className="compose-form">
            <div className="form-group">
              <label htmlFor="to">To:</label>
              <input
                type="email"
                id="to"
                value={to}
                onChange={(e) => setTo(e.target.value)}
                placeholder="recipient@example.com"
                disabled={sending}
              />
            </div>

            <div className="form-group">
              <label htmlFor="subject">Subject:</label>
              <input
                type="text"
                id="subject"
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                placeholder="Email subject"
                disabled={sending}
              />
            </div>

            <div className="form-group">
              <label htmlFor="body">Message:</label>
              <textarea
                id="body"
                value={body}
                onChange={(e) => setBody(e.target.value)}
                placeholder="Write your message here..."
                rows="15"
                disabled={sending}
              />
            </div>

            <div className="form-actions">
              <button 
                type="submit" 
                className="send-btn"
                disabled={sending}
              >
                {sending ? 'Sending...' : 'Send Email'}
              </button>
              <button 
                type="button" 
                className="cancel-btn"
                onClick={handleCancel}
                disabled={sending}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ComposePage;
