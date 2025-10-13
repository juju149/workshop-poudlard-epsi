import React from 'react';
import '../styles/EmailList.css';

function EmailList({ emails, onEmailClick }) {
  if (!emails || emails.length === 0) {
    return (
      <div className="email-list-empty">
        <p>No emails found</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return date.toLocaleDateString('en-US', { weekday: 'short' });
    } else {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
  };

  const extractEmail = (from) => {
    const match = from.match(/<(.+)>/);
    return match ? match[1] : from;
  };

  const extractName = (from) => {
    const match = from.match(/^(.+?)\s*</);
    return match ? match[1].replace(/"/g, '') : from;
  };

  return (
    <div className="email-list">
      <h2>Inbox ({emails.length})</h2>
      <div className="email-items">
        {emails.map((email) => (
          <div 
            key={email.id} 
            className="email-item"
            onClick={() => onEmailClick(email.id)}
          >
            <div className="email-item-header">
              <span className="email-from">{extractName(email.from)}</span>
              <span className="email-date">{formatDate(email.date)}</span>
            </div>
            <div className="email-subject">{email.subject || '(No Subject)'}</div>
            <div className="email-snippet">{email.snippet}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default EmailList;
