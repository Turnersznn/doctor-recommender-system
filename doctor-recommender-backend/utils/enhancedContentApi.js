import axios from 'axios';

// Function to normalize symptom names from frontend to model format
function normalizeSymptomName(symptomName) {
  return symptomName
    .toLowerCase()
    .replace(/\s+/g, '_')  // Replace spaces with underscores
    .replace(/[^a-z0-9_]/g, '')  // Remove special characters
    .replace(/^_+/, '')  // Remove leading underscores
    .replace(/_+$/, '');  // Remove trailing underscores
}

export async function getEnhancedPrediction(symptoms) {
  try {
    // Normalize symptom names from frontend format to model format
    const normalizedSymptoms = {};
    for (const [key, value] of Object.entries(symptoms)) {
      const normalizedKey = normalizeSymptomName(key);
      normalizedSymptoms[normalizedKey] = value;
    }
    
    console.log('Original symptoms received:', symptoms);
    console.log('Sending normalized symptoms to Enhanced FastAPI:', normalizedSymptoms);
    
    const response = await axios.post('http://127.0.0.1:8002/predict', {
      symptoms: normalizedSymptoms
    });

    console.log('Enhanced prediction received:', response.data);
    console.log('Raw diagnoses from ML API:', response.data.diagnoses);
    console.log('Raw suggested_diseases from ML API:', response.data.suggested_diseases);

    return {
      predicted_specialist: response.data.predicted_specialist,
      confidence: response.data.confidence,
      suggested_diseases: response.data.suggested_diseases,
      active_symptoms: response.data.active_symptoms,
      ml_prediction: response.data.ml_prediction,
      disease_based_specialists: response.data.disease_based_specialists,
      diagnoses: response.data.diagnoses || [] // Include diagnoses from ML API
    };
  } catch (error) {
    console.error('Error calling enhanced content API:', error.message);
    throw error;
  }
}

// Keep the original function for backward compatibility
export async function getPredictedSpecialist(symptoms) {
  try {
    // Normalize symptom names from frontend format to model format
    const normalizedSymptoms = {};
    for (const [key, value] of Object.entries(symptoms)) {
      const normalizedKey = normalizeSymptomName(key);
      normalizedSymptoms[normalizedKey] = value;
    }
    
    console.log('Original symptoms received:', symptoms);
    console.log('Sending normalized symptoms to FastAPI:', normalizedSymptoms);
    console.log('Original keys:', Object.keys(symptoms));
    console.log('Normalized keys:', Object.keys(normalizedSymptoms));
    
    const response = await axios.post('http://127.0.0.1:8000/predict', {
      symptoms: normalizedSymptoms
    });
    return response.data.predicted_specialist;
  } catch (error) {
    console.error('Error calling content API:', error.message);
    throw error;
  }
} 