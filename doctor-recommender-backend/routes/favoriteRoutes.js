import express from 'express';
import { addToFavorites, removeFromFavorites, getUserFavorites, checkFavorite } from '../controllers/favoriteController.js';

const router = express.Router();

// Add a doctor to favorites
router.post('/add', addToFavorites);

// Remove a doctor from favorites
router.delete('/:doctorId', removeFromFavorites);

// Get user's favorite doctors
router.get('/user-favorites', getUserFavorites);

// Check if a doctor is in user's favorites
router.get('/check/:doctorId', checkFavorite);

export default router;
