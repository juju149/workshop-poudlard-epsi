import React, { useState, useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import MailboxPage from './pages/MailboxPage';
import ComposePage from './pages/ComposePage';
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';

const App = () => {
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

  const router = createBrowserRouter([
    {
      path: '/login',
      element: <LoginPage onLogin={handleLogin} />,
    },
    {
      path: '/mailbox',
      element: sessionId ? <MailboxPage sessionId={sessionId} user={user} onLogout={handleLogout} /> : <Navigate to="/login" />,
    },
    {
      path: '/compose',
      element: sessionId ? <ComposePage sessionId={sessionId} user={user} onLogout={handleLogout} /> : <Navigate to="/login" />,
    },
    {
      path: '*',
      element: <Navigate to={sessionId ? "/mailbox" : "/login"} />,
    },
  ], {
    future: {
      v7_relativeSplatPath: true,
    },
  });

  return (
    <div className="app">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
