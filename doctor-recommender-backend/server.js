import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import doctorRoutes from './routes/doctorRoutes.js';
import userRoutes from './routes/userRoutes.js';
import ratingRoutes from './routes/ratingRoutes.js';
import reviewRoutes from './routes/reviewRoutes.js';
import recommendationRoutes from './routes/recommendationRoutes.js';
import favoriteRoutes from './routes/favoriteRoutes.js';
import specialistRoutes from './routes/specialistRoutes.js';
import authRoutes from './routes/authRoutes.js';
import userPreferenceRoutes from './routes/userPreferenceRoutes.js';

dotenv.config();
const app = express();

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }))

// Test route to verify server is working
app.get('/test', (req, res) => {
  res.json({ message: 'Server is working!' });
});

// Routes
app.use('/api/doctors', doctorRoutes);
app.use('/api/users', userRoutes);
app.use('/api/ratings', ratingRoutes);
app.use('/api/reviews', reviewRoutes);
app.use('/api/recommendations', recommendationRoutes);
app.use('/api/favorites', favoriteRoutes);
app.use('/api/specialist', specialistRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/preferences', userPreferenceRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
