import express from 'express';
import { updateUserPreferences, getUserPreferences } from '../controllers/userPreferenceController.js';

const router = express.Router();

// Update user preferences based on interactions
router.post('/update', updateUserPreferences);

// Get user preferences
router.get('/:userId', getUserPreferences);

export default router;