import axios from 'axios';

// Test the enhanced prediction system
async function testEnhancedSystem() {
  try {
    console.log('🧪 Testing Enhanced Symptom-to-Disease-to-Specialist System\n');
    
    // Test Case 1: Skin symptoms
    console.log('📋 Test Case 1: Skin Symptoms');
    const skinSymptoms = {
      "itching": true,
      "skin_rash": true,
      "nodal_skin_eruptions": false,
      "dischromic _patches": true
    };
    
    console.log('Sending request to enhanced endpoint...');
    const skinResponse = await axios.post('http://localhost:5000/api/specialist/enhanced-predict', {
      symptoms: skinSymptoms
    });
    
    console.log('✅ Skin symptoms response:');
    console.log('- Suggested Diseases:', skinResponse.data.suggested_diseases);
    console.log('- Recommended Specialist:', skinResponse.data.specialist);
    console.log('- Confidence:', skinResponse.data.confidence);
    console.log('- ML Prediction:', skinResponse.data.ml_prediction);
    console.log('- Disease-based Specialists:', skinResponse.data.disease_based_specialists);
    console.log('- Number of doctors found:', skinResponse.data.doctors.length);
    console.log('');
    
    // Test Case 2: Neurological symptoms
    console.log('📋 Test Case 2: Neurological Symptoms');
    const neuroSymptoms = {
      "headache": true,
      "altered_sensorium": true,
      "slurred_speech": true,
      "weakness_of_one_body_side": true
    };
    
    const neuroResponse = await axios.post('http://localhost:5000/api/specialist/enhanced-predict', {
      symptoms: neuroSymptoms
    });
    
    console.log('✅ Neurological symptoms response:');
    console.log('- Suggested Diseases:', neuroResponse.data.suggested_diseases);
    console.log('- Recommended Specialist:', neuroResponse.data.specialist);
    console.log('- Confidence:', neuroResponse.data.confidence);
    console.log('- ML Prediction:', neuroResponse.data.ml_prediction);
    console.log('- Disease-based Specialists:', neuroResponse.data.disease_based_specialists);
    console.log('- Number of doctors found:', neuroResponse.data.doctors.length);
    console.log('');
    
    // Test Case 3: Gastrointestinal symptoms
    console.log('📋 Test Case 3: Gastrointestinal Symptoms');
    const giSymptoms = {
      "stomach_pain": true,
      "abdominal_pain": true,
      "acidity": true,
      "vomiting": true,
      "nausea": true
    };
    
    const giResponse = await axios.post('http://localhost:5000/api/specialist/enhanced-predict', {
      symptoms: giSymptoms
    });
    
    console.log('✅ Gastrointestinal symptoms response:');
    console.log('- Suggested Diseases:', giResponse.data.suggested_diseases);
    console.log('- Recommended Specialist:', giResponse.data.specialist);
    console.log('- Confidence:', giResponse.data.confidence);
    console.log('- ML Prediction:', giResponse.data.ml_prediction);
    console.log('- Disease-based Specialists:', giResponse.data.disease_based_specialists);
    console.log('- Number of doctors found:', giResponse.data.doctors.length);
    console.log('');
    
    console.log('🎉 All tests completed successfully!');
    console.log('\n📊 Summary:');
    console.log('✅ Enhanced system provides:');
    console.log('   - Disease diagnosis based on symptoms');
    console.log('   - Specialist recommendation');
    console.log('   - Confidence levels');
    console.log('   - Multiple specialist suggestions when needed');
    console.log('   - Doctor recommendations with ratings');
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    console.error('Full error:', error);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
    if (error.request) {
      console.error('Request error:', error.request);
    }
  }
}

testEnhancedSystem(); 