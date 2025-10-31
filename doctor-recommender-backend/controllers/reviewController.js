import pool from '../db.js';

export const addReview = async (req, res) => {
  const { doctor_id, user_id, rating, comment } = req.body;

  if (!doctor_id || !user_id || !rating) {
    return res.status(400).json({ message: 'Doctor, user, and rating are required' });
  }

  try {
    await pool.query(
      'INSERT INTO reviews (doctor_id, user_id, rating, comment) VALUES (?, ?, ?, ?)',
      [doctor_id, user_id, rating, comment || null]
    );
    res.status(201).json({ message: 'Review added successfully' });
  } catch (error) {
    console.error('Error adding review:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

export const getDoctorReviews = async (req, res) => {
  const { doctorId } = req.params;

  try {
    const [reviews] = await pool.query(
      'SELECT r.*, u.name AS reviewer FROM reviews r JOIN users u ON r.user_id = u.id WHERE r.doctor_id = ?',
      [doctorId]
    );
    res.json(reviews);
  } catch (error) {
    console.error('Error fetching reviews:', error);
    res.status(500).json({ message: 'Server error' });
  }
};
