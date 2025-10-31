import axios from 'axios';

const BASE_URL = 'http://localhost:5000';
const DEFAULT_USER = 'DemoUser';

async function populateDashboardData() {
  try {
    console.log('Populating dashboard with sample data...');
    
    // Test 1: Submit some ratings
    console.log('\n1. Submitting sample ratings...');
    const ratings = [
      {
        doctorId: 'test-doctor-1',
        rating: 5,
        review: 'Excellent doctor, very thorough and caring',
        userName: DEFAULT_USER
      },
      {
        doctorId: 'test-doctor-2',
        rating: 4,
        review: 'Good consultation, helpful advice',
        userName: DEFAULT_USER
      },
      {
        doctorId: 'test-doctor-3',
        rating: 5,
        review: 'Great experience, highly recommended',
        userName: DEFAULT_USER
      }
    ];
    
    for (const rating of ratings) {
      const response = await axios.post(`${BASE_URL}/api/ratings/submit`, rating);
      console.log(`Rating submitted for ${rating.doctorId}:`, response.data.message);
    }
    
    // Test 2: Add some favorite doctors
    console.log('\n2. Adding sample favorite doctors...');
    const favorites = [
      {
        doctorId: 'test-doctor-1',
        doctorName: 'Dr. Sarah Johnson',
        specialty: 'Cardiology',
        location: 'Austin, TX',
        userName: DEFAULT_USER
      },
      {
        doctorId: 'test-doctor-2',
        doctorName: 'Dr. Michael Chen',
        specialty: 'Dermatology',
        location: 'Houston, TX',
        userName: DEFAULT_USER
      },
      {
        doctorId: 'test-doctor-3',
        doctorName: 'Dr. Emily Rodriguez',
        specialty: 'Pediatrics',
        location: 'Dallas, TX',
        userName: DEFAULT_USER
      }
    ];
    
    for (const favorite of favorites) {
      const response = await axios.post(`${BASE_URL}/api/favorites/add`, favorite);
      console.log(`Favorite added for ${favorite.doctorName}:`, response.data.message);
    }
    
    // Test 3: Verify the data
    console.log('\n3. Verifying dashboard data...');
    
    const ratingsResponse = await axios.get(`${BASE_URL}/api/ratings/user-history?userName=${DEFAULT_USER}`);
    console.log('User ratings:', ratingsResponse.data);
    
    const favoritesResponse = await axios.get(`${BASE_URL}/api/favorites/user-favorites?userName=${DEFAULT_USER}`);
    console.log('User favorites:', favoritesResponse.data);
    
    console.log('\n✅ Dashboard data populated successfully!');
    
  } catch (error) {
    console.error('❌ Error populating dashboard data:');
    console.error('Error message:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
  }
}

populateDashboardData(); 