import React, { useState } from 'react';
import '../styles/LoginPage.css';

function LoginPage({ onLogin }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGoogleLogin = async () => {
    try {
      setLoading(true);
      setError(null);

      // Get OAuth URL
      const response = await fetch('/api/auth/google');
      const data = await response.json();

      if (data.authUrl) {
        // Open OAuth popup
        const width = 500;
        const height = 600;
        const left = window.screen.width / 2 - width / 2;
        const top = window.screen.height / 2 - height / 2;
        
        const popup = window.open(
          data.authUrl,
          'Google OAuth',
          `width=${width},height=${height},left=${left},top=${top}`
        );

        // Listen for OAuth callback
        const checkPopup = setInterval(() => {
          try {
            if (popup.closed) {
              clearInterval(checkPopup);
              setLoading(false);
            }
            
            // Try to get the code from popup URL
            const popupUrl = popup.location.href;
            if (popupUrl.includes('code=')) {
              const urlParams = new URLSearchParams(popup.location.search);
              const code = urlParams.get('code');
              
              clearInterval(checkPopup);
              popup.close();
              handleCallback(code);
            }
          } catch (e) {
            // Cross-origin error - popup hasn't redirected yet
          }
        }, 500);
      }
    } catch (err) {
      setError('Failed to initiate Google login');
      setLoading(false);
    }
  };

  const handleCallback = async (code) => {
    try {
      const response = await fetch('/api/auth/callback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code })
      });

      const data = await response.json();

      if (data.sessionId && data.user) {
        onLogin(data.sessionId, data.user);
      } else {
        setError('Failed to authenticate');
      }
    } catch (err) {
      setError('Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>🦉 Hedwige</h1>
          <p>Your magical email companion</p>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <button 
          className="google-login-btn" 
          onClick={handleGoogleLogin}
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="spinner"></span>
              Connecting...
            </>
          ) : (
            <>
              <svg viewBox="0 0 24 24" width="20" height="20">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              Sign in with Google
            </>
          )}
        </button>

        <div className="login-info">
          <p>Connect with your Google account to access your emails</p>
          <ul>
            <li>View and read your emails</li>
            <li>Send new emails</li>
            <li>Secure OAuth2 authentication</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
