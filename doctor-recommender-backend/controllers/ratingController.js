import fs from 'fs';
import path from 'path';

const RATINGS_FILE = path.join(process.cwd(), 'data', 'ratings.json');

// Load ratings data
function loadRatings() {
  try {
    const data = fs.readFileSync(RATINGS_FILE, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    // If file doesn't exist, return default structure
    return {
      "ratings": {},
      "reviews": {},
      "statistics": {}
    };
  }
}

// Save ratings data
function saveRatings(data) {
  fs.writeFileSync(RATINGS_FILE, JSON.stringify(data, null, 2));
}

// Get doctor identifier (using NPI number or name + location)
function getDoctorId(doctor) {
  return doctor.npi || `${doctor.name}-${doctor.location}`.replace(/\s+/g, '-');
}

// Submit a rating for a doctor
export const submitRating = async (req, res) => {
  try {
    const { doctorId, rating, review, userName } = req.body;
    
    if (!doctorId || !rating || rating < 1 || rating > 5) {
      return res.status(400).json({ 
        error: 'Valid doctorId and rating (1-5) are required' 
      });
    }

    const ratingsData = loadRatings();
    
    // Initialize doctor ratings if not exists
    if (!ratingsData.ratings[doctorId]) {
      ratingsData.ratings[doctorId] = [];
    }
    
    if (!ratingsData.reviews[doctorId]) {
      ratingsData.reviews[doctorId] = [];
    }

    // Check if user has already rated this doctor
    const existingRatingIndex = ratingsData.ratings[doctorId].findIndex(
      r => r.userName === userName
    );

    const newRating = {
      rating: parseInt(rating),
      review: review || '',
      userName: userName || 'Anonymous',
      timestamp: new Date().toISOString()
    };

    let message = 'Rating submitted successfully';
    
    if (existingRatingIndex !== -1) {
      // Update existing rating
      ratingsData.ratings[doctorId][existingRatingIndex] = newRating;
      message = 'Rating updated successfully';
      
      // Update review if it exists
      const existingReviewIndex = ratingsData.reviews[doctorId].findIndex(
        r => r.userName === userName
      );
      if (existingReviewIndex !== -1) {
        ratingsData.reviews[doctorId][existingReviewIndex] = newRating;
      } else if (review) {
        ratingsData.reviews[doctorId].push(newRating);
      }
    } else {
      // Add new rating
      ratingsData.ratings[doctorId].push(newRating);
      
      if (review) {
        ratingsData.reviews[doctorId].push(newRating);
      }
    }

    // Update statistics
    const doctorRatings = ratingsData.ratings[doctorId];
    const avgRating = doctorRatings.reduce((sum, r) => sum + r.rating, 0) / doctorRatings.length;
    
    ratingsData.statistics[doctorId] = {
      averageRating: Math.round(avgRating * 10) / 10,
      totalRatings: doctorRatings.length,
      totalReviews: ratingsData.reviews[doctorId].length
    };

    saveRatings(ratingsData);

    res.json({
      success: true,
      message: message,
      statistics: ratingsData.statistics[doctorId],
      isUpdate: existingRatingIndex !== -1
    });

  } catch (error) {
    console.error('Error submitting rating:', error);
    res.status(500).json({ error: 'Failed to submit rating' });
  }
};

// Get ratings for a doctor
export const getDoctorRatings = async (req, res) => {
  try {
    const { doctorId } = req.params;
    const { userName } = req.query; // Optional: to get user's specific rating
    
    if (!doctorId) {
      return res.status(400).json({ error: 'Doctor ID is required' });
    }

    const ratingsData = loadRatings();
    const doctorRatings = ratingsData.ratings[doctorId] || [];
    const doctorReviews = ratingsData.reviews[doctorId] || [];
    
    // If there are no ratings, use default 5-star rating
    if (doctorRatings.length === 0) {
      const defaultStatistics = {
        averageRating: 5,
        totalRatings: 0,
        totalReviews: 0
      };
      
      res.json({
        ratings: doctorRatings,
        reviews: doctorReviews,
        statistics: defaultStatistics,
        userRating: null
      });
      return;
    }
    
    // Use existing statistics if there are ratings
    const statistics = ratingsData.statistics[doctorId] || {
      averageRating: 5,
      totalRatings: 0,
      totalReviews: 0
    };

    // Get user's specific rating if userName is provided
    let userRating = null;
    if (userName) {
      userRating = doctorRatings.find(r => r.userName === userName) || null;
    }

    res.json({
      ratings: doctorRatings,
      reviews: doctorReviews,
      statistics,
      userRating
    });

  } catch (error) {
    console.error('Error getting doctor ratings:', error);
    res.status(500).json({ error: 'Failed to get doctor ratings' });
  }
};

// Get user's rating history
export const getUserRatingHistory = async (req, res) => {
  try {
    const { userName } = req.query;
    const ratingsData = loadRatings();
    
    let userRatings = [];
    let totalRating = 0;
    let ratingCount = 0;
    const specialtyCounts = {};

    // Search through all ratings to find user's ratings
    for (const [doctorId, ratings] of Object.entries(ratingsData.ratings)) {
      for (const rating of ratings) {
        if (rating.userName === userName) {
          userRatings.push({
            doctorId,
            doctorName: doctorId.replace(/-/g, ' '), // Simple conversion
            rating: rating.rating,
            review: rating.review,
            timestamp: rating.timestamp,
            specialty: 'General' // This would need to be enhanced with actual doctor data
          });
          
          totalRating += rating.rating;
          ratingCount++;
          
          // Count specialties (simplified)
          const specialty = 'General';
          specialtyCounts[specialty] = (specialtyCounts[specialty] || 0) + 1;
        }
      }
    }

    // Calculate statistics
    const averageRating = ratingCount > 0 ? totalRating / ratingCount : 0;
    const mostRatedSpecialty = Object.keys(specialtyCounts).length > 0 
      ? Object.entries(specialtyCounts).sort((a, b) => b[1] - a[1])[0][0]
      : 'None';

    res.json({
      ratings: userRatings,
      averageRating: Math.round(averageRating * 10) / 10,
      totalRatings: ratingCount,
      mostRatedSpecialty
    });

  } catch (error) {
    console.error('Error getting user rating history:', error);
    res.status(500).json({ error: 'Failed to get user rating history' });
  }
};

// Get top rated doctors by specialty
export const getTopRatedDoctors = async (req, res) => {
  try {
    const { specialty, limit = 10 } = req.query;
    
    const ratingsData = loadRatings();
    const statistics = ratingsData.statistics;
    
    // Filter by specialty if provided
    let topDoctors = Object.entries(statistics)
      .filter(([doctorId, stats]) => {
        if (!specialty) return true;
        // This would need to be enhanced to match doctor specialties
        return true; // For now, return all
      })
      .sort((a, b) => b[1].averageRating - a[1].averageRating)
      .slice(0, parseInt(limit))
      .map(([doctorId, stats]) => ({
        doctorId,
        ...stats
      }));

    res.json({ topDoctors });

  } catch (error) {
    console.error('Error getting top rated doctors:', error);
    res.status(500).json({ error: 'Failed to get top rated doctors' });
  }
};
