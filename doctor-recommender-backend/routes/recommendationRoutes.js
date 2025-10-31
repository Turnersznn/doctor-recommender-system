import express from 'express';
import { recommendDoctors } from '../controllers/recommendationController.js';

const router = express.Router();
router.get('/:userId', recommendDoctors); // e.g., /api/recommendations/3

export default router;
