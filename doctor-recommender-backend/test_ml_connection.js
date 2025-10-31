import axios from 'axios';

async function testMLConnection() {
    console.log('Testing ML API connection...');
    
    const testSymptoms = {
        symptoms: {
            chest_pain: true,
            headache: true,
            fatigue: true
        }
    };
    
    try {
        console.log('Sending request to http://127.0.0.1:8000/predict');
        console.log('Payload:', JSON.stringify(testSymptoms, null, 2));
        
        const response = await axios.post('http://127.0.0.1:8000/predict', testSymptoms, {
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        console.log('✅ Success! Status:', response.status);
        console.log('Response data:', JSON.stringify(response.data, null, 2));
        
        if (response.data.diagnoses && response.data.diagnoses.length > 0) {
            console.log('\n📋 Diagnoses received:');
            response.data.diagnoses.forEach((diag, index) => {
                console.log(`  ${index + 1}. ${diag.disease} - ${(diag.probability * 100).toFixed(1)}% - ${diag.specialist}`);
            });
        }
        
    } catch (error) {
        console.log('❌ Error connecting to ML API:');
        if (error.code === 'ECONNREFUSED') {
            console.log('  - ML service is not running on port 8000');
            console.log('  - Make sure to start: python simple_api.py');
        } else if (error.code === 'ETIMEDOUT') {
            console.log('  - Request timed out');
        } else {
            console.log('  - Error:', error.message);
        }
    }
}

testMLConnection();
