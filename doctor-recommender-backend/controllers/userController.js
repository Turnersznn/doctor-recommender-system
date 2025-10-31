import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import pool from '../db.js'; // adjust path to your DB file

// Utility to generate JWT
const generateToken = (userId) => {
  return jwt.sign({ id: userId }, process.env.JWT_SECRET, { expiresIn: '1d' });
};

// GET all users (optional)
export const getAllUsers = async (req, res) => {
  try {
    const [rows] = await pool.query('SELECT * FROM users');
    res.json(rows);
  } catch (error) {
    console.error('Error fetching users:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// REGISTER user
export const registerUser = async (req, res) => {
  try {
    const { name, email, location, password } = req.body;

    if (!name || !email || !location || !password) {
      return res.status(400).json({ message: 'All fields are required' });
    }

    // Check if user already exists
    const [existing] = await pool.query('SELECT id FROM users WHERE email = ?', [email]);
    if (existing.length > 0) {
      return res.status(400).json({ message: 'User with this email already exists' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Save user
    const [result] = await pool.query(
      'INSERT INTO users (name, email, location, password) VALUES (?, ?, ?, ?)',
      [name, email, location, hashedPassword]
    );

    // Return success
    res.status(201).json({ message: 'User registered successfully', userId: result.insertId });

  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

// LOGIN user
export const loginUser = async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ message: 'Email and password are required' });
    }

    // Fetch user
    const [rows] = await pool.query('SELECT * FROM users WHERE email = ?', [email]);
    if (rows.length === 0) {
      return res.status(400).json({ message: 'Invalid email or password' });
    }

    const user = rows[0];

    // Check password
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(400).json({ message: 'Invalid email or password' });
    }

    // Generate token
    const token = generateToken(user.id);

    // Return user data + token
    res.status(200).json({
      id: user.id,
      name: user.name,
      email: user.email,
      location: user.location,
      token,
    });

  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};

export const getCurrentUser = async (req, res) => {
  try {
    const [users] = await pool.query('SELECT id, name, email, location FROM users WHERE id = ?', [req.user.id]);

    if (users.length === 0) {
      return res.status(404).json({ message: 'User not found' });
    }

    res.json(users[0]);
  } catch (error) {
    console.error('Fetch user error:', error);
    res.status(500).json({ message: 'Server error' });
  }
};
