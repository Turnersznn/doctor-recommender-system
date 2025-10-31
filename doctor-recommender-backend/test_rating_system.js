const axios = require('axios');

const BASE_URL = 'http://localhost:5000/api';

async function testRatingSystem() {
  console.log('🧪 Testing Rating System...\n');

  try {
    // Test 1: Submit a rating
    console.log('1. Testing rating submission...');
    const ratingData = {
      doctorId: 'dr_smith_cardiology',
      rating: 5,
      review: 'Excellent doctor! Very knowledgeable and caring.',
      userName: 'John Doe'
    };

    const submitResponse = await axios.post(`${BASE_URL}/ratings/submit`, ratingData);
    console.log('✅ Rating submitted successfully:', submitResponse.data);

    // Test 2: Get doctor ratings
    console.log('\n2. Testing get doctor ratings...');
    const ratingsResponse = await axios.get(`${BASE_URL}/ratings/doctor/dr_smith_cardiology`);
    console.log('✅ Doctor ratings retrieved:', ratingsResponse.data);

    // Test 3: Get top rated doctors
    console.log('\n3. Testing get top rated doctors...');
    const topRatedResponse = await axios.get(`${BASE_URL}/ratings/top-rated`);
    console.log('✅ Top rated doctors retrieved:', topRatedResponse.data);

    // Test 4: Get user rating history
    console.log('\n4. Testing get user rating history...');
    const userHistoryResponse = await axios.get(`${BASE_URL}/ratings/user-history?userName=John Doe`);
    console.log('✅ User rating history retrieved:', userHistoryResponse.data);

    console.log('\n🎉 All rating system tests passed!');

  } catch (error) {
    console.error('❌ Error testing rating system:', error.response?.data || error.message);
  }
}

async function testFavoriteSystem() {
  console.log('\n🧪 Testing Favorite System...\n');

  try {
    // Test 1: Add to favorites
    console.log('1. Testing add to favorites...');
    const favoriteData = {
      doctorId: 'dr_smith_cardiology',
      userName: 'John Doe'
    };

    const addResponse = await axios.post(`${BASE_URL}/favorites/add`, favoriteData);
    console.log('✅ Added to favorites successfully:', addResponse.data);

    // Test 2: Get user favorites
    console.log('\n2. Testing get user favorites...');
    const favoritesResponse = await axios.get(`${BASE_URL}/favorites/user-favorites?userName=John Doe`);
    console.log('✅ User favorites retrieved:', favoritesResponse.data);

    // Test 3: Check if doctor is favorited
    console.log('\n3. Testing check favorite status...');
    const checkResponse = await axios.get(`${BASE_URL}/favorites/check/dr_smith_cardiology?userName=John Doe`);
    console.log('✅ Favorite status checked:', checkResponse.data);

    console.log('\n🎉 All favorite system tests passed!');

  } catch (error) {
    console.error('❌ Error testing favorite system:', error.response?.data || error.message);
  }
}

async function testDashboardData() {
  console.log('\n🧪 Testing Dashboard Data...\n');

  try {
    // Test 1: Get user dashboard data
    console.log('1. Testing dashboard data retrieval...');
    const userName = 'John Doe';
    
    // Get user ratings
    const ratingsResponse = await axios.get(`${BASE_URL}/ratings/user-history?userName=${userName}`);
    console.log('✅ User ratings for dashboard:', ratingsResponse.data);

    // Get user favorites
    const favoritesResponse = await axios.get(`${BASE_URL}/favorites/user-favorites?userName=${userName}`);
    console.log('✅ User favorites for dashboard:', favoritesResponse.data);

    // Get top rated doctors for dashboard
    const topRatedResponse = await axios.get(`${BASE_URL}/ratings/top-rated`);
    console.log('✅ Top rated doctors for dashboard:', topRatedResponse.data);

    console.log('\n🎉 All dashboard data tests passed!');

  } catch (error) {
    console.error('❌ Error testing dashboard data:', error.response?.data || error.message);
  }
}

async function runAllTests() {
  console.log('🚀 Starting comprehensive rating and dashboard system tests...\n');
  
  await testRatingSystem();
  await testFavoriteSystem();
  await testDashboardData();
  
  console.log('\n✨ All tests completed!');
}

runAllTests().catch(console.error); 