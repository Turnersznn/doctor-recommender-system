#!/usr/bin/env node
/**
 * Test ML API Response Format
 */

const axios = require('axios');

const ML_API_URL = 'http://127.0.0.1:8005/predict';

async function testMLAPIResponse() {
    console.log('🔍 Testing ML API Response Format');
    console.log('=' * 50);
    
    const testSymptoms = {
        headache: true,
        dizziness: true,
        visual_disturbances: true,
        followupanswers: {}
    };
    
    try {
        console.log('\n📤 Sending symptoms to ML API:', testSymptoms);
        
        const response = await axios.post(ML_API_URL, {
            symptoms: testSymptoms
        });
        
        console.log('\n📥 ML API Response:');
        console.log('Status:', response.status);
        console.log('Data:', JSON.stringify(response.data, null, 2));
        
        // Check specific fields
        const data = response.data;
        console.log('\n🔍 Field Analysis:');
        console.log('- diagnoses:', data.diagnoses ? `Array with ${data.diagnoses.length} items` : 'Missing or empty');
        console.log('- suggested_diseases:', data.suggested_diseases ? `Array with ${data.suggested_diseases.length} items` : 'Missing or empty');
        console.log('- predicted_specialist:', data.predicted_specialist || 'Missing');
        console.log('- confidence:', data.confidence || 'Missing');
        
        if (data.diagnoses && data.diagnoses.length > 0) {
            console.log('\n📋 Diagnoses Details:');
            data.diagnoses.forEach((diag, index) => {
                console.log(`  ${index + 1}. ${diag.disease} (${(diag.probability * 100).toFixed(1)}%)`);
                console.log(`     Specialist: ${diag.specialist}`);
                console.log(`     Confidence: ${(diag.confidence * 100).toFixed(1)}%`);
            });
        }
        
        if (data.suggested_diseases && data.suggested_diseases.length > 0) {
            console.log('\n🦠 Suggested Diseases:');
            data.suggested_diseases.forEach((disease, index) => {
                console.log(`  ${index + 1}. ${disease}`);
            });
        }
        
    } catch (error) {
        console.log('❌ Error calling ML API:', error.message);
        if (error.response) {
            console.log('Response status:', error.response.status);
            console.log('Response data:', error.response.data);
        }
        console.log('\nMake sure the ML API is running:');
        console.log('cd ml-doctor-recommender && python ml_multi_symptom_api.py');
    }
    
    console.log('\n' + '=' * 50);
    console.log('ML API test complete!');
}

// Run the test
testMLAPIResponse().catch(console.error);
