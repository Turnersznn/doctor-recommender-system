import { ContentBasedRecommender } from '../contentBasedRecommender.js';

const contentRecommender = new ContentBasedRecommender();

// Update user preferences based on doctor rating
export const updateUserPreferences = async (req, res) => {
  try {
    const { userId, doctorId, rating, specialty, doctorFeatures } = req.body;
    
    if (!userId || !doctorId || !rating || !specialty) {
      return res.status(400).json({ 
        error: 'userId, doctorId, rating, and specialty are required' 
      });
    }
    
    // Update user profile with new preference data
    contentRecommender.updateUserProfile(userId, doctorId, rating, specialty, doctorFeatures);
    
    res.json({ 
      message: 'User preferences updated successfully',
      userId: userId
    });
    
  } catch (error) {
    console.error('Error updating user preferences:', error);
    res.status(500).json({ error: 'Failed to update user preferences' });
  }
};

// Get user preferences
export const getUserPreferences = async (req, res) => {
  try {
    const { userId } = req.params;
    
    if (!userId) {
      return res.status(400).json({ error: 'userId is required' });
    }
    
    const userProfile = contentRecommender.getUserProfile(userId);
    
    res.json({
      userId: userId,
      preferences: userProfile.preferences
    });
    
  } catch (error) {
    console.error('Error getting user preferences:', error);
    res.status(500).json({ error: 'Failed to get user preferences' });
  }
};