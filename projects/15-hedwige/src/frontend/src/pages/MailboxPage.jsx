import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import EmailList from '../components/EmailList';
import EmailDetail from '../components/EmailDetail';
import '../styles/MailboxPage.css';

function MailboxPage() {
  const [tab, setTab] = useState('received');
  const [selectedEmail, setSelectedEmail] = useState(null);
  const navigate = useNavigate();

  // Mocks de mails reçus
  const receivedEmails = [
    {
      id: 1,
      from: 'Minerva McGonagall <mcgonagall@poudlard.fr>',
      to: 'Harry Potter <harry@poudlard.fr>',
      subject: 'Bienvenue à Poudlard',
      date: '2025-10-10T10:00:00Z',
      body: 'Cher Harry, bienvenue à Poudlard!'
    },
    {
      id: 2,
      from: 'Hermione Granger <hermione@poudlard.fr>',
      to: 'Harry Potter <harry@poudlard.fr>',
      subject: 'Devoirs',
      date: '2025-10-11T12:00:00Z',
      body: 'N’oublie pas tes devoirs de potions!'
    }
  ];

  // Mocks de mails envoyés
  const sentEmails = [
    {
      id: 101,
      from: 'Harry Potter <harry@poudlard.fr>',
      to: 'Minerva McGonagall <mcgonagall@poudlard.fr>',
      subject: 'Merci !',
      date: '2025-10-12T09:00:00Z',
      body: 'Merci pour la lettre de bienvenue.'
    },
    {
      id: 102,
      from: 'Harry Potter <harry@poudlard.fr>',
      to: 'Hermione Granger <hermione@poudlard.fr>',
      subject: 'Réponse devoirs',
      date: '2025-10-12T10:00:00Z',
      body: 'Merci Hermione, je vais m’y mettre !'
    }
  ];

  const handleEmailClick = (emailId) => {
    const emails = tab === 'received' ? receivedEmails : sentEmails;
    const email = emails.find(e => e.id === emailId);
    setSelectedEmail(email);
  };

  const handleBackToList = () => {
    setSelectedEmail(null);
  };

  const handleLogout = () => {
    localStorage.removeItem('sessionId');
    navigate('/login');
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
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <div className="mailbox-content">
        <div className="mailbox-sidebar">
          <button className="compose-btn" onClick={handleCompose}>
            ✉️ Compose
          </button>
          <div className="mailbox-tabs sidebar-tabs">
            <button
              className={tab === 'received' ? 'tab-active' : ''}
              onClick={() => { setSelectedEmail(null); setTab('received'); }}
            >📥 Mail reçu</button>
            <button
              className={tab === 'sent' ? 'tab-active' : ''}
              onClick={() => { setSelectedEmail(null); setTab('sent'); }}
            >📤 Mail envoyé</button>
          </div>
        </div>

        <div className="mailbox-main">
          {selectedEmail ? (
            <EmailDetail email={selectedEmail} onBack={handleBackToList} />
          ) : (
            <EmailList
              emails={tab === 'received' ? receivedEmails : sentEmails}
              onEmailClick={handleEmailClick}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default MailboxPage;
