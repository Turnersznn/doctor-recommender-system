import pool from '../db.js';

export const recommendDoctors = async (req, res) => {
  const { userId } = req.params;

  try {
    // Get reviews made by user
    const [userReviews] = await pool.query(
      'SELECT d.specialty, d.location FROM reviews r JOIN doctors d ON r.doctor_id = d.id WHERE r.user_id = ?',
      [userId]
    );

    if (userReviews.length === 0) {
      // If no reviews yet, return top-rated doctors
      const [topDoctors] = await pool.query(
        'SELECT * FROM doctors ORDER BY rating DESC LIMIT 5'
      );
      return res.json(topDoctors);
    }

    // Find the most reviewed specialty and location
    const specialties = userReviews.map(r => r.specialty);
    const locations = userReviews.map(r => r.location);

    const favoriteSpecialty = specialties.sort((a, b) =>
      specialties.filter(v => v === a).length - specialties.filter(v => v === b).length
    ).pop();

    const favoriteLocation = locations.sort((a, b) =>
      locations.filter(v => v === a).length - locations.filter(v => v === b).length
    ).pop();

    // Recommend doctors matching favorite specialty & location
    const [recommended] = await pool.query(
      'SELECT * FROM doctors WHERE specialty = ? AND location = ? ORDER BY rating DESC LIMIT 5',
      [favoriteSpecialty, favoriteLocation]
    );

    res.json(recommended);
  } catch (error) {
    console.error('Recommendation error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};
