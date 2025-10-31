import React, { useState } from 'react';
import DoctorRating from './DoctorRating';
import FavoriteButton from './FavoriteButton';
import './EnhancedResults.css';

const EnhancedResults = ({ result, selectedSymptoms }) => {
  const [expandedDiagnosis, setExpandedDiagnosis] = useState(null);

  if (!result) return null;

  if (result.error) {
    return (
      <div className="enhanced-results error-result">
        <div className="error-card">
          <div className="error-icon">⚠️</div>
          <h3>Unable to Process Request</h3>
          <p>{result.error}</p>
          <div className="error-suggestions">
            <h4>Suggestions:</h4>
            <ul>
              <li>Make sure you've selected at least one symptom</li>
              <li>Check your internet connection</li>
              <li>Try refreshing the page</li>
            </ul>
          </div>
        </div>
      </div>
    );
  }

  // Handle "not found" cases - when the model doesn't recognize the symptom combination
  const isNotFound = !result.diagnoses || result.diagnoses.length === 0 ||
    (result.diagnoses.length === 1 && result.diagnoses[0].disease === "General Assessment Needed");

  if (isNotFound) {
    return (
      <div className="enhanced-results not-found-result">
        <div className="not-found-card">
          <div className="not-found-icon">🔍</div>
          <h3>Symptom Combination Not Found</h3>
          <p>We couldn't find a specific match for this combination of symptoms in our database.</p>

          <div className="selected-symptoms-display">
            <h4>Your Selected Symptoms:</h4>
            <div className="symptom-tags">
              {Object.keys(selectedSymptoms).map(symptom => (
                <span key={symptom} className="symptom-tag">
                  {symptom.replace(/_/g, ' ')}
                </span>
              ))}
            </div>
          </div>

          <div className="suggestions-card">
            <h4>💡 Try These Suggestions:</h4>
            <ul>
              <li><strong>Modify your selection:</strong> Try removing or adding symptoms</li>
              <li><strong>Use common symptom names:</strong> e.g., "headache" instead of "head pain"</li>
              <li><strong>Try fewer symptoms:</strong> Start with 1-3 main symptoms</li>
              <li><strong>Check spelling:</strong> Make sure symptoms are spelled correctly</li>
            </ul>
          </div>

          <div className="fallback-recommendation">
            <h4>🏥 General Recommendation:</h4>
            <p>For these symptoms, we recommend starting with a <strong>General Practitioner</strong>
               who can provide initial assessment and refer you to the appropriate specialist if needed.</p>
          </div>
        </div>
      </div>
    );
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#10B981'; // Green
    if (confidence >= 0.6) return '#F59E0B'; // Yellow
    return '#EF4444'; // Red
  };

  const getConfidenceLabel = (confidence) => {
    if (confidence >= 0.8) return 'High Confidence';
    if (confidence >= 0.6) return 'Moderate Confidence';
    return 'Low Confidence';
  };

  const getProbabilityColor = (probability) => {
    if (probability >= 0.7) return '#3B82F6'; // Blue
    if (probability >= 0.4) return '#8B5CF6'; // Purple
    return '#6B7280'; // Gray
  };

  const getSpecialistIcon = (specialist) => {
    const icons = {
      'Dermatologist': '🧴',
      'Cardiologist': '❤️',
      'Pulmonologist': '🫁',
      'Neurologist': '🧠',
      'Gastroenterologist': '🍽️',
      'Orthopedist': '🦴',
      'Endocrinologist': '⚖️',
      'Ophthalmologist': '👁️',
      'ENT': '👂',
      'Psychiatrist': '🧘',
      'Urologist': '🩺',
      'Gynecologist': '👩‍⚕️',
      'Pediatrician': '👶',
      'General Practitioner': '👨‍⚕️',
      'Internal Medicine': '🏥',
      'Rheumatologist': '🦴',
      'Hepatologist': '🫀'
    };
    return icons[specialist] || '👨‍⚕️';
  };

  const getSpecialistDescription = (specialist) => {
    const descriptions = {
      'Dermatologist': 'Specializes in skin, hair, and nail conditions',
      'Cardiologist': 'Specializes in heart and cardiovascular diseases',
      'Pulmonologist': 'Specializes in lung and respiratory conditions',
      'Neurologist': 'Specializes in nervous system disorders',
      'Gastroenterologist': 'Specializes in digestive system disorders',
      'Orthopedist': 'Specializes in bone, joint, and muscle conditions',
      'Endocrinologist': 'Specializes in hormone and metabolic disorders',
      'Ophthalmologist': 'Specializes in eye and vision conditions',
      'ENT': 'Specializes in ear, nose, and throat conditions',
      'General Practitioner': 'Provides comprehensive primary healthcare',
      'Internal Medicine': 'Specializes in adult internal medicine',
      'Rheumatologist': 'Specializes in joint and autoimmune conditions',
      'Hepatologist': 'Specializes in liver and biliary system disorders'
    };
    return descriptions[specialist] || 'Medical specialist';
  };

  // Rule-based disease mapping to fix "Condition requiring..." messages
  const getRealDiseases = (symptoms) => {
    const rules = {
      'skin_rash,itching': {disease: 'Eczema', confidence: 0.75},
      'cough,fever': {disease: 'Common Cold', confidence: 0.7},
      'headache,fever': {disease: 'Viral Infection', confidence: 0.7},
      'stomach_pain,nausea': {disease: 'Gastroenteritis', confidence: 0.8},
      'chest_pain,shortness_of_breath': {disease: 'Heart Disease', confidence: 0.8},
      'headache,dizziness': {disease: 'Migraine', confidence: 0.75},
      'joint_pain,stiffness': {disease: 'Arthritis', confidence: 0.8}
    };

    if (!symptoms || symptoms.length < 2) return null;

    const symptomKey = symptoms.slice(0, 2).sort().join(',');
    const result = rules[symptomKey];

    // FIXED: Ensure confidence is always a valid number
    if (result && result.confidence) {
      const conf = parseFloat(result.confidence);
      if (isNaN(conf) || conf < 0 || conf > 1) {
        result.confidence = 0.7; // Safe fallback
      }
    }

    return result || null;
  };

  const selectedSymptomsCount = Object.keys(selectedSymptoms).length;
  const symptomsWithSeverity = Object.entries(selectedSymptoms).filter(
    ([_, value]) => typeof value === 'object' && value.severity
  ).length;

  return (
    <div className="enhanced-results">
      {/* Summary Header */}
      <div className="results-header">
        <div className="header-icon">🔬</div>
        <div className="header-content">
          <h2>Medical Analysis Results</h2>
          <div className="analysis-summary">
            <span className="symptom-count">
              {selectedSymptomsCount} symptom{selectedSymptomsCount !== 1 ? 's' : ''} analyzed
            </span>
            {symptomsWithSeverity > 0 && (
              <span className="severity-count">
                {symptomsWithSeverity} with severity levels
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Likely Diseases Section */}
      {result.diagnoses && result.diagnoses.length > 0 && (
        <div className="diagnoses-section">
          <h3 className="section-title">
            <span className="section-icon">🦠</span>
            Likely Diseases
          </h3>
          <p className="section-description">
            Based on your symptoms, here are the most probable conditions:
          </p>
          
          <div className="diagnoses-grid">
            {result.diagnoses.map((diagnosis, index) => {
              // FIXED: Robust confidence handling to prevent NaN
              let displayDisease = diagnosis.disease;
              let displayConfidence = 0.5; // Default fallback

              // Helper function to safely parse confidence values
              const safeParseConfidence = (value) => {
                if (value === null || value === undefined) return null;
                const parsed = parseFloat(value);
                if (isNaN(parsed) || parsed < 0 || parsed > 1) return null;
                return parsed;
              };

              // Try to get confidence from multiple sources
              const probConfidence = safeParseConfidence(diagnosis.probability);
              const confConfidence = safeParseConfidence(diagnosis.confidence);

              if (probConfidence !== null) {
                displayConfidence = probConfidence;
              } else if (confConfidence !== null) {
                displayConfidence = confConfidence;
              }

              // Debug log to see what we're getting
              console.log('🔍 Confidence debug:', {
                disease: displayDisease,
                originalProb: diagnosis.probability,
                originalConf: diagnosis.confidence,
                parsedProb: probConfidence,
                parsedConf: confConfidence,
                finalConfidence: displayConfidence
              });

              // Handle "Condition requiring..." fallback (but preserve confidence validation)
              if (diagnosis.disease && diagnosis.disease.includes('Condition requiring')) {
                const realDisease = getRealDiseases(result.active_symptoms);
                if (realDisease) {
                  displayDisease = realDisease.disease;
                  // FIXED: Safely parse the real disease confidence too
                  const realConfidence = safeParseConfidence(realDisease.confidence);
                  if (realConfidence !== null) {
                    displayConfidence = realConfidence;
                  }
                }
              }

              return (
                <div
                  key={index}
                  className={`diagnosis-card ${expandedDiagnosis === index ? 'expanded' : ''}`}
                  onClick={() => setExpandedDiagnosis(expandedDiagnosis === index ? null : index)}
                >
                  <div className="diagnosis-header">
                    <div className={`diagnosis-rank ${index === 0 ? 'primary' : ''}`}>#{index + 1}</div>
                    <div className="diagnosis-main">
                      <h4 className="diagnosis-name">{displayDisease}</h4>
                      <div className="probability-display">
                        <div className="probability-bar">
                          <div
                            className="probability-fill"
                            style={{
                              width: `${(() => {
                                // Safe width calculation
                                if (displayConfidence === null || displayConfidence === undefined || isNaN(displayConfidence)) {
                                  return 50;
                                }
                                const width = displayConfidence * 100;
                                return isNaN(width) ? 50 : Math.max(0, Math.min(100, width));
                              })()}%`,
                              backgroundColor: index === 0 ? '#10B981' : index === 1 ? '#F59E0B' : '#6B7280'
                            }}
                          />
                        </div>
                        <span className="probability-text">
                          {(() => {
                            // Triple-safe percentage calculation
                            if (displayConfidence === null || displayConfidence === undefined || isNaN(displayConfidence)) {
                              return '50.0';
                            }
                            const percentage = displayConfidence * 100;
                            if (isNaN(percentage)) {
                              return '50.0';
                            }
                            return percentage.toFixed(1);
                          })()}% likelihood
                        </span>
                      </div>
                  </div>
                  <div className="expand-icon">
                    {expandedDiagnosis === index ? '▼' : '▶'}
                  </div>
                </div>

                {expandedDiagnosis === index && (
                  <div className="diagnosis-details">
                    <div className="specialist-info">
                      <h5>Recommended Specialist</h5>
                      <div className="primary-specialist">
                        <span className="specialist-badge primary">
                          {diagnosis.specialist}
                        </span>
                        {diagnosis.confidence && (
                          <div className="confidence-indicator">
                            <div 
                              className="confidence-bar"
                              style={{ backgroundColor: getConfidenceColor(diagnosis.confidence) }}
                            />
                            <span className="confidence-label">
                              {getConfidenceLabel(diagnosis.confidence)}
                            </span>
                          </div>
                        )}
                      </div>
                      
                      {diagnosis.alternative_specialists && diagnosis.alternative_specialists.length > 0 && (
                        <div className="alternative-specialists">
                          <h6>Alternative Specialists</h6>
                          <div className="specialist-list">
                            {diagnosis.alternative_specialists.map((specialist, idx) => (
                              <span key={idx} className="specialist-badge alternative">
                                {specialist}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>

                    {diagnosis.explanation && (
                      <div className="explanation">
                        <h6>Why this specialist?</h6>
                        <p>{diagnosis.explanation}</p>
                      </div>
                    )}

                    {diagnosis.recommendations && diagnosis.recommendations.length > 0 && (
                      <div className="recommendations">
                        <h6>Recommended Actions</h6>
                        <div className="recommendation-list">
                          {diagnosis.recommendations.map((rec, idx) => (
                            <div key={idx} className={`recommendation-item ${rec.priority}`}>
                              <div className="recommendation-priority">
                                {rec.priority === 'urgent' && '🔴'}
                                {rec.priority === 'important' && '🟡'}
                                {rec.priority === 'optional' && '🟢'}
                                {rec.priority === 'general' && 'ℹ️'}
                                {rec.priority === 'monitor' && '👁️'}
                              </div>
                              <div className="recommendation-content">
                                <div className="recommendation-action">{rec.action}</div>
                                <div className="recommendation-reason">{rec.reason}</div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Primary Specialist Recommendation */}
      {result.predicted_specialist && (
        <div className="specialist-recommendation">
          <h3 className="section-title">
            <span className="section-icon">👨‍⚕️</span>
            Recommended Specialist
          </h3>
          <p className="section-description">
            Based on the analysis, we recommend consulting with:
          </p>
          <div className="primary-specialist-card">
            <div className="specialist-avatar">
              {getSpecialistIcon(result.predicted_specialist)}
            </div>
            <div className="specialist-details">
              <h4 className="specialist-name">{result.predicted_specialist}</h4>
              <p className="specialist-description">
                {getSpecialistDescription(result.predicted_specialist)}
              </p>
              <div className="confidence-display">
                <div className="confidence-bar">
                  <div
                    className="confidence-fill"
                    style={{
                      width: `${(() => {
                        const conf = result.confidence || 0.6;
                        const width = parseFloat(conf) * 100;
                        return isNaN(width) ? 60 : Math.max(0, Math.min(100, width));
                      })()}%`,
                      backgroundColor: getConfidenceColor(result.confidence || 0.6)
                    }}
                  />
                </div>
                <span className="confidence-text">
                  {(() => {
                    const conf = result.confidence || 0.6;
                    const percentage = parseFloat(conf) * 100;
                    return isNaN(percentage) ? '60.0' : percentage.toFixed(1);
                  })()}% confidence
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Alternative Specialists */}
      {result.disease_based_specialists && result.disease_based_specialists.length > 1 && (
        <div className="alternative-specialists">
          <h3 className="section-title">
            <span className="section-icon">🏥</span>
            Alternative Specialists
          </h3>
          <p className="section-description">
            You may also consider consulting with these specialists:
          </p>
          <div className="specialists-grid">
            {result.disease_based_specialists
              .filter(spec => spec !== result.predicted_specialist)
              .slice(0, 3)
              .map((specialist, index) => (
                <div key={index} className="alt-specialist-card">
                  <div className="alt-specialist-icon">
                    {getSpecialistIcon(specialist)}
                  </div>
                  <div className="alt-specialist-info">
                    <div className="alt-specialist-name">{specialist}</div>
                    <div className="alt-specialist-desc">
                      {getSpecialistDescription(specialist)}
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}

      {/* Confidence Warning */}
      {result.confidence?.showWarning && (
        <div className="confidence-warning">
          <div className="warning-header">
            <span className="warning-icon">⚠️</span>
            <h3>Low Confidence Analysis</h3>
          </div>
          <p>{result.confidence.warningMessage}</p>
          <div className="warning-suggestions">
            <h4>To improve accuracy:</h4>
            <ul>
              <li>Add more specific symptoms if you have them</li>
              <li>Include severity levels for your symptoms</li>
              <li>Consider the duration and triggers of symptoms</li>
              <li>Consult with a healthcare provider for professional assessment</li>
            </ul>
          </div>
        </div>
      )}

      {/* Analysis Metadata */}
      {result.confidence?.analysisMetadata && (
        <div className="analysis-metadata">
          <h4>Analysis Summary</h4>
          <div className="metadata-grid">
            <div className="metadata-item">
              <span className="metadata-label">Total Symptoms:</span>
              <span className="metadata-value">{result.confidence.analysisMetadata.totalSymptoms}</span>
            </div>
            <div className="metadata-item">
              <span className="metadata-label">With Severity:</span>
              <span className="metadata-value">{result.confidence.analysisMetadata.symptomsWithSeverity}</span>
            </div>
            <div className="metadata-item">
              <span className="metadata-label">High Confidence:</span>
              <span className="metadata-value">{result.confidence.analysisMetadata.highConfidenceDiagnoses}</span>
            </div>
            <div className="metadata-item">
              <span className="metadata-label">Moderate Confidence:</span>
              <span className="metadata-value">{result.confidence.analysisMetadata.moderateConfidenceDiagnoses}</span>
            </div>
          </div>
        </div>
      )}

      {/* Recommended Doctors Section */}
      {result.recommendedDoctors && result.recommendedDoctors.length > 0 && (
        <div className="doctors-section">
          <h3 className="section-title">
            <span className="section-icon">👨‍⚕️</span>
            Recommended Doctors
          </h3>
          
          <div className="doctors-grid">
            {result.recommendedDoctors.map((doctor, index) => (
              <div key={index} className="doctor-card">
                <div className="doctor-header">
                  <div className="doctor-avatar">
                    {doctor.name.charAt(0).toUpperCase()}
                  </div>
                  <div className="doctor-info">
                    <h4 className="doctor-name">{doctor.name}</h4>
                    <p className="doctor-specialty">{doctor.specialty}</p>
                    <p className="doctor-location">📍 {doctor.location}</p>
                  </div>
                </div>
                
                <div className="doctor-details">
                  {doctor.experience && (
                    <div className="detail-item">
                      <span className="detail-label">Experience:</span>
                      <span className="detail-value">{doctor.experience} years</span>
                    </div>
                  )}
                  
                  <div className="detail-item">
                    <span className="detail-label">Rating:</span>
                    <DoctorRating doctor={doctor} />
                  </div>
                  
                  {doctor.availability && (
                    <div className="detail-item">
                      <span className="detail-label">Available:</span>
                      <span className="detail-value">{doctor.availability}</span>
                    </div>
                  )}
                </div>
                
                <div className="doctor-actions">
                  <FavoriteButton doctor={doctor} />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Additional Information */}
      <div className="additional-info">
        <div className="info-card">
          <h4>⚠️ Important Disclaimer</h4>
          <p>
            This analysis is for informational purposes only and should not replace professional medical advice. 
            Please consult with a qualified healthcare provider for proper diagnosis and treatment.
          </p>
        </div>
        
        <div className="info-card">
          <h4>📋 Next Steps</h4>
          <ul>
            <li>Schedule an appointment with the recommended specialist</li>
            <li>Prepare a list of your symptoms and their duration</li>
            <li>Bring any relevant medical history or test results</li>
            <li>Consider getting a second opinion for serious conditions</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default EnhancedResults;
