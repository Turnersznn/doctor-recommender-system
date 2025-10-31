import express from 'express';
import { addReview, getDoctorReviews } from '../controllers/reviewController.js';

const router = express.Router();

router.post('/', addReview); // POST /api/reviews
router.get('/:doctorId', getDoctorReviews); // GET /api/reviews/:doctorId

export default router;
