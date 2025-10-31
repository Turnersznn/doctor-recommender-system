import express from 'express';
import { getAllUsers } from '../controllers/userController.js';
import { registerUser, loginUser } from '../controllers/userController.js';
import { getCurrentUser } from '../controllers/userController.js';
import { protect } from '../middleware/auth.js';

const router = express.Router();

router.get('/', getAllUsers);

// POST to register a new user
router.post('/register', registerUser);
router.post('/login', loginUser); 
router.get('/me', protect, getCurrentUser);

export default router; // ✅ Required




