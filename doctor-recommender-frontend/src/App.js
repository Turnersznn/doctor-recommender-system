import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import Home from './pages/home';
import Dashboard from './pages/dashboard';
import Login from './pages/Login';
import SignUp from './pages/SignUp';

function App() {
  const [user, setUser] = useState(null);
  const [showSignUp, setShowSignUp] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing token on app load
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      try {
        const user = JSON.parse(userData);
        setUser({ token, ...user });
      } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
    setIsLoading(false);
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setShowSignUp(false);
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
      }}>
        <div style={{ color: 'white', fontSize: '18px' }}>Loading...</div>
      </div>
    );
  }

  // If no user is logged in, show only login/signup pages
  if (!user) {
    return (
      <Router>
        <div className="app">
          <Navigation user={user} onLogout={handleLogout} />
          <div className="app-content">
            <Routes>
              <Route path="/" element={
                <div style={{ 
                  padding: '40px', 
                  textAlign: 'center',
                  minHeight: '60vh',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center'
                }}>
                  <h1 style={{ fontSize: '2.5rem', marginBottom: '20px', color: '#1f2937' }}>
                    🏥 Welcome to MediMatch
                  </h1>
                  <p style={{ fontSize: '1.2rem', marginBottom: '30px', color: '#6b7280', maxWidth: '600px' }}>
                    Find the right specialist for your symptoms. Please log in or create an account to get started.
                  </p>
                  <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', justifyContent: 'center' }}>
                    <button 
                      onClick={() => window.location.href = '/login'}
                      style={{
                        padding: '12px 24px',
                        fontSize: '1.1rem',
                        backgroundColor: '#667eea',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease'
                      }}
                      onMouseOver={(e) => e.target.style.backgroundColor = '#5a67d8'}
                      onMouseOut={(e) => e.target.style.backgroundColor = '#667eea'}
                    >
                      Login
                    </button>
                    <button 
                      onClick={() => window.location.href = '/signup'}
                      style={{
                        padding: '12px 24px',
                        fontSize: '1.1rem',
                        backgroundColor: 'transparent',
                        color: '#667eea',
                        border: '2px solid #667eea',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease'
                      }}
                      onMouseOver={(e) => {
                        e.target.style.backgroundColor = '#667eea';
                        e.target.style.color = 'white';
                      }}
                      onMouseOut={(e) => {
                        e.target.style.backgroundColor = 'transparent';
                        e.target.style.color = '#667eea';
                      }}
                    >
                      Sign Up
                    </button>
                  </div>
                </div>
              } />
              <Route path="/dashboard" element={<div style={{ padding: '20px', textAlign: 'center' }}>
                <h2>Please log in to access your dashboard</h2>
                <p>You need to be logged in to view your personalized dashboard.</p>
              </div>} />
              <Route path="/login" element={<Login onLogin={handleLogin} onSwitchToSignUp={() => setShowSignUp(true)} />} />
              <Route path="/signup" element={<SignUp onSwitchToLogin={() => setShowSignUp(false)} />} />
            </Routes>
          </div>
        </div>
      </Router>
    );
  }

  return (
    <Router>
      <div className="app">
        <Navigation user={user} onLogout={handleLogout} />
        <div className="app-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;

