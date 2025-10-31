import React, { useState } from 'react';
import './MLEnhancedResults.css';

const MLEnhancedResults = ({ result, selectedSymptoms }) => {
  const [expandedDiagnosis, setExpandedDiagnosis] = useState(null);

  if (!result) return null;

  // Handle error cases
  if (result.error) {
    return (
      <div className="ml-results error-result">
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

  // Handle "not found" cases - when ML model doesn't recognize the symptom combination
  const isNotFound = !result.diagnoses || result.diagnoses.length === 0 || 
    (result.diagnoses.length === 1 && result.diagnoses[0].disease === "General Assessment Needed");

  if (isNotFound) {
    return (
      <div className="ml-results not-found-result">
        <div className="not-found-card">
          <div className="not-found-icon">🤖❓</div>
          <h3>Symptom Combination Not Found</h3>
          <p>Our ML model doesn't recognize this specific combination of symptoms in its training data.</p>
          
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

          <div className="ml-info-card">
            <div className="ml-icon">🧠</div>
            <div className="ml-details">
              <h4>About Our ML Model:</h4>
              <p>Trained on <strong>5,787 medical records</strong> with <strong>131 symptoms</strong>, 
                 <strong>41 diseases</strong>, and <strong>17 specialists</strong></p>
              <div className="accuracy-stats">
                <span className="stat">96.3% Disease Accuracy</span>
                <span className="stat">97.2% Specialist Accuracy</span>
              </div>
            </div>
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

  // Calculate selected symptoms info
  const selectedSymptomsCount = Object.keys(selectedSymptoms).length;
  const symptomsWithSeverity = Object.values(selectedSymptoms).filter(
    val => typeof val === 'object' && val.severity
  ).length;

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#10B981'; // Green
    if (confidence >= 0.6) return '#F59E0B'; // Yellow
    return '#EF4444'; // Red
  };

  const getProbabilityColor = (probability) => {
    if (probability >= 0.7) return '#10B981';
    if (probability >= 0.4) return '#F59E0B';
    return '#EF4444';
  };

  return (
    <div className="ml-results">
      {/* ML-Powered Header */}
      <div className="results-header">
        <div className="header-icon">🤖</div>
        <div className="header-content">
          <h2>ML-Powered Analysis Results</h2>
          <div className="analysis-summary">
            <span className="symptom-count">
              {selectedSymptomsCount} symptom{selectedSymptomsCount !== 1 ? 's' : ''} analyzed
            </span>
            {result.ml_powered && (
              <span className="ml-powered-badge">
                <span className="ml-badge-icon">🧠</span>
                ML-Powered
              </span>
            )}
          </div>
        </div>
      </div>

      {/* ML Model Info */}
      {result.model_info && (
        <div className="ml-model-info">
          <div className="model-stats">
            <div className="stat-item">
              <span className="stat-label">Disease Model:</span>
              <span className="stat-value">{result.model_info.disease_model}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Specialist Model:</span>
              <span className="stat-value">{result.model_info.specialist_model}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Features Used:</span>
              <span className="stat-value">{result.model_info.active_features}/{result.model_info.total_features}</span>
            </div>
          </div>
        </div>
      )}

      {/* Diagnoses Section */}
      {result.diagnoses && result.diagnoses.length > 0 && (
        <div className="diagnoses-section">
          <h3 className="section-title">
            <span className="section-icon">🔍</span>
            ML Predictions
          </h3>
          
          <div className="diagnoses-grid">
            {result.diagnoses.map((diagnosis, index) => (
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
                        {(diagnosis.probability * 100).toFixed(1)}% probability
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
                      <h5>👨‍⚕️ Recommended Specialist:</h5>
                      <div className="specialist-name">{diagnosis.specialist}</div>
                      <div 
                        className="confidence-badge"
                        style={{ backgroundColor: getConfidenceColor(diagnosis.confidence) }}
                      >
                        {(diagnosis.confidence * 100).toFixed(1)}% confidence
                      </div>
                    </div>

                    {diagnosis.explanation && (
                      <div className="explanation">
                        <h5>📋 ML Analysis:</h5>
                        <p>{diagnosis.explanation}</p>
                      </div>
                    )}

                    {diagnosis.ml_disease_confidence !== undefined && (
                      <div className="ml-confidence-breakdown">
                        <h5>🧠 ML Confidence Breakdown:</h5>
                        <div className="confidence-items">
                          <div className="confidence-item">
                            <span>Disease Prediction:</span>
                            <span>{(diagnosis.ml_disease_confidence * 100).toFixed(1)}%</span>
                          </div>
                          <div className="confidence-item">
                            <span>Specialist Prediction:</span>
                            <span>{(diagnosis.ml_specialist_confidence * 100).toFixed(1)}%</span>
                          </div>
                        </div>
                      </div>
                    )}

                    {diagnosis.matching_symptoms && (
                      <div className="matching-symptoms">
                        <h5>✅ Matching Symptoms:</h5>
                        <div className="symptom-list">
                          {diagnosis.matching_symptoms.map((symptom, idx) => (
                            <span key={idx} className="matched-symptom">
                              {symptom.replace(/_/g, ' ')}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Primary Recommendation */}
      {result.predicted_specialist && (
        <div className="primary-recommendation">
          <h3 className="section-title">
            <span className="section-icon">🎯</span>
            Primary ML Recommendation
          </h3>
          <div className="primary-card">
            <div className="specialist-avatar">👨‍⚕️</div>
            <div className="specialist-details">
              <h4>{result.predicted_specialist}</h4>
              <div className="confidence-display">
                <div 
                  className="confidence-bar"
                  style={{ 
                    width: `${result.confidence * 100}%`,
                    backgroundColor: getConfidenceColor(result.confidence)
                  }}
                />
                <span className="confidence-text">
                  {(result.confidence * 100).toFixed(1)}% ML confidence
                </span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MLEnhancedResults;
