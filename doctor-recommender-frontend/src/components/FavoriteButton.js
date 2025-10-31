import React, { useState, useEffect, useCallback } from 'react';
import './FavoriteButton.css';

const FavoriteButton = ({ doctor }) => {
  const [isFavorite, setIsFavorite] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  
  // Get current user from localStorage (user must be logged in to use this feature)
  const userData = localStorage.getItem('user');
  const user = userData ? JSON.parse(userData) : null;
  const defaultUserName = user?.username || 'User';

  const checkFavoriteStatus = useCallback(async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/favorites/check/${doctor.doctorId}?userName=${defaultUserName}`);
      const data = await response.json();
      setIsFavorite(data.isFavorite);
    } catch (error) {
      console.error('Error checking favorite status:', error);
    }
  }, [doctor.doctorId, defaultUserName]);

  // Check if doctor is in favorites on component mount
  useEffect(() => {
    checkFavoriteStatus();
  }, [checkFavoriteStatus]);

  const toggleFavorite = async () => {
    setIsLoading(true);
    try {
      if (isFavorite) {
        // Remove from favorites
        await fetch(`http://localhost:5000/api/favorites/${doctor.doctorId}?userName=${defaultUserName}`, {
          method: 'DELETE'
        });
        setIsFavorite(false);
      } else {
        // Add to favorites
        await fetch('http://localhost:5000/api/favorites/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            doctorId: doctor.doctorId,
            doctorName: doctor.name,
            specialty: doctor.specialty,
            location: doctor.location,
            userName: defaultUserName
          }),
        });
        setIsFavorite(true);
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
      alert('Failed to update favorites. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      className={`favorite-button ${isFavorite ? 'favorited' : ''}`}
      onClick={toggleFavorite}
      disabled={isLoading}
      title={isFavorite ? 'Remove from favorites' : 'Add to favorites'}
    >
      {isLoading ? '...' : (isFavorite ? '❤️' : '🤍')}
    </button>
  );
};

export default FavoriteButton; 