// Test if server is running
const testServer = async () => {
  try {
    console.log('Testing server status...');
    
    // Test a simple GET request to see if server responds
    const response = await fetch('http://localhost:5000/', {
      method: 'GET',
    });
    
    console.log('Response status:', response.status);
    console.log('Response headers:', response.headers);
    
    const text = await response.text();
    console.log('Response body:', text.substring(0, 200) + '...');
    
  } catch (error) {
    console.log('❌ Server not responding:', error.message);
  }
};

testServer(); 