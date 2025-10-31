// Test script for the rating system
const testRatingSystem = async () => {
  const baseUrl = 'http://localhost:5000/api';
  
  console.log('🧪 Testing Rating System...\n');
  
  // Test 1: Submit a rating
  console.log('1. Testing rating submission...');
  try {
    const ratingResponse = await fetch(`${baseUrl}/ratings/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        doctorId: 'test-doctor-123',
        rating: 5,
        review: 'Excellent doctor! Very knowledgeable and caring.',
        userName: 'John Doe'
      }),
    });
    
    const ratingData = await ratingResponse.json();
    console.log('✅ Rating submitted successfully:', ratingData);
  } catch (error) {
    console.log('❌ Error submitting rating:', error.message);
  }
  
  // Test 2: Get doctor ratings
  console.log('\n2. Testing get doctor ratings...');
  try {
    const ratingsResponse = await fetch(`${baseUrl}/ratings/doctor/test-doctor-123`);
    const ratingsData = await ratingsResponse.json();
    console.log('✅ Doctor ratings retrieved:', ratingsData);
  } catch (error) {
    console.log('❌ Error getting ratings:', error.message);
  }
  
  // Test 3: Get top rated doctors
  console.log('\n3. Testing get top rated doctors...');
  try {
    const topResponse = await fetch(`${baseUrl}/ratings/top-rated`);
    const topData = await topResponse.json();
    console.log('✅ Top rated doctors retrieved:', topData);
  } catch (error) {
    console.log('❌ Error getting top rated doctors:', error.message);
  }
  
  console.log('\n🎉 Rating system test completed!');
};

// Run the test
testRatingSystem(); 