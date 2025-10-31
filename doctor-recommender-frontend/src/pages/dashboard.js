import React, { useState, useEffect } from 'react';
import './dashboard.css';

const Dashboard = () => {
  const [userData, setUserData] = useState({
    ratingHistory: [],
    favoriteDoctors: [],
    searchHistory: [],
    statistics: {
      totalRatings: 0,
      averageRating: 0,
      mostRatedSpecialty: '',
      totalSearches: 0
    }
  });
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadUserData();
  }, []);

  const loadUserData = async () => {
    try {
      // Get current user from localStorage (user must be logged in to access dashboard)
      const userData = localStorage.getItem('user');
      const user = userData ? JSON.parse(userData) : null;
      const userName = user?.username || 'User';

      console.log('Loading dashboard data for user:', userName);

      // Initialize default data
      let ratingsData = { ratings: [], averageRating: 0, mostRatedSpecialty: 'None' };
      let favoritesData = { favorites: [] };

      // Load user's rating history
      try {
        const ratingsResponse = await fetch(`http://localhost:5000/api/ratings/user-history?userName=${userName}`);
        if (ratingsResponse.ok) {
          ratingsData = await ratingsResponse.json();
          console.log('Ratings data loaded:', ratingsData);
        } else {
          console.warn('Failed to load ratings:', ratingsResponse.status);
        }
      } catch (error) {
        console.warn('Error loading ratings:', error);
      }

      // Load favorite doctors
      try {
        const favoritesResponse = await fetch(`http://localhost:5000/api/favorites/user-favorites?userName=${userName}`);
        if (favoritesResponse.ok) {
          favoritesData = await favoritesResponse.json();
          console.log('Favorites data loaded:', favoritesData);
        } else {
          console.warn('Failed to load favorites:', favoritesResponse.status);
        }
      } catch (error) {
        console.warn('Error loading favorites:', error);
      }

      // Load search history (user-specific)
      const searchHistory = JSON.parse(localStorage.getItem(`searchHistory_${userName}`) || '[]');
      console.log('Search history loaded:', searchHistory.length, 'items');

      // If no data exists, add some sample data for demo purposes
      if (ratingsData.ratings.length === 0 && favoritesData.favorites.length === 0 && searchHistory.length === 0) {
        console.log('No existing data found, adding sample data for demo');

        // Add sample search history
        const sampleSearchHistory = [
          {
            symptoms: ['headache', 'fever'],
            diagnoses: [{ disease: 'Common Cold', specialist: 'General Practitioner' }],
            timestamp: new Date(Date.now() - 86400000).toISOString() // 1 day ago
          },
          {
            symptoms: ['chest_pain', 'shortness_of_breath'],
            diagnoses: [{ disease: 'Heart Condition', specialist: 'Cardiologist' }],
            timestamp: new Date(Date.now() - 172800000).toISOString() // 2 days ago
          }
        ];

        localStorage.setItem(`searchHistory_${userName}`, JSON.stringify(sampleSearchHistory));

        setUserData({
          ratingHistory: [],
          favoriteDoctors: [],
          searchHistory: sampleSearchHistory,
          statistics: {
            totalRatings: 0,
            averageRating: 0,
            mostRatedSpecialty: 'None',
            totalSearches: sampleSearchHistory.length
          }
        });
      } else {
        setUserData({
          ratingHistory: ratingsData.ratings || [],
          favoriteDoctors: favoritesData.favorites || [],
          searchHistory: searchHistory,
          statistics: {
            totalRatings: ratingsData.ratings?.length || 0,
            averageRating: ratingsData.averageRating || 0,
            mostRatedSpecialty: ratingsData.mostRatedSpecialty || 'None',
            totalSearches: searchHistory.length
          }
        });
      }

      console.log('Dashboard data loaded successfully');
    } catch (error) {
      console.error('Error loading user data:', error);
      setError('Failed to load dashboard data. Please try refreshing the page.');
    } finally {
      setLoading(false);
    }
  };

  const removeFavorite = async (doctorId) => {
    try {
      const userData = localStorage.getItem('user');
      const user = userData ? JSON.parse(userData) : null;
      const userName = user?.username || 'User';
      
      await fetch(`http://localhost:5000/api/favorites/${doctorId}?userName=${userName}`, {
        method: 'DELETE'
      });
      setUserData(prev => ({
        ...prev,
        favoriteDoctors: prev.favoriteDoctors.filter(doc => doc.doctorId !== doctorId)
      }));
    } catch (error) {
      console.error('Error removing favorite:', error);
    }
  };

  const clearSearchHistory = () => {
    const userData = localStorage.getItem('user');
    const user = userData ? JSON.parse(userData) : null;
    const userName = user?.username || 'User';
    
    localStorage.removeItem(`searchHistory_${userName}`);
    setUserData(prev => ({
      ...prev,
      searchHistory: [],
      statistics: {
        ...prev.statistics,
        totalSearches: 0
      }
    }));
  };

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '60vh',
        flexDirection: 'column',
        gap: '20px'
      }}>
        <div style={{
          fontSize: '2rem',
          animation: 'spin 1s linear infinite'
        }}>⏳</div>
        <div style={{ fontSize: '1.2rem', color: '#666' }}>Loading your dashboard...</div>
        <style>{`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '60vh',
        flexDirection: 'column',
        gap: '20px'
      }}>
        <div style={{ fontSize: '3rem' }}>⚠️</div>
        <div style={{ fontSize: '1.2rem', color: '#dc2626', textAlign: 'center' }}>{error}</div>
        <button
          onClick={() => {
            setError(null);
            setLoading(true);
            loadUserData();
          }}
          style={{
            padding: '10px 20px',
            backgroundColor: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '1rem'
          }}
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard" style={{ 
      maxWidth: '1200px', 
      margin: '0 auto', 
      marginTop: '20px',
      padding: '20px',
      fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      minHeight: 'calc(100vh - 70px)'
    }}>
      <div className="dashboard-header" style={{
        textAlign: 'center',
        marginBottom: '30px',
        marginTop: '20px',
        padding: '20px',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        borderRadius: '12px'
      }}>
        <h1 style={{ margin: '0 0 10px 0', fontSize: '2.5rem', fontWeight: '600' }}>🏥 Your Health Dashboard</h1>
        <p style={{ margin: '0', fontSize: '1.1rem', opacity: '0.9' }}>Track your doctor interactions and health journey</p>
      </div>

      <div className="dashboard-stats" style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '20px',
        marginBottom: '30px'
      }}>
        <div className="stat-card" style={{
          background: 'white',
          padding: '20px',
          borderRadius: '10px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          textAlign: 'center',
          transition: 'transform 0.2s'
        }}>
          <div className="stat-number" style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#667eea', marginBottom: '5px' }}>{userData.statistics.totalRatings}</div>
          <div className="stat-label" style={{ color: '#666', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Doctors Rated</div>
        </div>
        <div className="stat-card" style={{
          background: 'white',
          padding: '20px',
          borderRadius: '10px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          textAlign: 'center',
          transition: 'transform 0.2s'
        }}>
          <div className="stat-number" style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#667eea', marginBottom: '5px' }}>{userData.statistics.averageRating.toFixed(1)}</div>
          <div className="stat-label" style={{ color: '#666', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Avg Rating Given</div>
        </div>
        <div className="stat-card" style={{
          background: 'white',
          padding: '20px',
          borderRadius: '10px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          textAlign: 'center',
          transition: 'transform 0.2s'
        }}>
          <div className="stat-number" style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#667eea', marginBottom: '5px' }}>{userData.favoriteDoctors.length}</div>
          <div className="stat-label" style={{ color: '#666', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Favorite Doctors</div>
        </div>
        <div className="stat-card" style={{
          background: 'white',
          padding: '20px',
          borderRadius: '10px',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          textAlign: 'center',
          transition: 'transform 0.2s'
        }}>
          <div className="stat-number" style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#667eea', marginBottom: '5px' }}>{userData.statistics.totalSearches}</div>
          <div className="stat-label" style={{ color: '#666', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Symptom Searches</div>
        </div>
      </div>

      <div className="dashboard-tabs" style={{
        display: 'flex',
        gap: '10px',
        marginBottom: '30px',
        borderBottom: '2px solid #eee',
        paddingBottom: '10px'
      }}>
        <button 
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
          style={{
            padding: '12px 24px',
            border: 'none',
            background: activeTab === 'overview' ? '#667eea' : '#f8f9fa',
            color: activeTab === 'overview' ? 'white' : '#666',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '500',
            transition: 'all 0.2s'
          }}
        >
          Overview
        </button>
        <button 
          className={`tab-button ${activeTab === 'ratings' ? 'active' : ''}`}
          onClick={() => setActiveTab('ratings')}
          style={{
            padding: '12px 24px',
            border: 'none',
            background: activeTab === 'ratings' ? '#667eea' : '#f8f9fa',
            color: activeTab === 'ratings' ? 'white' : '#666',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '500',
            transition: 'all 0.2s'
          }}
        >
          My Ratings ({userData.ratingHistory.length})
        </button>
        <button 
          className={`tab-button ${activeTab === 'favorites' ? 'active' : ''}`}
          onClick={() => setActiveTab('favorites')}
          style={{
            padding: '12px 24px',
            border: 'none',
            background: activeTab === 'favorites' ? '#667eea' : '#f8f9fa',
            color: activeTab === 'favorites' ? 'white' : '#666',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '500',
            transition: 'all 0.2s'
          }}
        >
          Favorites ({userData.favoriteDoctors.length})
        </button>
        <button 
          className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
          style={{
            padding: '12px 24px',
            border: 'none',
            background: activeTab === 'history' ? '#667eea' : '#f8f9fa',
            color: activeTab === 'history' ? 'white' : '#666',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: '500',
            transition: 'all 0.2s'
          }}
        >
          Search History ({userData.searchHistory.length})
        </button>
      </div>

      <div className="dashboard-content" style={{
        background: 'white',
        borderRadius: '12px',
        padding: '30px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        minHeight: '400px'
      }}>
        {activeTab === 'overview' && (
          <div className="overview-tab">
            <div className="overview-section" style={{ marginBottom: '30px' }}>
              <h3 style={{ color: '#333', marginBottom: '15px', fontSize: '1.3rem' }}>Recent Activity</h3>
              {userData.ratingHistory.length > 0 ? (
                <div className="recent-ratings" style={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '10px'
                }}>
                  {userData.ratingHistory.slice(0, 3).map((rating, index) => (
                    <div key={index} className="recent-rating" style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '12px',
                      background: '#f8f9fa',
                      borderRadius: '8px'
                    }}>
                      <div className="rating-info" style={{
                        display: 'flex',
                        flexDirection: 'column',
                        gap: '5px'
                      }}>
                        <span className="doctor-name" style={{ fontWeight: '500', color: '#333' }}>{rating.doctorName}</span>
                        <span className="rating-stars" style={{ color: '#ffc107', fontSize: '14px' }}>
                          {'★'.repeat(rating.rating)}{'☆'.repeat(5 - rating.rating)}
                        </span>
                      </div>
                      <span className="rating-date" style={{ color: '#666', fontSize: '12px' }}>
                        {new Date(rating.timestamp).toLocaleDateString()}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="no-data" style={{ textAlign: 'center', padding: '40px', color: '#666' }}>No recent ratings</p>
              )}
            </div>

            <div className="overview-section" style={{ marginBottom: '30px' }}>
              <h3 style={{ color: '#333', marginBottom: '15px', fontSize: '1.3rem' }}>Most Rated Specialty</h3>
              <p className="specialty-info" style={{
                fontSize: '1.1rem',
                color: '#667eea',
                fontWeight: '500'
              }}>
                {userData.statistics.mostRatedSpecialty || 'No ratings yet'}
              </p>
            </div>

            <div className="overview-section" style={{ marginBottom: '30px' }}>
              <h3 style={{ color: '#333', marginBottom: '15px', fontSize: '1.3rem' }}>Quick Actions</h3>
              <div className="quick-actions" style={{
                display: 'flex',
                gap: '15px',
                flexWrap: 'wrap'
              }}>
                <button className="action-button" onClick={() => window.location.href = '/'} style={{
                  padding: '12px 20px',
                  border: 'none',
                  background: '#667eea',
                  color: 'white',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                  transition: 'background 0.2s'
                }}>
                  🔍 Find New Doctor
                </button>
                <button className="action-button" onClick={() => setActiveTab('ratings')} style={{
                  padding: '12px 20px',
                  border: 'none',
                  background: '#667eea',
                  color: 'white',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                  transition: 'background 0.2s'
                }}>
                  ⭐ Rate Doctors
                </button>
                <button className="action-button" onClick={() => setActiveTab('favorites')} style={{
                  padding: '12px 20px',
                  border: 'none',
                  background: '#667eea',
                  color: 'white',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                  transition: 'background 0.2s'
                }}>
                  ❤️ View Favorites
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'ratings' && (
          <div className="ratings-tab">
            <h3 style={{ color: '#333', marginBottom: '15px', fontSize: '1.3rem' }}>My Doctor Ratings</h3>
            {userData.ratingHistory.length > 0 ? (
              <div className="ratings-list" style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '15px'
              }}>
                {userData.ratingHistory.map((rating, index) => (
                  <div key={index} className="rating-item" style={{
                    padding: '20px',
                    border: '1px solid #e9ecef',
                    borderRadius: '8px',
                    background: '#f8f9fa'
                  }}>
                    <div className="rating-header" style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      marginBottom: '10px'
                    }}>
                      <span className="doctor-name" style={{ fontWeight: '500', color: '#333' }}>{rating.doctorName}</span>
                      <span className="rating-stars" style={{ color: '#ffc107', fontSize: '14px' }}>
                        {'★'.repeat(rating.rating)}{'☆'.repeat(5 - rating.rating)}
                      </span>
                    </div>
                    <div className="rating-details" style={{
                      display: 'flex',
                      gap: '20px',
                      fontSize: '14px',
                      color: '#666'
                    }}>
                      <span className="specialty">{rating.specialty}</span>
                      <span className="date">{new Date(rating.timestamp).toLocaleDateString()}</span>
                    </div>
                    {rating.review && (
                      <div className="rating-review" style={{
                        marginTop: '10px',
                        padding: '10px',
                        background: 'white',
                        borderRadius: '6px',
                        fontStyle: 'italic',
                        color: '#555'
                      }}>
                        "{rating.review}"
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data" style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
                <p style={{ marginBottom: '20px', fontSize: '1.1rem' }}>You haven't rated any doctors yet.</p>
                <button onClick={() => window.location.href = '/'} style={{
                  padding: '12px 24px',
                  border: 'none',
                  background: '#667eea',
                  color: 'white',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                  transition: 'background 0.2s'
                }}>
                  Find and Rate Doctors
                </button>
              </div>
            )}
          </div>
        )}

        {activeTab === 'favorites' && (
          <div className="favorites-tab">
            <h3 style={{ color: '#333', marginBottom: '15px', fontSize: '1.3rem' }}>My Favorite Doctors</h3>
            {userData.favoriteDoctors.length > 0 ? (
              <div className="favorites-list" style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '15px'
              }}>
                {userData.favoriteDoctors.map((doctor, index) => (
                  <div key={index} className="favorite-item" style={{
                    padding: '20px',
                    border: '1px solid #e9ecef',
                    borderRadius: '8px',
                    background: '#f8f9fa'
                  }}>
                    <div className="doctor-info" style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      marginBottom: '10px'
                    }}>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                        <span className="doctor-name" style={{ fontWeight: '500', color: '#333' }}>{doctor.name}</span>
                        <span className="specialty" style={{ color: '#667eea', fontWeight: '500' }}>{doctor.specialty}</span>
                        <span className="location" style={{ color: '#666', fontSize: '14px' }}>{doctor.location}</span>
                      </div>
                      <div className="favorite-actions" style={{ display: 'flex', gap: '10px' }}>
                        <button 
                          className="remove-favorite"
                          onClick={() => removeFavorite(doctor.doctorId)}
                          style={{
                            padding: '6px 12px',
                            border: '1px solid #dc3545',
                            background: 'white',
                            color: '#dc3545',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontSize: '12px',
                            transition: 'all 0.2s'
                          }}
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data" style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
                <p style={{ marginBottom: '20px', fontSize: '1.1rem' }}>You haven't added any favorite doctors yet.</p>
                <button onClick={() => window.location.href = '/'} style={{
                  padding: '12px 24px',
                  border: 'none',
                  background: '#667eea',
                  color: 'white',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                  transition: 'background 0.2s'
                }}>
                  Find Doctors to Favorite
                </button>
              </div>
            )}
          </div>
        )}

        {activeTab === 'history' && (
          <div className="history-tab">
            <div className="history-header" style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '20px'
            }}>
              <h3 style={{ color: '#333', marginBottom: '15px', fontSize: '1.3rem' }}>Search History</h3>
              <button className="clear-history" onClick={clearSearchHistory} style={{
                padding: '8px 16px',
                border: '1px solid #dc3545',
                background: 'white',
                color: '#dc3545',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '12px',
                transition: 'all 0.2s'
              }}>
                Clear History
              </button>
            </div>
            {userData.searchHistory.length > 0 ? (
              <div className="history-list" style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '15px'
              }}>
                {userData.searchHistory.map((search, index) => (
                  <div key={index} className="history-item" style={{
                    padding: '20px',
                    border: '1px solid #e9ecef',
                    borderRadius: '8px',
                    background: '#f8f9fa'
                  }}>
                    <div className="search-info" style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      marginBottom: '10px'
                    }}>
                      <span className="symptoms" style={{ fontWeight: '500', color: '#333' }}>
                        {search.symptoms.join(', ')}
                      </span>
                      <span className="specialist" style={{ color: '#667eea', fontWeight: '500' }}>
                        Recommended: {search.specialist}
                      </span>
                    </div>
                    <span className="search-date" style={{ color: '#666', fontSize: '12px' }}>
                      {new Date(search.timestamp).toLocaleDateString()}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data" style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
                <p style={{ marginBottom: '20px', fontSize: '1.1rem' }}>No search history yet.</p>
                <button onClick={() => window.location.href = '/'} style={{
                  padding: '12px 24px',
                  border: 'none',
                  background: '#667eea',
                  color: 'white',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  fontWeight: '500',
                  transition: 'background 0.2s'
                }}>
                  Start Searching
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
