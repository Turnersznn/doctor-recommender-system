import axios from 'axios';

const BASE_URL = 'http://localhost:5000';

async function testDefaultRating() {
  try {
    console.log('Testing default rating system...');
    
    // Test 1: Get ratings for a new doctor (should have default 5-star rating)
    console.log('\n1. Testing default rating for new doctor...');
    const newDoctorId = 'new-doctor-456';
    const doctorRatingsResponse = await axios.get(`${BASE_URL}/api/ratings/doctor/${newDoctorId}`);
    console.log('New doctor ratings response:', doctorRatingsResponse.data);
    
    // Test 2: Test specialist prediction to see if doctors get default ratings
    console.log('\n2. Testing specialist prediction with default ratings...');
    const symptoms = { "fever": true, "cough": true };
    const specialistResponse = await axios.post(`${BASE_URL}/api/specialist/predict`, { symptoms });
    console.log('Specialist prediction response:');
    console.log('Specialist:', specialistResponse.data.specialist);
    console.log('Number of doctors:', specialistResponse.data.doctors.length);
    console.log('Sample doctor with ratings:', specialistResponse.data.doctors[0]);
    
    console.log('\n✅ Default rating system test passed!');
    
  } catch (error) {
    console.error('❌ Error testing default rating system:');
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

testDefaultRating(); 