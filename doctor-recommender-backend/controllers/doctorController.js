// /controllers/doctorController.js
import pool from '../db.js';

// Get all doctors
export async function getAllDoctors(req, res) {
  try {
    const [rows] = await pool.query('SELECT * FROM doctors');
    res.json(rows);
  } catch (error) {
    console.error('Error fetching doctors:', error);
    res.status(500).json({ message: 'Server error' });
  }
}

// Get similar doctors (content-based filtering)
export async function getSimilarDoctors(req, res) {
  const doctorId = parseInt(req.params.id);
  const topN = 5;

  try {
    // Get target doctor
    const [doctorRows] = await pool.query('SELECT * FROM doctors WHERE id = ?', [doctorId]);
    if (doctorRows.length === 0) {
      return res.status(404).json({ message: 'Doctor not found' });
    }
    const targetDoctor = doctorRows[0];

    // Get all other doctors
    const [allDoctors] = await pool.query('SELECT * FROM doctors WHERE id != ?', [doctorId]);

    // Score similarity
    const scoredDoctors = allDoctors.map(doc => {
      let score = 0;

      // Specialty match (weight 5)
      if (doc.specialty === targetDoctor.specialty) score += 5;

      // Location match (weight 3)
      if (doc.location === targetDoctor.location) {
        score += 3;
      } else if (
        doc.location.toLowerCase().includes(targetDoctor.location.toLowerCase()) ||
        targetDoctor.location.toLowerCase().includes(doc.location.toLowerCase())
      ) {
        score += 1;
      }

      // Experience (weight 2)
      const expDiff = Math.abs(doc.experience - targetDoctor.experience);
      score += Math.max(0, 2 - expDiff * 0.1);

      return { doctor: doc, score };
    });

    // Sort and return top N
    scoredDoctors.sort((a, b) => b.score - a.score);
    const recommendations = scoredDoctors.slice(0, topN).map(d => d.doctor);

    res.json({ recommendations });
  } catch (error) {
    console.error('Error fetching similar doctors:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

export const filterDoctors = async (req, res) => {
  const {
    specialty,
    location,
    availability,
    minRating,
    minExperience,
    maxExperience,
    sortBy = 'rating', // default sort
    order = 'desc',     // default order
    page = 1,
    limit = 5
  } = req.query;

  let query = 'SELECT * FROM doctors WHERE 1=1';
  const params = [];

  if (specialty) {
    query += ' AND specialty = ?';
    params.push(specialty);
  }

  if (location) {
    query += ' AND location = ?';
    params.push(location);
  }

  if (availability) {
    query += ' AND availability LIKE ?';
    params.push(`%${availability}%`);
  }

  if (minRating) {
    query += ' AND rating >= ?';
    params.push(minRating);
  }

  if (minExperience) {
    query += ' AND experience >= ?';
    params.push(minExperience);
  }

  if (maxExperience) {
    query += ' AND experience <= ?';
    params.push(maxExperience);
  }

  // Safe sort options
  const validSortFields = ['rating', 'experience', 'name'];
  const validOrder = order.toUpperCase() === 'ASC' ? 'ASC' : 'DESC';

  if (validSortFields.includes(sortBy)) {
    query += ` ORDER BY ${sortBy} ${validOrder}`;
  }

  // Pagination
  const offset = (page - 1) * limit;
  query += ' LIMIT ? OFFSET ?';
  params.push(parseInt(limit), parseInt(offset));

  try {
    const [doctors] = await pool.query(query, params);
    res.json({
      page: parseInt(page),
      limit: parseInt(limit),
      data: doctors
    });
  } catch (error) {
    console.error('Error filtering doctors:', error);
    res.status(500).json({ message: 'Server error' });
  }
};
