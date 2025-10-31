import pool from './db.js';

const nigerianDoctors = [
  { name: 'Dr. Adebayo Ogundimu', specialty: 'Cardiology', location: 'Lagos', experience: 15, availability: 'Mon-Fri 9am-5pm', rating: 4.5 },
  { name: 'Dr. Chioma Okwu', specialty: 'Dermatology', location: 'Abuja', experience: 8, availability: 'Tue-Thu 10am-4pm', rating: 4.0 },
  { name: 'Dr. Emeka Nwosu', specialty: 'Neurology', location: 'Port Harcourt', experience: 20, availability: 'Mon-Wed 8am-3pm', rating: 4.7 },
  { name: 'Dr. Fatima Aliyu', specialty: 'Pediatrics', location: 'Kano', experience: 12, availability: 'Fri-Sun 10am-6pm', rating: 4.3 },
  { name: 'Dr. Olumide Adeyemi', specialty: 'Orthopedics', location: 'Ibadan', experience: 10, availability: 'Mon-Fri 9am-5pm', rating: 4.2 },
  { name: 'Dr. Ngozi Okafor', specialty: 'Pulmonology', location: 'Enugu', experience: 14, availability: 'Mon-Fri 8am-4pm', rating: 4.6 },
  { name: 'Dr. Ibrahim Musa', specialty: 'Gastroenterology', location: 'Kaduna', experience: 18, availability: 'Tue-Sat 9am-5pm', rating: 4.4 },
  { name: 'Dr. Blessing Eze', specialty: 'Ophthalmology', location: 'Calabar', experience: 9, availability: 'Mon-Thu 10am-6pm', rating: 4.1 },
  { name: 'Dr. Yusuf Abdullahi', specialty: 'ENT', location: 'Jos', experience: 11, availability: 'Wed-Sun 9am-4pm', rating: 4.3 },
  { name: 'Dr. Kemi Adesanya', specialty: 'Dentistry', location: 'Abeokuta', experience: 7, availability: 'Mon-Fri 8am-5pm', rating: 4.2 }
];

async function addNigerianDoctors() {
  try {
    // Clear existing doctors
    await pool.query('DELETE FROM doctors');
    
    // Insert Nigerian doctors
    for (const doctor of nigerianDoctors) {
      await pool.query(
        'INSERT INTO doctors (name, specialty, location, experience, availability, rating) VALUES (?, ?, ?, ?, ?, ?)',
        [doctor.name, doctor.specialty, doctor.location, doctor.experience, doctor.availability, doctor.rating]
      );
    }
    
    console.log('Nigerian doctors added successfully!');
    process.exit(0);
  } catch (error) {
    console.error('Error adding doctors:', error);
    process.exit(1);
  }
}

addNigerianDoctors();