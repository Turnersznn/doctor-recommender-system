// src/api/multiSymptomApi.js

const MULTI_SYMPTOM_API_URL = 'http://localhost:8002';

/**
 * Send symptoms to the multi-symptom API and get specialist recommendations
 * @param {Array} symptoms - Array of symptom strings
 * @returns {Promise<Object>} - API response with diagnoses and specialist recommendations
 */
export const getMultiSymptomRecommendations = async (symptoms) => {
  try {
    console.log('🔄 Sending request to multi-symptom API...');
    console.log('Symptoms:', symptoms);
    
    const response = await fetch(`${MULTI_SYMPTOM_API_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ symptoms }),
    });

    console.log('📡 Response status:', response.status);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('❌ Multi-symptom API error:', errorText);
      return { error: `API error: ${response.status} - ${errorText}` };
    }

    const data = await response.json();
    console.log('✅ Multi-symptom API response:', data);

    return data;
  } catch (error) {
    console.error('❌ Network error:', error);
    return { 
      error: `Network error: ${error.message}. Make sure the multi-symptom API is running on port 8002.` 
    };
  }
};

/**
 * Get sample data for demonstration purposes
 * @param {string} type - Type of sample data to return (respiratory, gastrointestinal, neurological)
 * @returns {Object} - Sample API response
 */
export const getSampleMultiSymptomData = (type = 'respiratory') => {
  const samples = {
    respiratory: {
      diagnoses: [
        {
          disease: "Pneumonia",
          confidence: 0.85,
          explanation: "Based on the combination of cough, breathlessness, and high fever"
        },
        {
          disease: "Bronchitis",
          confidence: 0.65,
          explanation: "Consistent with symptoms of cough and breathlessness"
        },
        {
          disease: "Common Cold",
          confidence: 0.45,
          explanation: "Matches some symptoms but lacks other typical indicators"
        }
      ],
      predicted_specialist: "Pulmonologist",
      confidence: 0.85,
      active_symptoms: ["cough", "breathlessness", "high_fever"],
      ml_prediction: true
    },
    gastrointestinal: {
      diagnoses: [
        {
          disease: "Gastroenteritis",
          confidence: 0.9,
          explanation: "Based on the combination of abdominal pain, nausea, and vomiting"
        },
        {
          disease: "Irritable Bowel Syndrome",
          confidence: 0.6,
          explanation: "Consistent with abdominal pain but lacks other key indicators"
        },
        {
          disease: "Food Poisoning",
          confidence: 0.7,
          explanation: "Matches symptoms but would typically include additional indicators"
        }
      ],
      predicted_specialist: "Gastroenterologist",
      confidence: 0.9,
      active_symptoms: ["abdominal_pain", "nausea", "vomiting"],
      ml_prediction: true
    },
    neurological: {
      diagnoses: [
        {
          disease: "Migraine",
          confidence: 0.8,
          explanation: "Based on the combination of headache, dizziness, and visual disturbances"
        },
        {
          disease: "Tension Headache",
          confidence: 0.5,
          explanation: "Consistent with headache but lacks other distinguishing features"
        },
        {
          disease: "Vestibular Disorder",
          confidence: 0.6,
          explanation: "Matches dizziness symptoms but not fully aligned with all indicators"
        }
      ],
      predicted_specialist: "Neurologist",
      confidence: 0.8,
      active_symptoms: ["headache", "dizziness", "visual_disturbances"],
      ml_prediction: true
    }
  };
  
  return samples[type] || samples.respiratory;
};