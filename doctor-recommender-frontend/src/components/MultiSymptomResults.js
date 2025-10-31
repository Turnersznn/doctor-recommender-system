import React, { useState } from 'react';
import './EnhancedResults.css'; // Reusing existing CSS

const MultiSymptomResults = ({ result }) => {
  const [expandedDiagnosis, setExpandedDiagnosis] = useState(null);

  if (!result) return null;

  // Handle error case
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

  // Helper functions for styling
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
    if (probability >= 0.8) return '#10B981'; // Green
    if (probability >= 0.5) return '#3B82F6'; // Blue
    if (probability >= 0.3) return '#F59E0B'; // Yellow
    return '#EF4444'; // Red
  };

  return (
    <div className="enhanced-results">
      {/* Results Header */}
      <div className="results-header">
        <div className="header-icon">🩺</div>
        <div className="header-content">
          <h2>Multi-Symptom Analysis Results</h2>
          <div className="analysis-summary">
            <div className="symptom-count">
              {result.active_symptoms?.length || 0} Symptoms Analyzed
            </div>
          </div>
        </div>
      </div>

      {/* Diagnoses Section */}
      <div className="diagnoses-section">
        <h3 className="section-title">
          <span className="section-icon">🔍</span>
          Potential Diagnoses
        </h3>
        
        <div className="diagnoses-grid">
          {result.diagnoses?.map((diagnosis, index) => (
            <div
              key={index}
              className={`diagnosis-card ${expandedDiagnosis === index ? 'expanded' : ''}`}
              onClick={() => setExpandedDiagnosis(expandedDiagnosis === index ? null : index)}
            >
              <div className="diagnosis-header">
                <div className="diagnosis-rank">#{index + 1}</div>
                <div className="diagnosis-main">
                  <h4 className="diagnosis-name">{diagnosis.disease}</h4>
                  <div className="probability-bar">
                    <div 
                      className="probability-fill"
                      style={{ 
                        width: `${diagnosis.probability * 100}%`,
                        backgroundColor: getProbabilityColor(diagnosis.probability)
                      }}
                    />
                    <span className="probability-text">
                      {(diagnosis.probability * 100).toFixed(1)}% match
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

                  {diagnosis.matching_symptoms && diagnosis.matching_symptoms.length > 0 && (
                    <div className="explanation">
                      <h6>Matching Symptoms</h6>
                      <p>{diagnosis.matching_symptoms.join(', ')}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Primary Specialist Recommendation */}
      <div className="diagnoses-section">
        <h3 className="section-title">
          <span className="section-icon">👨‍⚕️</span>
          Primary Specialist Recommendation
        </h3>
        
        <div className="recommendation-card expanded">
          <div className="diagnosis-header">
            <div className="diagnosis-rank">1</div>
            <div className="diagnosis-main">
              <h4 className="diagnosis-name">{result.predicted_specialist}</h4>
              <div className="probability-bar">
                <div 
                  className="probability-fill"
                  style={{ 
                    width: `${result.confidence * 100}%`,
                    backgroundColor: getProbabilityColor(result.confidence)
                  }}
                />
                <span className="probability-text">
                  {(result.confidence * 100).toFixed(1)}% confidence
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Symptoms Section */}
      <div className="diagnoses-section">
        <h3 className="section-title">
          <span className="section-icon">🤒</span>
          Analyzed Symptoms
        </h3>
        
        <div className="analysis-metadata">
          <div className="metadata-grid">
            {result.active_symptoms?.map((symptom, index) => (
              <div key={index} className="metadata-item">
                <span className="metadata-label">{symptom.replace('_', ' ')}</span>
                <span className="metadata-value">Active</span>
              </div>
            ))}
          </div>
        </div>
      </div>

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

export default MultiSymptomResults;