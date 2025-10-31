import express from 'express';
import { predictSpecialist } from '../controllers/specialistController.js';
import { enhancedPredictSpecialist } from '../controllers/enhancedSpecialistController.js';

const router = express.Router();
router.post('/predict', predictSpecialist);
router.post('/enhanced-predict', enhancedPredictSpecialist);
 
export default router; 