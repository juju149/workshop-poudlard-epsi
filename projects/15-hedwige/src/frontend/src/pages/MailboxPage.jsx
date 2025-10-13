import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import EmailList from '../components/EmailList';
import EmailDetail from '../components/EmailDetail';
import '../styles/MailboxPage.css';

function MailboxPage({ sessionId, user, onLogout }) {
  const [emails, setEmails] = useState([]);
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchEmails();
  }, [sessionId]);

  const fetchEmails = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch('/api/emails?maxResults=20', {
        headers: {
          'x-session-id': sessionId
        }
      });

      const data = await response.json();

      if (response.ok) {
        setEmails(data.emails || []);
      } else {
        setError(data.error || 'Failed to fetch emails');
      }
    } catch (err) {
      setError('Failed to connect to server');
    } finally {
      setLoading(false);
    }
  };

  const handleEmailClick = async (emailId) => {
    try {
      const response = await fetch(`/api/emails/${emailId}`, {
        headers: {
          'x-session-id': sessionId
        }
      });

      const data = await response.json();

      if (response.ok) {
        setSelectedEmail(data);
      } else {
        setError(data.error || 'Failed to fetch email');
      }
    } catch (err) {
      setError('Failed to load email');
    }
  };

  const handleBackToList = () => {
    setSelectedEmail(null);
  };

  const handleCompose = () => {
    navigate('/compose');
  };

  return (
    <div className="mailbox-page">
      <header className="mailbox-header">
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

      <div className="mailbox-content">
        <div className="mailbox-sidebar">
          <button className="compose-btn" onClick={handleCompose}>
            ✉️ Compose
          </button>
          <button className="refresh-btn" onClick={fetchEmails}>
            🔄 Refresh
          </button>
        </div>

        <div className="mailbox-main">
          {loading ? (
            <div className="loading">Loading emails...</div>
          ) : error ? (
            <div className="error">{error}</div>
          ) : selectedEmail ? (
            <EmailDetail 
              email={selectedEmail} 
              onBack={handleBackToList} 
            />
          ) : (
            <EmailList 
              emails={emails} 
              onEmailClick={handleEmailClick}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default MailboxPage;
