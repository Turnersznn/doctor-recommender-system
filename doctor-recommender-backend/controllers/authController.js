import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import fs from 'fs';
import path from 'path';

const USERS_FILE = path.join(process.cwd(), 'data', 'users.json');
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-in-production';

// Load users data
function loadUsers() {
  try {
    const data = fs.readFileSync(USERS_FILE, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    // If file doesn't exist, return default structure
    return {
      users: []
    };
  }
}

// Save users data
function saveUsers(data) {
  fs.writeFileSync(USERS_FILE, JSON.stringify(data, null, 2));
}

// Generate JWT token
function generateToken(userId) {
  return jwt.sign({ userId }, JWT_SECRET, { expiresIn: '7d' });
}

// Register new user
export const register = async (req, res) => {
  try {
    const { username, email, password, firstName, lastName } = req.body;

    // Validate input
    if (!username || !email || !password || !firstName || !lastName) {
      return res.status(400).json({
        error: 'All fields are required'
      });
    }

    if (password.length < 6) {
      return res.status(400).json({
        error: 'Password must be at least 6 characters long'
      });
    }

    const usersData = loadUsers();

    // Check if username already exists
    const existingUser = usersData.users.find(user => 
      user.username === username || user.email === email
    );

    if (existingUser) {
      return res.status(400).json({
        error: 'Username or email already exists'
      });
    }

    // Hash password
    const saltRounds = 10;
    const hashedPassword = await bcrypt.hash(password, saltRounds);

    // Create new user
    const newUser = {
      id: Date.now().toString(),
      username,
      email,
      password: hashedPassword,
      firstName,
      lastName,
      createdAt: new Date().toISOString(),
      lastLogin: null
    };

    usersData.users.push(newUser);
    saveUsers(usersData);

    // Generate token
    const token = generateToken(newUser.id);

    // Return user data (without password)
    const { password: _, ...userWithoutPassword } = newUser;

    res.status(201).json({
      success: true,
      message: 'User registered successfully',
      user: userWithoutPassword,
      token
    });

  } catch (error) {
    console.error('Error registering user:', error);
    res.status(500).json({ error: 'Failed to register user' });
  }
};

// Login user
export const login = async (req, res) => {
  try {
    const { username, password } = req.body;

    // Validate input
    if (!username || !password) {
      return res.status(400).json({
        error: 'Username and password are required'
      });
    }

    const usersData = loadUsers();

    // Find user by username or email
    const user = usersData.users.find(user => 
      user.username === username || user.email === username
    );

    if (!user) {
      return res.status(401).json({
        error: 'Invalid credentials'
      });
    }

    // Check password
    const isPasswordValid = await bcrypt.compare(password, user.password);

    if (!isPasswordValid) {
      return res.status(401).json({
        error: 'Invalid credentials'
      });
    }

    // Update last login
    user.lastLogin = new Date().toISOString();
    saveUsers(usersData);

    // Generate token
    const token = generateToken(user.id);

    // Return user data (without password)
    const { password: _, ...userWithoutPassword } = user;

    res.json({
      success: true,
      message: 'Login successful',
      user: userWithoutPassword,
      token
    });

  } catch (error) {
    console.error('Error logging in:', error);
    res.status(500).json({ error: 'Failed to login' });
  }
};

// Get current user profile
export const getProfile = async (req, res) => {
  try {
    const userId = req.user.userId;
    const usersData = loadUsers();

    const user = usersData.users.find(user => user.id === userId);

    if (!user) {
      return res.status(404).json({
        error: 'User not found'
      });
    }

    // Return user data (without password)
    const { password: _, ...userWithoutPassword } = user;

    res.json({
      success: true,
      user: userWithoutPassword
    });

  } catch (error) {
    console.error('Error getting profile:', error);
    res.status(500).json({ error: 'Failed to get profile' });
  }
};

// Update user profile
export const updateProfile = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { firstName, lastName, email } = req.body;

    const usersData = loadUsers();
    const userIndex = usersData.users.findIndex(user => user.id === userId);

    if (userIndex === -1) {
      return res.status(404).json({
        error: 'User not found'
      });
    }

    // Update user data
    if (firstName) usersData.users[userIndex].firstName = firstName;
    if (lastName) usersData.users[userIndex].lastName = lastName;
    if (email) usersData.users[userIndex].email = email;

    saveUsers(usersData);

    // Return updated user data (without password)
    const { password: _, ...userWithoutPassword } = usersData.users[userIndex];

    res.json({
      success: true,
      message: 'Profile updated successfully',
      user: userWithoutPassword
    });

  } catch (error) {
    console.error('Error updating profile:', error);
    res.status(500).json({ error: 'Failed to update profile' });
  }
};

// Change password
export const changePassword = async (req, res) => {
  try {
    const userId = req.user.userId;
    const { currentPassword, newPassword } = req.body;

    if (!currentPassword || !newPassword) {
      return res.status(400).json({
        error: 'Current password and new password are required'
      });
    }

    if (newPassword.length < 6) {
      return res.status(400).json({
        error: 'New password must be at least 6 characters long'
      });
    }

    const usersData = loadUsers();
    const userIndex = usersData.users.findIndex(user => user.id === userId);

    if (userIndex === -1) {
      return res.status(404).json({
        error: 'User not found'
      });
    }

    // Verify current password
    const isCurrentPasswordValid = await bcrypt.compare(
      currentPassword, 
      usersData.users[userIndex].password
    );

    if (!isCurrentPasswordValid) {
      return res.status(401).json({
        error: 'Current password is incorrect'
      });
    }

    // Hash new password
    const saltRounds = 10;
    const hashedNewPassword = await bcrypt.hash(newPassword, saltRounds);

    // Update password
    usersData.users[userIndex].password = hashedNewPassword;
    saveUsers(usersData);

    res.json({
      success: true,
      message: 'Password changed successfully'
    });

  } catch (error) {
    console.error('Error changing password:', error);
    res.status(500).json({ error: 'Failed to change password' });
  }
};

// Verify token middleware
export const verifyToken = (req, res, next) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];

    if (!token) {
      return res.status(401).json({
        error: 'Access token required'
      });
    }

    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded;
    next();

  } catch (error) {
    console.error('Token verification error:', error);
    res.status(401).json({
      error: 'Invalid or expired token'
    });
  }
}; 