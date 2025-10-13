import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import MailboxPage from './pages/MailboxPage';
import ComposePage from './pages/ComposePage';
import './styles/App.css';

function App() {
  const [sessionId, setSessionId] = useState(localStorage.getItem('sessionId'));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (sessionId) {
      // Verify session is still valid
      fetch(`/api/auth/session/${sessionId}`)
        .then(res => res.json())
        .then(data => {
          if (data.user) {
            setUser(data.user);
          } else {
            handleLogout();
          }
        })
        .catch(() => handleLogout());
    }
  }, [sessionId]);

  const handleLogin = (newSessionId, userData) => {
    setSessionId(newSessionId);
    setUser(userData);
    localStorage.setItem('sessionId', newSessionId);
  };

  const handleLogout = () => {
    if (sessionId) {
      fetch(`/api/auth/logout/${sessionId}`, { method: 'DELETE' });
    }
    setSessionId(null);
    setUser(null);
    localStorage.removeItem('sessionId');
  };

  return (
    <Router>
      <div className="app">
        <Routes>
          <Route 
            path="/login" 
            element={
              sessionId ? <Navigate to="/mailbox" /> : <LoginPage onLogin={handleLogin} />
            } 
          />
          <Route 
            path="/mailbox" 
            element={
              sessionId ? (
                <MailboxPage sessionId={sessionId} user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            } 
          />
          <Route 
            path="/compose" 
            element={
              sessionId ? (
                <ComposePage sessionId={sessionId} user={user} onLogout={handleLogout} />
              ) : (
                <Navigate to="/login" />
              )
            } 
          />
          <Route path="*" element={<Navigate to={sessionId ? "/mailbox" : "/login"} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
