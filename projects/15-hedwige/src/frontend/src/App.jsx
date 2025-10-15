import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import MailboxPage from './pages/MailboxPage';
import ComposePage from './pages/ComposePage';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route 
            path="/mailbox" 
            element={<MailboxPage />} 
          />
          <Route 
            path="/compose" 
            element={<ComposePage />} 
          />
          <Route path="*" element={<Navigate to="/mailbox" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
