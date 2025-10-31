// src/api.js
const API_BASE_URL = 'http://localhost:5000';

export const getRecommendations = async (symptomsObj) => {
  try {
    console.log('🔄 Sending request to backend...');
    console.log('Symptoms:', symptomsObj);
    console.log('URL:', `${API_BASE_URL}/api/specialist/enhanced-predict`);

    const res = await fetch(`${API_BASE_URL}/api/specialist/enhanced-predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ symptoms: symptomsObj }),
    });

    console.log('📡 Response status:', res.status);
    console.log('📡 Response ok:', res.ok);

    if (!res.ok) {
      const errorText = await res.text();
      console.error('❌ Backend error:', errorText);
      return { error: `Backend error: ${res.status} - ${errorText}` };
    }

    const data = await res.json();
    console.log('✅ Backend response:', data);

    return data;
  } catch (error) {
    console.error('❌ API error:', error);
    return { error: `Network error: ${error.message}` };
  }
};
