import { getEnhancedPrediction } from '../utils/enhancedContentApi.js';
import { ConfidenceAnalyzer } from '../utils/confidenceAnalyzer.js';
import { AdvancedSpecialistRecommender } from '../utils/advancedSpecialistRecommender.js';
import { searchDoctorsForDiagnoses } from '../utils/doctorsApiService.js';
import { ContentBasedRecommender } from '../contentBasedRecommender.js';
import fs from 'fs';
import path from 'path';

// Rule-based disease mapping for quick fixes
const RULE_DISEASES = {
  'skin_rash,itching': {disease: 'Eczema', confidence: 0.75},
  'cough,fever': {disease: 'Common Cold', confidence: 0.7},
  'headache,fever': {disease: 'Viral Infection', confidence: 0.7},
  'stomach_pain,nausea': {disease: 'Gastroenteritis', confidence: 0.8},
  'chest_pain,shortness_of_breath': {disease: 'Heart Disease', confidence: 0.8}
};

function getRuleBasedDiseases(symptoms) {
  if (!symptoms || symptoms.length < 2) return [];

  const results = [];
  const symptomKey = symptoms.slice(0, 2).sort().join(',');

  if (RULE_DISEASES[symptomKey]) {
    results.push(RULE_DISEASES[symptomKey]);
  }

  return results;
}

// Load ratings data
function loadRatings() {
  try {
    const ratingsPath = path.join(process.cwd(), 'data', 'ratings.json');
    const data = fs.readFileSync(ratingsPath, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    return {
      "ratings": {},
      "reviews": {},
      "statistics": {}
    };
  }
}

// Get doctor identifier
function getDoctorId(doctor) {
  return `${doctor.name}-${doctor.location}`.replace(/\s+/g, '-');
}

// Map model predictions to actual specialist names in the doctor database
const SPECIALIST_MAPPING = {
  // Direct matches
  "Dermatologist": "Dermatology",
  "Dermatologists": "Dermatology",
  "Cardiologist": "Internal Medicine, Cardiovascular Disease",
  "Gastroenterologist": "Internal Medicine, Gastroenterology",
  "Endocrinologist": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
  "Pulmonologist": "Internal Medicine, Pulmonary Disease",
  "Neurologist": "Psychiatry & Neurology, Neurology",
  "Allergist": "Allergy & Immunology",
  "Otolaryngologist": "Otolaryngology",
  "Gynecologist": "Obstetrics & Gynecology",
  "Pediatrician": "Pediatrics",
  "Rheumatologists": "Internal Medicine, Rheumatology",
  "Ophthalmologist": "Ophthalmology",
  
  // Dental specialists
  "Dentistry": "Dentist",
  "Emergency Dentistry": "Dentist",
  "Dentist, General Practice": "Dentist",
  "Dentist, Oral and Maxillofacial Surgery": "Dentist",
  "Dentist, Pediatric Dentistry": "Dentist",
  
  // Close matches
  "Internal Medcine": "Internal Medicine",
  "Hepatologist": "Internal Medicine, Gastroenterology",
  "Phlebologist": "Internal Medicine, Cardiovascular Disease",
  "Osteopathic": "Family Medicine",
  "Osteoarthristis": "Internal Medicine, Rheumatology",
  "Common Cold": "Family Medicine",
};

export const enhancedPredictSpecialist = async (req, res) => {
  const symptoms = req.body.symptoms;
  const userId = req.body.userId || 'anonymous'; // Get user ID for personalization
  if (!symptoms || typeof symptoms !== 'object') {
    return res.status(400).json({ error: 'Symptoms must be provided as an object.' });
  }
  try {
    // Initialize analyzers and recommenders
    const confidenceAnalyzer = new ConfidenceAnalyzer();
    const specialistRecommender = new AdvancedSpecialistRecommender();
    const contentRecommender = new ContentBasedRecommender();

    // Get enhanced prediction with disease diagnosis
    const prediction = await getEnhancedPrediction(symptoms);
    console.log('Enhanced prediction received:', prediction);

    // Use the correct fields from ML API response
    const primarySpecialist = prediction.predicted_specialist || 'General Practitioner';

    // Use the actual diagnoses array from ML API (has individual confidence scores)
    let diagnoses = prediction.diagnoses || [];
    console.log('🔍 ML API diagnoses:', diagnoses);
    console.log('🔍 Diagnoses length:', diagnoses.length);
    console.log('🔍 Suggested diseases:', prediction.suggested_diseases);

    // QUICK FIX: Use rule-based diseases for common patterns
    const ruleBasedDiseases = getRuleBasedDiseases(prediction.active_symptoms);

    if (ruleBasedDiseases.length > 0) {
      console.log('✅ Using rule-based diseases:', ruleBasedDiseases.map(d => d.disease));
      diagnoses = ruleBasedDiseases.map(rule => ({
        disease: rule.disease,
        specialist: prediction.predicted_specialist,
        confidence: rule.confidence,
        probability: rule.confidence,
        explanation: `Based on symptom analysis, ${rule.disease} is likely (${(rule.confidence * 100).toFixed(0)}% confidence). Recommended specialist: ${prediction.predicted_specialist}`,
        matching_symptoms: prediction.active_symptoms || []
      }));
    } else if (diagnoses.length === 0 && prediction.suggested_diseases && prediction.suggested_diseases.length > 0) {
      console.log('⚠️ Creating diagnoses from suggested_diseases:', prediction.suggested_diseases);

      // Create diagnoses from suggested diseases
      diagnoses = prediction.suggested_diseases.map((disease, index) => {
        const baseConfidence = prediction.confidence || 0.6;
        const confidence = baseConfidence * (1 - (index * 0.1));

        return {
          disease: disease,
          specialist: prediction.predicted_specialist,
          confidence: Math.max(confidence, 0.3),
          probability: Math.max(confidence, 0.3),
          explanation: `Based on your symptoms, ${disease} is a possible condition. Recommended specialist: ${prediction.predicted_specialist}`,
          matching_symptoms: prediction.active_symptoms || []
        };
      });

      console.log('✅ Created diagnoses from suggested diseases:', diagnoses.length);
    } else if (diagnoses.length === 0) {
      console.log('⚠️ Using fallback diagnoses creation - no suggested diseases available');
      diagnoses = [{
        disease: `Condition requiring ${prediction.predicted_specialist} consultation`,
        specialist: prediction.predicted_specialist,
        confidence: prediction.confidence,
        probability: prediction.confidence
      }];
    } else {
      console.log('✅ Using ML API diagnoses with individual confidence scores');
    }

    // Map specialists using SPECIALIST_MAPPING if possible
    const mappedDiagnoses = diagnoses.map(d => ({
      ...d,
      specialist: SPECIALIST_MAPPING[d.specialist] || d.specialist
    }));

    // Analyze confidence for all diagnoses
    const enhancedDiagnoses = confidenceAnalyzer.analyzeConfidence(mappedDiagnoses, symptoms);

    // Check if we should show warning
    const showWarning = confidenceAnalyzer.shouldShowWarning(enhancedDiagnoses);
    const warningMessage = showWarning ? confidenceAnalyzer.generateWarningMessage(symptoms) : null;

    // Generate advanced specialist recommendations
    const advancedRecommendations = specialistRecommender.generateAdvancedRecommendations(
      enhancedDiagnoses,
      symptoms,
      { showWarning, warningMessage }
    );
    // Filter specialists based on confidence - only include those with meaningful confidence
    const confidenceThreshold = 0.1; // 10% minimum confidence
    const highConfidenceSpecialists = [];

    // Add specialists from high-confidence diagnoses only
    for (const diagnosis of enhancedDiagnoses) {
      if (diagnosis.confidence > confidenceThreshold && !highConfidenceSpecialists.includes(diagnosis.specialist)) {
        highConfidenceSpecialists.push(diagnosis.specialist);
      }
    }

    // Ensure primary specialist is always first if it's high confidence
    const specialistsToSearch = highConfidenceSpecialists.length > 0 ?
      highConfidenceSpecialists : [primarySpecialist];

    // Get doctors using DoctorsAPI first, fallback to local data
    let doctorsFromAPI = [];
    try {
      console.log('🔍 Attempting to fetch doctors from DoctorsAPI...');
      console.log('🔍 Enhanced diagnoses for doctor search:', enhancedDiagnoses);
      console.log('🔍 Disease-based specialists:', prediction.disease_based_specialists);
      console.log('🔍 Specialists to search for:', specialistsToSearch);
      console.log('🔍 Primary specialist:', primarySpecialist);
      console.log('🔍 High confidence specialists only:', highConfidenceSpecialists);
      console.log('🔍 Confidence threshold:', confidenceThreshold);

      // Create diagnoses format for doctor search
      const diagnosesForSearch = specialistsToSearch.map(specialist => ({
        specialist: specialist,
        disease: `${specialist} Condition`,
        probability: 0.8
      }));

      doctorsFromAPI = await searchDoctorsForDiagnoses(diagnosesForSearch);
      console.log(`✅ DoctorsAPI returned ${doctorsFromAPI.length} doctors`);
    } catch (error) {
      console.log('⚠️ DoctorsAPI failed, falling back to local data:', error.message);
    }

    let topDoctors = doctorsFromAPI;

    // Fallback to local data if DoctorsAPI didn't return enough results
    if (topDoctors.length < 3) {
      console.log('📁 Using local doctors data as fallback...');
      try {
        const dataPath = path.join(process.cwd(), '..', 'ml-doctor-recommender', 'final_data.json');
        const raw = fs.readFileSync(dataPath, 'utf-8');
        const data = JSON.parse(raw);
        let allDoctors = [];

        for (const entry of data) {
          if (Array.isArray(entry) && entry[1] && entry[1].results && Array.isArray(entry[1].results)) {
            allDoctors = allDoctors.concat(entry[1].results);
          }
        }

        // Filter doctors by taxonomy description
        const localDoctors = allDoctors
          .map(doc => {
            const taxonomy = (doc.taxonomies || []).find(t => t.primary) || (doc.taxonomies || [])[0];
            const specialty = taxonomy ? taxonomy.desc : '';
            let name = '';
            if (doc.basic) {
              name = doc.basic.organization_name || (doc.basic.first_name ? `${doc.basic.first_name} ${doc.basic.last_name}` : '');
            }
            let location = '';
            if (doc.addresses && Array.isArray(doc.addresses)) {
              const loc = doc.addresses.find(a => a.address_purpose === 'LOCATION');
              if (loc) location = `${loc.address_1 || ''} ${loc.city || ''} ${loc.state || ''}`.trim();
            }
            return { name, specialty, location };
          })
          .filter(doc => {
            if (!doc.specialty) return false;
            const specialtyLower = doc.specialty.toLowerCase();
            const primaryLower = primarySpecialist.toLowerCase();
            
            // Direct match
            if (specialtyLower.includes(primaryLower)) return true;
            
            // Dental specialist matching
            if (primaryLower.includes('dentist') && specialtyLower.includes('dentist')) return true;
            if (primaryLower === 'dentistry' && specialtyLower.includes('dentist')) return true;
            if (primaryLower === 'emergency dentistry' && specialtyLower.includes('dentist')) return true;
            
            return false;
          });

        // Remove duplicates
        const uniqueDoctors = [];
        const seen = new Set();
        for (const doc of localDoctors) {
          const key = `${doc.name}|${doc.specialty}|${doc.location}`;
          if (!seen.has(key)) {
            uniqueDoctors.push(doc);
            seen.add(key);
          }
        }

        // Combine API and local doctors, prioritizing API results
        const combinedDoctors = [...topDoctors, ...uniqueDoctors.slice(0, 5 - topDoctors.length)];
        
        // Apply content-based filtering for personalized recommendations
        const personalizedDoctors = contentRecommender.recommendDoctors(
          userId, 
          combinedDoctors, 
          primarySpecialist, 
          5
        );
        
        topDoctors = personalizedDoctors.length > 0 ? personalizedDoctors : combinedDoctors.slice(0, 5);

      } catch (localError) {
        console.error('❌ Local data fallback failed:', localError.message);
        // Create minimal fallback doctors
        topDoctors = [{
          name: `Dr. ${primarySpecialist} Specialist`,
          specialty: primarySpecialist,
          location: 'Medical Center'
        }];
      }
    }
    // Load ratings data and add rating information
    const ratingsData = loadRatings();
    console.log('📊 Ratings data loaded:', ratingsData ? 'Success' : 'Failed');

    const doctorsWithRatings = topDoctors.map(doctor => {
      const doctorId = getDoctorId(doctor);
      const statistics = (ratingsData && ratingsData.statistics && ratingsData.statistics[doctorId]) || {
        averageRating: doctor.rating || 4.5, // Use existing rating or default
        totalRatings: 0,
        totalReviews: 0
      };
      const finalRating = statistics.averageRating > 0 ? statistics.averageRating : (doctor.rating || 4.5);

      return {
        ...doctor,
        doctorId,
        rating: finalRating,
        totalRatings: statistics.totalRatings,
        totalReviews: statistics.totalReviews
      };
    });
    doctorsWithRatings.sort((a, b) => b.rating - a.rating);
    // Return comprehensive enhanced response
    res.json({
      diagnoses: enhancedDiagnoses,
      recommendedDoctors: doctorsWithRatings,
      specialistRecommendations: advancedRecommendations,
      // Add ML prediction data for frontend compatibility
      predicted_specialist: primarySpecialist,
      suggested_diseases: prediction.suggested_diseases || [],
      active_symptoms: prediction.active_symptoms || [],
      ml_prediction: primarySpecialist,
      disease_based_specialists: specialistsToSearch,
      confidence: {
        score: prediction.confidence || (diagnoses[0]?.confidence || 0.6),
        showWarning,
        warningMessage,
        analysisMetadata: {
          totalSymptoms: Object.keys(symptoms).filter(key => key !== 'followUpAnswers').length,
          symptomsWithSeverity: Object.entries(symptoms).filter(([_, value]) =>
            typeof value === 'object' && value.severity
          ).length,
          highConfidenceDiagnoses: enhancedDiagnoses.filter(d => d.confidenceLevel === 'HIGH').length,
          moderateConfidenceDiagnoses: enhancedDiagnoses.filter(d => d.confidenceLevel === 'MODERATE').length,
          urgencyLevel: advancedRecommendations.urgencyLevel
        }
      }
    });
  } catch (err) {
    console.error('Enhanced prediction error:', err);

    // Return fallback response with sample data for testing
    const fallbackDiagnoses = [
      {
        disease: 'General Health Concern',
        probability: 0.70,
        specialist: 'Family Medicine',
        confidence: 0.60,
        confidenceLevel: 'MODERATE',
        explanation: 'Based on your symptoms, we recommend starting with a Family Medicine specialist for comprehensive evaluation.'
      }
    ];

    const fallbackDoctors = [
      {
        name: 'Dr. Sarah Johnson',
        specialty: 'Family Medicine',
        location: 'Medical Center',
        rating: 4.8,
        totalRatings: 150,
        totalReviews: 45,
        phone: '(555) 123-4567',
        address: '123 Medical Plaza, Healthcare City'
      },
      {
        name: 'Dr. Michael Chen',
        specialty: 'Internal Medicine',
        location: 'General Hospital',
        rating: 4.7,
        totalRatings: 200,
        totalReviews: 67,
        phone: '(555) 987-6543',
        address: '456 Health Street, Medical District'
      }
    ];

    res.json({
      diagnoses: fallbackDiagnoses,
      recommendedDoctors: fallbackDoctors,
      specialistRecommendations: {
        urgencyLevel: 'MODERATE',
        recommendations: ['Schedule an appointment with a Family Medicine specialist'],
        followUpQuestions: []
      },
      confidence: {
        showWarning: true,
        warningMessage: 'ML service unavailable - showing fallback recommendations',
        analysisMetadata: {
          totalSymptoms: 1,
          symptomsWithSeverity: 0,
          highConfidenceDiagnoses: 0,
          moderateConfidenceDiagnoses: 1,
          urgencyLevel: 'MODERATE'
        }
      }
    });
  }
}; 