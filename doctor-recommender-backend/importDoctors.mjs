// importDoctors.js
import fs from 'fs';
import path from 'path';
import mysql from 'mysql2/promise';
import dotenv from 'dotenv';

dotenv.config();

// Replace with your database credentials
const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'root',
  password: process.env.DB_PASSWORD || '',
  database: process.env.DB_NAME || 'drs-db',
});

const importDoctors = async () => {
  try {
    const dataPath = path.join(__dirname, 'doctors.json');
    const rawData = fs.readFileSync(dataPath, 'utf-8');
    const doctors = JSON.parse(rawData);

    const conn = await pool.getConnection();

    for (const doc of doctors) {
      const { name, specialty, location, experience, email } = doc;

      await conn.execute(
        'INSERT INTO doctors (name, specialty, location, experience, email) VALUES (?, ?, ?, ?, ?)',
        [name, specialty, location, experience, email]
      );
    }

    conn.release();
    console.log('✅ Doctors imported successfully');
  } catch (error) {
    console.error('❌ Error importing doctors:', error);
  } finally {
    pool.end();
  }
};

importDoctors();
