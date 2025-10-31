const BASE_URL = 'http://localhost:5000';

async function testSimple() {
  try {
    console.log('🧪 Testing server and auth routes...\n');
    
    // Test 1: Check if server is running
    console.log('1. Testing server connection...');
    const testResponse = await fetch(`${BASE_URL}/test`);
    const testData = await testResponse.json();
    console.log('✅ Server is running:', testData.message);
    
    // Test 2: Check if auth routes are accessible
    console.log('\n2. Testing auth routes...');
    try {
      const authResponse = await fetch(`${BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: 'testuser',
          email: 'test@example.com',
          password: 'password123',
          firstName: 'Test',
          lastName: 'User'
        })
      });
      
      if (authResponse.ok) {
        const authData = await authResponse.json();
        console.log('✅ Auth routes are working:', authData.message);
      } else {
        const errorData = await authResponse.text();
        console.log('❌ Auth routes error:', authResponse.status, errorData);
      }
    } catch (error) {
      console.log('❌ Auth routes error:', error.message);
    }
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
  }
}

testSimple(); 