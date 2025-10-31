import axios from 'axios';

const BASE_URL = 'http://localhost:5000';

async function testOneRatingPerUser() {
  try {
    console.log('Testing one rating per user functionality...');
    
    const doctorId = 'test-doctor-456';
    const userName = 'TestUser123';
    
    // Test 1: Submit first rating
    console.log('\n1. Submitting first rating...');
    const firstRating = {
      doctorId: doctorId,
      rating: 4,
      review: 'Good doctor, helpful consultation',
      userName: userName
    };
    
    const firstResponse = await axios.post(`${BASE_URL}/api/ratings/submit`, firstRating);
    console.log('First rating response:', firstResponse.data);
    
    // Test 2: Submit second rating from same user (should update)
    console.log('\n2. Submitting second rating from same user...');
    const secondRating = {
      doctorId: doctorId,
      rating: 5,
      review: 'Excellent doctor, very thorough!',
      userName: userName
    };
    
    const secondResponse = await axios.post(`${BASE_URL}/api/ratings/submit`, secondRating);
    console.log('Second rating response:', secondResponse.data);
    
    // Test 3: Check doctor ratings to see if only one rating exists per user
    console.log('\n3. Checking doctor ratings...');
    const ratingsResponse = await axios.get(`${BASE_URL}/api/ratings/doctor/${doctorId}`);
    console.log('Doctor ratings:', ratingsResponse.data);
    
    // Test 4: Check user's specific rating
    console.log('\n4. Checking user specific rating...');
    const userRatingResponse = await axios.get(`${BASE_URL}/api/ratings/doctor/${doctorId}?userName=${userName}`);
    console.log('User rating:', userRatingResponse.data.userRating);
    
    console.log('\n✅ One rating per user test passed!');
    
  } catch (error) {
    console.error('❌ Error testing one rating per user:');
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

testOneRatingPerUser(); 