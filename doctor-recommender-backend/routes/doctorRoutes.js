// /routes/doctorRoutes.js
import express from 'express';
import { getAllDoctors, getSimilarDoctors, filterDoctors } from '../controllers/doctorController.js';

const router = express.Router();

router.get('/', getAllDoctors); // /api/doctors
router.get('/:id/similar', getSimilarDoctors); // /api/doctors/:id/similar
router.get('/filter', filterDoctors);


export default router;
