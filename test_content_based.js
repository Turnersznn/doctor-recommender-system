import axios from 'axios';

const BASE_URL = 'http://localhost:5000/api';

async function testContentBasedSystem() {
  console.log('🧪 Testing Content-Based Filtering System\n');

  try {
    // Test 1: First-time user (no preferences)
    console.log('📋 Test 1: New User - Eye Symptoms');
    const response1 = await axios.post(`${BASE_URL}/specialist/enhanced-predict`, {
      symptoms: {
        eye_pain: true,
        blurred_vision: true,
        halos_around_lights: true
      },
      userId: 'testuser123'
    });
    
    console.log('✅ Doctors recommended:', response1.data.recommendedDoctors.length);
    console.log('📊 Content scores:', response1.data.recommendedDoctors.map(d => ({
      name: d.name,
      contentScore: d.contentScore,
      reason: d.recommendationReason
    })));

    // Test 2: Update user preferences (positive rating)
    console.log('\n📋 Test 2: User Rates Doctor Positively');
    await axios.post(`${BASE_URL}/preferences/update`, {
      userId: 'testuser123',
      doctorId: response1.data.recommendedDoctors[0].doctorId,
      rating: 5,
      specialty: 'Ophthalmology',
      doctorFeatures: {
        gender: 'F',
        location: 'Lagos'
      }
    });
    console.log('✅ User preferences updated');

    // Test 3: Get user preferences
    console.log('\n📋 Test 3: Check User Preferences');
    const prefs = await axios.get(`${BASE_URL}/preferences/testuser123`);
    console.log('📊 User preferences:', prefs.data.preferences);

    // Test 4: Second recommendation (should be personalized)
    console.log('\n📋 Test 4: Personalized Recommendations');
    const response2 = await axios.post(`${BASE_URL}/specialist/enhanced-predict`, {
      symptoms: {
        eye_pain: true,
        redness_of_eyes: true
      },
      userId: 'testuser123'
    });
    
    console.log('✅ Personalized doctors:', response2.data.recommendedDoctors.map(d => ({
      name: d.name,
      gender: d.gender,
      location: d.location,
      contentScore: d.contentScore,
      reason: d.recommendationReason
    })));

    // Test 5: Compare with anonymous user
    console.log('\n📋 Test 5: Anonymous User (No Personalization)');
    const response3 = await axios.post(`${BASE_URL}/specialist/enhanced-predict`, {
      symptoms: {
        eye_pain: true,
        redness_of_eyes: true
      },
      userId: 'anonymous'
    });
    
    console.log('✅ Anonymous recommendations:', response3.data.recommendedDoctors.map(d => ({
      name: d.name,
      contentScore: d.contentScore || 'No score'
    })));

    console.log('\n🎉 Content-Based System Test Complete!');

  } catch (error) {
    console.error('❌ Test failed:', error.response?.data || error.message);
  }
}

// Run the test
testContentBasedSystem();