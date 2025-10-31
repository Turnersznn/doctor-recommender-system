import React, { useState } from 'react';
import './DoctorRating.css';

const DoctorRating = ({ doctor, onRatingSubmit }) => {
  const [showRatingForm, setShowRatingForm] = useState(false);
  const [rating, setRating] = useState(5);
  const [review, setReview] = useState('');
  const [userName, setUserName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [userRating, setUserRating] = useState(null);
  const [hasRated, setHasRated] = useState(false);

  // Safety check for doctor object
  if (!doctor) {
    return <div className="doctor-rating">No doctor data available</div>;
  }
  
  // Get current user from localStorage (user must be logged in to use this feature)
  const userData = localStorage.getItem('user');
  const user = userData ? JSON.parse(userData) : null;
  const defaultUserName = user?.username || 'User';

  const handleSubmitRating = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const response = await fetch('http://localhost:5000/api/ratings/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          doctorId: doctor.doctorId,
          rating: rating,
          review: review,
          userName: userName || defaultUserName
        }),
      });

      const data = await response.json();
      
      if (data.success) {
        setShowRatingForm(false);
        setHasRated(true);
        setUserRating({ rating, review, userName: userName || 'Anonymous' });
        
        // Notify parent component to refresh ratings
        if (onRatingSubmit) {
          onRatingSubmit(doctor.doctorId, data.statistics);
        }
        
        // Show appropriate message
        alert(data.isUpdate ? 'Rating updated successfully!' : 'Rating submitted successfully!');
      } else {
        alert('Failed to submit rating. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting rating:', error);
      alert('Failed to submit rating. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const renderStars = (rating) => {
    return (
      <div className="stars">
        {[1, 2, 3, 4, 5].map((star) => (
          <span
            key={star}
            className={`star ${star <= rating ? 'filled' : ''}`}
            onClick={() => setRating(star)}
          >
            ★
          </span>
        ))}
      </div>
    );
  };

  // Check if user has already rated this doctor
  const checkUserRating = async (userName) => {
    if (!userName) return;
    
    try {
      const response = await fetch(`http://localhost:5000/api/ratings/doctor/${doctor.doctorId}?userName=${userName}`);
      const data = await response.json();
      
      if (data.userRating) {
        setUserRating(data.userRating);
        setHasRated(true);
        setRating(data.userRating.rating);
        setReview(data.userRating.review);
        setUserName(data.userRating.userName);
      }
    } catch (error) {
      console.error('Error checking user rating:', error);
    }
  };

  const renderDisplayStars = (rating) => {
    return (
      <div className="stars display">
        {[1, 2, 3, 4, 5].map((star) => (
          <span
            key={star}
            className={`star ${star <= rating ? 'filled' : ''}`}
          >
            ★
          </span>
        ))}
      </div>
    );
  };

  return (
    <div className="doctor-rating">
      <div className="rating-display">
        {doctor.rating && doctor.rating > 0 ? (
          <div className="rating-info">
            {renderDisplayStars(doctor.rating)}
            <span className="rating-text">
              {Number(doctor.rating).toFixed(1)} ({doctor.totalRatings || 0} ratings)
            </span>
          </div>
        ) : (
          <span className="no-rating">No ratings yet</span>
        )}
        
        <button 
          className="rate-button"
          onClick={() => {
            if (!showRatingForm) {
              // When opening form, check for existing user rating
              if (userName) {
                checkUserRating(userName);
              }
            }
            setShowRatingForm(!showRatingForm);
          }}
        >
          {showRatingForm ? 'Cancel' : hasRated ? 'Update Rating' : 'Rate this doctor'}
        </button>
      </div>

      {showRatingForm && (
        <form className="rating-form" onSubmit={handleSubmitRating}>
          {hasRated && userRating && (
            <div className="existing-rating">
              <p>Your current rating: {renderDisplayStars(userRating.rating)}</p>
              {userRating.review && <p>Your review: "{userRating.review}"</p>}
            </div>
          )}
          
          <div className="form-group">
            <label>Your Rating:</label>
            {renderStars(rating)}
          </div>
          
          <div className="form-group">
            <label htmlFor="userName">Your Name (optional):</label>
            <input
              type="text"
              id="userName"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              placeholder="Anonymous"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="review">Review (optional):</label>
            <textarea
              id="review"
              value={review}
              onChange={(e) => setReview(e.target.value)}
              placeholder="Share your experience with this doctor..."
              rows="3"
            />
          </div>
          
          <button 
            type="submit" 
            className="submit-rating"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Submitting...' : hasRated ? 'Update Rating' : 'Submit Rating'}
          </button>
        </form>
      )}
    </div>
  );
};

export default DoctorRating; 