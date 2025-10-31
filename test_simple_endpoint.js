// Test if backend is responding
const testBackend = async () => {
  try {
    console.log('Testing backend connection...');
    
    const response = await fetch('http://localhost:5000/api/specialist', {
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
    
    if (!response.ok) {
      const errorText = await response.text();
      console.log('❌ Error response:', response.status, errorText);
      return;
    }
    
    const data = await response.json();
    console.log('✅ Backend is working:', data);
    
  } catch (error) {
    console.log('❌ Network error:', error.message);
  }
};

testBackend(); 