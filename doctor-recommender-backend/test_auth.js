import axios from 'axios';

const BASE_URL = 'http://localhost:5000';

async function testAuth() {
  try {
    console.log('🧪 Testing Authentication System...\n');
    
    // Test 1: Register a new user
    console.log('1. Testing user registration...');
    const registerData = {
      username: 'testuser',
      email: 'test@example.com',
      password: 'password123',
      firstName: 'Test',
      lastName: 'User'
    };
    
    const registerResponse = await axios.post(`${BASE_URL}/api/auth/register`, registerData);
    console.log('✅ Registration successful:', registerResponse.data.message);
    console.log('User ID:', registerResponse.data.user.id);
    console.log('Token:', registerResponse.data.token.substring(0, 20) + '...\n');
    
    // Test 2: Login with the registered user
    console.log('2. Testing user login...');
    const loginData = {
      username: 'testuser',
      password: 'password123'
    };
    
    const loginResponse = await axios.post(`${BASE_URL}/api/auth/login`, loginData);
    console.log('✅ Login successful:', loginResponse.data.message);
    console.log('User:', loginResponse.data.user.username);
    console.log('Token:', loginResponse.data.token.substring(0, 20) + '...\n');
    
    // Test 3: Get user profile (protected route)
    console.log('3. Testing protected route (get profile)...');
    const token = loginResponse.data.token;
    const profileResponse = await axios.get(`${BASE_URL}/api/auth/profile`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    console.log('✅ Profile retrieved successfully');
    console.log('User profile:', profileResponse.data.user);
    console.log('');
    
    // Test 4: Test invalid login
    console.log('4. Testing invalid login...');
    try {
      await axios.post(`${BASE_URL}/api/auth/login`, {
        username: 'testuser',
        password: 'wrongpassword'
      });
    } catch (error) {
      console.log('✅ Invalid login correctly rejected:', error.response.data.error);
    }
    console.log('');
    
    // Test 5: Test duplicate registration
    console.log('5. Testing duplicate registration...');
    try {
      await axios.post(`${BASE_URL}/api/auth/register`, registerData);
    } catch (error) {
      console.log('✅ Duplicate registration correctly rejected:', error.response.data.error);
    }
    console.log('');
    
    console.log('🎉 All authentication tests passed!');
    
  } catch (error) {
    console.error('❌ Authentication test failed:');
    console.error('Error message:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
  }
}

testAuth(); 