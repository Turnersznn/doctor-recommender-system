// Test rating endpoint
const testRating = async () => {
  try {
    console.log('Testing rating endpoint...');
    
    const response = await fetch('http://localhost:5000/api/ratings/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        doctorId: 'test-doctor-1',
        rating: 5,
        review: 'Great doctor!',
        userName: 'test-user'
      }),
    });
    
    console.log('Response status:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.log('❌ Error response:', errorText);
      return;
    }
    
    const data = await response.json();
    console.log('✅ Rating submitted successfully:', data);
    
  } catch (error) {
    console.log('❌ Network error:', error.message);
  }
};

testRating(); 