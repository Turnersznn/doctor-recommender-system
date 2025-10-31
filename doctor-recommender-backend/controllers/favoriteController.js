import fs from 'fs';
import path from 'path';

const FAVORITES_FILE = path.join(process.cwd(), 'data', 'favorites.json');

// Load favorites data
function loadFavorites() {
  try {
    const data = fs.readFileSync(FAVORITES_FILE, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    // If file doesn't exist, return default structure
    return {
      "favorites": {}
    };
  }
}

// Save favorites data
function saveFavorites(data) {
  fs.writeFileSync(FAVORITES_FILE, JSON.stringify(data, null, 2));
}

// Add a doctor to favorites
export const addToFavorites = async (req, res) => {
  try {
    const { doctorId, doctorName, specialty, location, userName } = req.body;
    
    if (!doctorId || !userName) {
      return res.status(400).json({ 
        error: 'Doctor ID and user name are required' 
      });
    }

    const favoritesData = loadFavorites();
    
    // Initialize user favorites if not exists
    if (!favoritesData.favorites[userName]) {
      favoritesData.favorites[userName] = [];
    }

    // Check if doctor is already in favorites
    const existingIndex = favoritesData.favorites[userName].findIndex(
      fav => fav.doctorId === doctorId
    );

    if (existingIndex !== -1) {
      return res.status(400).json({ 
        error: 'Doctor is already in your favorites' 
      });
    }

    // Add to favorites
    const favoriteDoctor = {
      doctorId,
      doctorName: doctorName || doctorId.replace(/-/g, ' '),
      specialty: specialty || 'General',
      location: location || 'Unknown',
      addedAt: new Date().toISOString()
    };

    favoritesData.favorites[userName].push(favoriteDoctor);
    saveFavorites(favoritesData);

    res.json({
      success: true,
      message: 'Doctor added to favorites',
      favorite: favoriteDoctor
    });

  } catch (error) {
    console.error('Error adding to favorites:', error);
    res.status(500).json({ error: 'Failed to add to favorites' });
  }
};

// Remove a doctor from favorites
export const removeFromFavorites = async (req, res) => {
  try {
    const { doctorId } = req.params;
    const { userName } = req.query;
    
    if (!doctorId || !userName) {
      return res.status(400).json({ 
        error: 'Doctor ID and user name are required' 
      });
    }

    const favoritesData = loadFavorites();
    
    if (!favoritesData.favorites[userName]) {
      return res.status(404).json({ 
        error: 'No favorites found for this user' 
      });
    }

    // Remove from favorites
    const updatedFavorites = favoritesData.favorites[userName].filter(
      fav => fav.doctorId !== doctorId
    );

    if (updatedFavorites.length === favoritesData.favorites[userName].length) {
      return res.status(404).json({ 
        error: 'Doctor not found in favorites' 
      });
    }

    favoritesData.favorites[userName] = updatedFavorites;
    saveFavorites(favoritesData);

    res.json({
      success: true,
      message: 'Doctor removed from favorites'
    });

  } catch (error) {
    console.error('Error removing from favorites:', error);
    res.status(500).json({ error: 'Failed to remove from favorites' });
  }
};

// Get user's favorite doctors
export const getUserFavorites = async (req, res) => {
  try {
    const { userName } = req.query;
    
    if (!userName) {
      return res.status(400).json({ 
        error: 'User name is required' 
      });
    }

    const favoritesData = loadFavorites();
    const userFavorites = favoritesData.favorites[userName] || [];

    res.json({
      favorites: userFavorites,
      totalFavorites: userFavorites.length
    });

  } catch (error) {
    console.error('Error getting user favorites:', error);
    res.status(500).json({ error: 'Failed to get user favorites' });
  }
};

// Check if a doctor is in user's favorites
export const checkFavorite = async (req, res) => {
  try {
    const { doctorId } = req.params;
    const { userName } = req.query;
    
    if (!doctorId || !userName) {
      return res.status(400).json({ 
        error: 'Doctor ID and user name are required' 
      });
    }

    const favoritesData = loadFavorites();
    const userFavorites = favoritesData.favorites[userName] || [];
    
    const isFavorite = userFavorites.some(fav => fav.doctorId === doctorId);

    res.json({
      isFavorite,
      doctorId
    });

  } catch (error) {
    console.error('Error checking favorite status:', error);
    res.status(500).json({ error: 'Failed to check favorite status' });
  }
};
