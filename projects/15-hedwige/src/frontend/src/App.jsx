import React, { useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import MailboxPage from './pages/MailboxPage';
import ComposePage from './pages/ComposePage';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
function App() {
  const [sessionId, setSessionId] = useState(localStorage.getItem('sessionId'));
  const [user, setUser] = useState(null);

  const handleLogin = (newSessionId, userData) => {
    setSessionId(newSessionId);
    setUser(userData);
    localStorage.setItem('sessionId', newSessionId);
  };

  const handleLogout = () => {
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
            element={<LoginPage onLogin={handleLogin} />} 
          />
          <Route 
            path="/mailbox" 
            element={sessionId ? <MailboxPage sessionId={sessionId} user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/compose" 
            element={sessionId ? <ComposePage sessionId={sessionId} user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} 
          />
          <Route path="*" element={<Navigate to={sessionId ? "/mailbox" : "/login"} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
