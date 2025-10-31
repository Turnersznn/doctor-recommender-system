import pool from './db.js'; // adjust path if needed

async function seed() {
  try {
    // Clear existing data to avoid duplicates on re-run
    await pool.query('DELETE FROM ratings');
    await pool.query('DELETE FROM users');
    await pool.query('DELETE FROM doctors');

    // Insert sample doctors with Nigerian names and locations
    await pool.query(`
      INSERT INTO doctors (name, specialty, location, experience, availability, rating) VALUES
      ('Dr. Adebayo Ogundimu', 'Cardiology', 'Lagos', 15, 'Mon-Fri 9am-5pm', 4.5),
      ('Dr. Chioma Okwu', 'Dermatology', 'Abuja', 8, 'Tue-Thu 10am-4pm', 4.0),
      ('Dr. Emeka Nwosu', 'Neurology', 'Port Harcourt', 20, 'Mon-Wed 8am-3pm', 4.7),
      ('Dr. Fatima Aliyu', 'Pediatrics', 'Kano', 12, 'Fri-Sun 10am-6pm', 4.3),
      ('Dr. Olumide Adeyemi', 'Orthopedics', 'Ibadan', 10, 'Mon-Fri 9am-5pm', 4.2),
      ('Dr. Ngozi Okafor', 'Pulmonology', 'Enugu', 14, 'Mon-Fri 8am-4pm', 4.6),
      ('Dr. Ibrahim Musa', 'Gastroenterology', 'Kaduna', 18, 'Tue-Sat 9am-5pm', 4.4),
      ('Dr. Blessing Eze', 'Ophthalmology', 'Calabar', 9, 'Mon-Thu 10am-6pm', 4.1),
      ('Dr. Yusuf Abdullahi', 'ENT', 'Jos', 11, 'Wed-Sun 9am-4pm', 4.3),
      ('Dr. Kemi Adesanya', 'Dentistry', 'Abeokuta', 7, 'Mon-Fri 8am-5pm', 4.2)
    `);

    // Insert sample users with Nigerian names
    await pool.query(`
      INSERT INTO users (name, email) VALUES
      ('Tunde Adebayo', 'tunde@example.com'),
      ('Amina Hassan', 'amina@example.com'),
      ('Chidi Okonkwo', 'chidi@example.com')
    `);

    // Insert sample ratings
    await pool.query(`
      INSERT INTO ratings (user_id, doctor_id, rating, review) VALUES
      (1, 1, 5, 'Excellent care and very professional'),
      (2, 3, 4, 'Knowledgeable and friendly'),
      (3, 2, 3, 'Average experience, room for improvement'),
      (1, 4, 4, 'Good with kids, very patient'),
      (2, 5, 5, 'Helped me recover quickly')
    `);

    console.log('Seeding completed successfully!');
    process.exit(0);
  } catch (error) {
    console.error('Error during seeding:', error);
    process.exit(1);
  }
}

seed();
