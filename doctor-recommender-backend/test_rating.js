import axios from 'axios';

const BASE_URL = 'http://localhost:5000';

async function testRatingSystem() {
  try {
    console.log('Testing rating system...');
    
    // Test 1: Submit a rating
    console.log('\n1. Testing rating submission...');
    const ratingData = {
      doctorId: 'test-doctor-123',
      rating: 5,
      review: 'Great doctor, very helpful!',
      userName: 'Test User'
    };
    
    const submitResponse = await axios.post(`${BASE_URL}/api/ratings/submit`, ratingData);
    console.log('Rating submission response:', submitResponse.data);
    
    // Test 2: Get doctor ratings
    console.log('\n2. Testing get doctor ratings...');
    const doctorRatingsResponse = await axios.get(`${BASE_URL}/api/ratings/doctor/test-doctor-123`);
    console.log('Doctor ratings response:', doctorRatingsResponse.data);
    
    // Test 3: Get top rated doctors
    console.log('\n3. Testing get top rated doctors...');
    const topRatedResponse = await axios.get(`${BASE_URL}/api/ratings/top-rated`);
    console.log('Top rated doctors response:', topRatedResponse.data);
    
    console.log('\n✅ All rating system tests passed!');
    
  } catch (error) {
    console.error('❌ Error testing rating system:');
    console.error('Error message:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
    if (error.code) {
      console.error('Error code:', error.code);
    }
  }
}

testRatingSystem(); 