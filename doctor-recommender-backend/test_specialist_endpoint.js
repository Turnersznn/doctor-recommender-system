// Test specialist endpoint
const testSpecialist = async () => {
  try {
    console.log('Testing specialist endpoint...');
    
    const response = await fetch('http://localhost:5000/api/specialist/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        symptoms: {
          headache: true
        }
      }),
    });
    
    console.log('Response status:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.log('❌ Error response:', errorText);
      return;
    }
    
    const data = await response.json();
    console.log('✅ Specialist endpoint working:', data);
    
  } catch (error) {
    console.log('❌ Network error:', error.message);
  }
};

testSpecialist(); 