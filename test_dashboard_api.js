#!/usr/bin/env node
/**
 * Test Dashboard API Endpoints
 */

const axios = require('axios');

const BASE_URL = 'http://localhost:5000';
const TEST_USER = 'testuser';

async function testDashboardAPIs() {
    console.log('🔍 Testing Dashboard API Endpoints');
    console.log('=' * 50);
    
    try {
        // Test server status
        console.log('\n1. Testing server status...');
        const serverResponse = await axios.get(`${BASE_URL}/test`);
        console.log('✅ Server is running:', serverResponse.data.message);
        
        // Test ratings endpoint
        console.log('\n2. Testing ratings endpoint...');
        try {
            const ratingsResponse = await axios.get(`${BASE_URL}/api/ratings/user-history?userName=${TEST_USER}`);
            console.log('✅ Ratings endpoint working:', ratingsResponse.status);
            console.log('   Response:', ratingsResponse.data);
        } catch (error) {
            console.log('❌ Ratings endpoint error:', error.response?.status, error.response?.data || error.message);
        }
        
        // Test favorites endpoint
        console.log('\n3. Testing favorites endpoint...');
        try {
            const favoritesResponse = await axios.get(`${BASE_URL}/api/favorites/user-favorites?userName=${TEST_USER}`);
            console.log('✅ Favorites endpoint working:', favoritesResponse.status);
            console.log('   Response:', favoritesResponse.data);
        } catch (error) {
            console.log('❌ Favorites endpoint error:', error.response?.status, error.response?.data || error.message);
        }
        
        // Test if user exists
        console.log('\n4. Testing user data...');
        try {
            const userResponse = await axios.get(`${BASE_URL}/api/users`);
            console.log('✅ Users endpoint working:', userResponse.status);
            console.log('   Number of users:', userResponse.data?.length || 'Unknown');
        } catch (error) {
            console.log('❌ Users endpoint error:', error.response?.status, error.response?.data || error.message);
        }
        
    } catch (error) {
        console.log('❌ Server connection error:', error.message);
        console.log('Make sure the backend server is running on port 5000');
        console.log('Run: cd doctor-recommender-backend && npm start');
    }
    
    console.log('\n' + '=' * 50);
    console.log('Dashboard API test complete!');
}

// Run the test
testDashboardAPIs().catch(console.error);
