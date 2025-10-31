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

export async function getDiagnosesAndSpecialists(symptoms) {
  try {
    // Normalize symptom names from frontend format to model format
    const normalizedSymptoms = {};
    for (const [key, value] of Object.entries(symptoms)) {
      const normalizedKey = normalizeSymptomName(key);
      normalizedSymptoms[normalizedKey] = value;
    }
    console.log('Original symptoms received:', symptoms);
    console.log('Sending normalized symptoms to Multi-Symptom API:', normalizedSymptoms);
    console.log('Original keys:', Object.keys(symptoms));
    console.log('Normalized keys:', Object.keys(normalizedSymptoms));

    // Call the ML-powered multi-symptom API
    const response = await axios.post('http://127.0.0.1:8005/predict', {
      symptoms: normalizedSymptoms
    });

    console.log('Multi-symptom API response:', response.data);
    return response.data.diagnoses; // Array of {disease, probability, specialist}
  } catch (error) {
    console.error('Error calling multi-symptom API:', error.message);
    throw error;
  }
}