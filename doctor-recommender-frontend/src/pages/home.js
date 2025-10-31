
import React, { useState } from 'react';
import { getRecommendations } from '../api/api';
import EnhancedSymptomSelector from '../components/EnhancedSymptomSelector';
import EnhancedResults from '../components/EnhancedResults';
import FollowUpQuestions from '../components/FollowUpQuestions';
import './home.css';

// Curated set of most common/user-friendly symptoms
const COMMON_SYMPTOMS = [
  "fever", "itching", "skin_rash", "cough", "headache", "chest_pain", "abdominal_pain", 
  "nausea", "vomiting", "diarrhoea", "constipation", "joint_pain", "back_pain", 
  "muscle_weakness", "fatigue", "dizziness", "breathlessness", "palpitations", 
  "loss_of_appetite", "weight_loss", "weight_gain", "anxiety", "depression",
  "irregular_sugar_level", "excessive_hunger", "abnormal_menstruation", 
  "burning_micturition", "dark_urine", "sweating", "mild_fever", "high_fever"
];

// All symptoms including dental and eye symptoms
const ALL_SYMPTOMS = [
  // Original symptoms
  "fever", "itching", "skin_rash", "nodal_skin_eruptions", "dischromic_patches", "continuous_sneezing", "shivering", "chills", "watering_from_eyes", "stomach_pain", "acidity", "ulcers_on_tongue", "vomiting", "cough", "chest_pain", "yellowish_skin", "nausea", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes", "burning_micturition", "spotting_urination", "passage_of_gases", "internal_itching", "indigestion", "muscle_wasting", "patches_in_throat", "high_fever", "extra_marital_contacts", "fatigue", "weight_loss", "restlessness", "lethargy", "irregular_sugar_level", "blurred_and_distorted_vision", "obesity", "excessive_hunger", "increased_appetite", "polyuria", "sunken_eyes", "dehydration", "diarrhoea", "breathlessness", "family_history", "mucoid_sputum", "headache", "dizziness", "loss_of_balance", "lack_of_concentration", "stiff_neck", "depression", "irritability", "visual_disturbances", "back_pain", "weakness_in_limbs", "neck_pain", "weakness_of_one_body_side", "altered_sensorium", "dark_urine", "sweating", "muscle_pain", "muscle_aches", "mild_fever", "swelled_lymph_nodes", "malaise", "red_spots_over_body", "joint_pain", "pain_behind_the_eyes", "constipation", "toxic_look_typhos", "belly_pain", "yellow_urine", "receiving_blood_transfusion", "receiving_unsterile_injections", "coma", "stomach_bleeding", "acute_liver_failure", "swelling_of_stomach", "distention_of_abdomen", "history_of_alcohol_consumption", "fluid_overload", "phlegm", "blood_in_sputum", "throat_irritation", "redness_of_eyes", "sinus_pressure", "runny_nose", "congestion", "loss_of_smell", "fast_heart_rate", "rusty_sputum", "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", "irritation_in_anus", "cramps", "bruising", "swollen_legs", "swollen_blood_vessels", "prominent_veins_on_calf", "weight_gain", "cold_hands_and_feets", "mood_swings", "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails", "swollen_extremeties", "abnormal_menstruation", "muscle_weakness", "anxiety", "slurred_speech", "palpitations", "drying_and_tingling_lips", "knee_pain", "hip_joint_pain", "swelling_joints", "painful_walking", "movement_stiffness", "spinning_movements", "unsteadiness", "pus_filled_pimples", "blackheads", "scurring", "bladder_discomfort", "foul_smell_of_urine", "continuous_feel_of_urine", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", "blister", "red_sore_around_nose", "yellow_crust_ooze",

  // Dental symptoms from multi_symptom_mapper.py
  "toothache", "tooth_sensitivity", "jaw_pain", "facial_swelling", "bleeding_gums", "swollen_gums", "bad_breath", "jaw_clicking",

  // Eye symptoms from multi_symptom_mapper.py
  "eye_pain", "redness_of_eyes", "blurred_vision", "halos_around_lights"
];

function Home() {
  const [selectedSymptoms, setSelectedSymptoms] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showFollowUp, setShowFollowUp] = useState(false);
  const [followUpAnswers, setFollowUpAnswers] = useState({});

  // Handle follow-up questions
  const handleFollowUpAnswers = (answers) => {
    setFollowUpAnswers(answers);
  };

  const handleFollowUpComplete = (answers) => {
    setFollowUpAnswers(answers);
    setShowFollowUp(false);
    // Trigger new analysis with follow-up data
    handleSubmitWithFollowUp(answers);
  };

  const handleSubmitWithFollowUp = async (followUpData = {}) => {
    setLoading(true);
    setResult(null);
    try {
      const processedSymptoms = processSymptoms(selectedSymptoms);

      // Include follow-up answers in the request
      const enhancedRequest = {
        ...processedSymptoms,
        followUpAnswers: followUpData
      };

      const response = await getRecommendations(enhancedRequest);
      console.log('🎯 ML response received in home:', response);

      // Handle ML-specific response format
      if (response && response.diagnoses) {
        setResult(response);
      } else if (response && response.error) {
        setResult({ error: response.error });
      } else {
        // Fallback for unexpected response format
        setResult({
          error: "Unexpected response format from ML model",
          diagnoses: [],
          ml_powered: false
        });
      }

      // Save search history with follow-up data
      const userData = localStorage.getItem('user');
      const user = userData ? JSON.parse(userData) : null;
      const userName = user?.username || 'User';
      const searchHistory = JSON.parse(localStorage.getItem(`searchHistory_${userName}`) || '[]');
      const newSearch = {
        symptoms: Object.keys(selectedSymptoms).filter(s => selectedSymptoms[s]),
        diagnoses: response.diagnoses || [],
        timestamp: new Date().toISOString(),
        severityInfo: Object.entries(selectedSymptoms).reduce((acc, [symptom, value]) => {
          if (typeof value === 'object' && value.severity) {
            acc[symptom] = value.severity;
          }
          return acc;
        }, {}),
        followUpAnswers: followUpData
      };
      searchHistory.unshift(newSearch);
      if (searchHistory.length > 10) {
        searchHistory.splice(10);
      }
      localStorage.setItem(`searchHistory_${userName}`, JSON.stringify(searchHistory));
    } catch (error) {
      console.error('Error getting ML recommendations:', error);
      setResult({
        error: 'Failed to connect to ML model. Please check if the ML API is running on port 8005 and try again.',
        diagnoses: [],
        ml_powered: false
      });
    } finally {
      setLoading(false);
    }
  };

  // Process symptoms for API call (handle severity levels)
  const processSymptoms = (symptoms) => {
    const processed = {};
    Object.entries(symptoms).forEach(([symptom, value]) => {
      if (typeof value === 'object' && value.selected) {
        // Include severity in the symptom name for better prediction
        const severityModifier = value.severity === 'severe' ? '_severe' :
                               value.severity === 'mild' ? '_mild' : '';
        processed[symptom + severityModifier] = true;
        processed[symptom] = true; // Also include base symptom
      } else if (value === true) {
        processed[symptom] = true;
      }
    });
    return processed;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check if we should show follow-up questions first
    const symptomCount = Object.keys(selectedSymptoms).length;
    if (symptomCount >= 2 && !showFollowUp && Object.keys(followUpAnswers).length === 0) {
      setShowFollowUp(true);
      return;
    }

    // Proceed with analysis
    await handleSubmitWithFollowUp(followUpAnswers);
  };

  return (
    <div className="home-bg">
      <div className="card doctor-card">
        <div className="doctor-header">
          <div className="doctor-title">
            <span className="doctor-icon">🏥</span>
            MediMatch
          </div>
        </div>

        <EnhancedSymptomSelector
          selectedSymptoms={selectedSymptoms}
          onSymptomsChange={setSelectedSymptoms}
          availableSymptoms={ALL_SYMPTOMS}
        />

        <form onSubmit={handleSubmit} style={{ marginTop: '20px' }}>
          <button
            className="submit-btn"
            type="submit"
            disabled={loading || Object.keys(selectedSymptoms).length === 0}
            style={{
              width: '100%',
              padding: '15px',
              fontSize: '1.1rem',
              fontWeight: '600',
              backgroundColor: Object.keys(selectedSymptoms).length === 0 ? '#9CA3AF' : '#3B82F6',
              cursor: Object.keys(selectedSymptoms).length === 0 ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Analyzing Symptoms...' : `Get Recommendations (${Object.keys(selectedSymptoms).length} symptoms)`}
          </button>
        </form>
        {/* Follow-up Questions */}
        {showFollowUp && (
          <FollowUpQuestions
            selectedSymptoms={selectedSymptoms}
            onAnswersChange={handleFollowUpAnswers}
            onComplete={handleFollowUpComplete}
          />
        )}

        <EnhancedResults result={result} selectedSymptoms={selectedSymptoms} />
      </div>
    </div>
  );
}

export default Home;
