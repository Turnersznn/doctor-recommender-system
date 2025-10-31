import express from 'express';
import { submitRating, getDoctorRatings, getTopRatedDoctors, getUserRatingHistory } from '../controllers/ratingController.js';

const router = express.Router();

// Submit a rating for a doctor
router.post('/submit', submitRating);

// Get ratings for a specific doctor
router.get('/doctor/:doctorId', getDoctorRatings);

// Get user's rating history
router.get('/user-history', getUserRatingHistory);

// Get top rated doctors
router.get('/top-rated', getTopRatedDoctors);

export default router;
