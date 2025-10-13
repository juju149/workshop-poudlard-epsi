import React from 'react';
import '../styles/EmailDetail.css';

function EmailDetail({ email, onBack }) {
  if (!email) {
    return <div className="email-detail-empty">Select an email to read</div>;
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const extractEmail = (from) => {
    const match = from.match(/<(.+)>/);
    return match ? match[1] : from;
  };

  const extractName = (from) => {
    const match = from.match(/^(.+?)\s*</);
    return match ? match[1].replace(/"/g, '') : extractEmail(from);
  };

  return (
    <div className="email-detail">
      <div className="email-detail-header">
        <button className="back-btn" onClick={onBack}>
          ← Back to Inbox
        </button>
      </div>

      <div className="email-detail-content">
        <h2 className="email-detail-subject">{email.subject || '(No Subject)'}</h2>
        
        <div className="email-detail-meta">
          <div className="email-from-info">
            <strong>{extractName(email.from)}</strong>
            <span className="email-address">&lt;{extractEmail(email.from)}&gt;</span>
          </div>
          <div className="email-to-info">
            <span>To: {email.to}</span>
          </div>
          <div className="email-date-info">
            {formatDate(email.date)}
          </div>
        </div>

        <div className="email-body">
          <pre>{email.body || email.snippet}</pre>
        </div>
      </div>
    </div>
  );
}

export default EmailDetail;
