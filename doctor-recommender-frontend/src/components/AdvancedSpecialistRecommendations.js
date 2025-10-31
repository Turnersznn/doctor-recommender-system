import React, { useState } from 'react';
import './AdvancedSpecialistRecommendations.css';

const AdvancedSpecialistRecommendations = ({ specialistRecommendations }) => {
  const [expandedRecommendation, setExpandedRecommendation] = useState(null);

  if (!specialistRecommendations || !specialistRecommendations.recommendations) {
    return null;
  }

  const { recommendations, urgencyLevel, overallAdvice } = specialistRecommendations;

  const getUrgencyColor = (urgency) => {
    switch (urgency) {
      case 'urgent': return '#DC2626';
      case 'semi-urgent': return '#D97706';
      case 'moderate': return '#059669';
      default: return '#3B82F6';
    }
  };

  const getUrgencyIcon = (urgency) => {
    switch (urgency) {
      case 'urgent': return '🚨';
      case 'semi-urgent': return '⚠️';
      case 'moderate': return '🟡';
      default: return '🟢';
    }
  };

  const getPriorityBadge = (priority) => {
    const badges = {
      1: { label: 'Primary Care', color: '#3B82F6' },
      2: { label: 'General Medicine', color: '#059669' },
      3: { label: 'Specialist', color: '#8B5CF6' },
      4: { label: 'Advanced Specialist', color: '#DC2626' },
      5: { label: 'Emergency', color: '#EF4444' }
    };
    return badges[priority] || { label: 'Specialist', color: '#6B7280' };
  };

  return (
    <div className="advanced-specialist-recommendations">
      {/* Urgency Alert */}
      {urgencyLevel === 'urgent' && (
        <div className="urgency-alert urgent">
          <div className="alert-header">
            <span className="alert-icon">🚨</span>
            <h3>Urgent Medical Attention Required</h3>
          </div>
          <p>Your symptoms suggest a condition that requires immediate medical care. Please seek emergency medical attention.</p>
        </div>
      )}

      {urgencyLevel === 'semi-urgent' && (
        <div className="urgency-alert semi-urgent">
          <div className="alert-header">
            <span className="alert-icon">⚠️</span>
            <h3>Prompt Medical Attention Recommended</h3>
          </div>
          <p>Your symptoms warrant medical evaluation within the next few days.</p>
        </div>
      )}

      {/* Section Header */}
      <div className="section-header">
        <h3 className="section-title">
          <span className="section-icon">👨‍⚕️</span>
          Specialist Recommendations
        </h3>
        <div className="urgency-indicator">
          <span className="urgency-icon">{getUrgencyIcon(urgencyLevel)}</span>
          <span className="urgency-text" style={{ color: getUrgencyColor(urgencyLevel) }}>
            {urgencyLevel.charAt(0).toUpperCase() + urgencyLevel.slice(1)} Priority
          </span>
        </div>
      </div>

      {/* Recommendations List */}
      <div className="recommendations-list">
        {recommendations.map((rec, index) => {
          const priorityBadge = getPriorityBadge(rec.priority);
          const isExpanded = expandedRecommendation === index;

          return (
            <div 
              key={index} 
              className={`recommendation-card ${isExpanded ? 'expanded' : ''}`}
              onClick={() => setExpandedRecommendation(isExpanded ? null : index)}
            >
              <div className="recommendation-header">
                <div className="rank-badge">#{rec.rank}</div>
                
                <div className="specialist-info">
                  <h4 className="specialist-name">{rec.specialist}</h4>
                  <p className="specialist-description">{rec.description}</p>
                  
                  <div className="badges-row">
                    <span 
                      className="priority-badge"
                      style={{ backgroundColor: priorityBadge.color }}
                    >
                      {priorityBadge.label}
                    </span>
                    
                    {rec.urgency !== 'routine' && (
                      <span 
                        className="urgency-badge"
                        style={{ backgroundColor: getUrgencyColor(rec.urgency) }}
                      >
                        {getUrgencyIcon(rec.urgency)} {rec.urgency}
                      </span>
                    )}
                    
                    {rec.confidenceLevel && (
                      <span className={`confidence-badge ${rec.confidenceLevel.toLowerCase()}`}>
                        {rec.confidenceLevel} Confidence
                      </span>
                    )}
                  </div>
                </div>

                <div className="expand-toggle">
                  {isExpanded ? '▼' : '▶'}
                </div>
              </div>

              {isExpanded && (
                <div className="recommendation-details">
                  {/* Reasoning */}
                  <div className="detail-section">
                    <h5>Why this specialist?</h5>
                    <p>{rec.reasoning}</p>
                  </div>

                  {/* Timeline */}
                  <div className="detail-section">
                    <h5>Recommended Timeline</h5>
                    <div className="timeline-info">
                      <span className="timeline-text">{rec.timeline}</span>
                    </div>
                  </div>

                  {/* Expertise */}
                  {rec.expertise && rec.expertise.length > 0 && (
                    <div className="detail-section">
                      <h5>Areas of Expertise</h5>
                      <div className="expertise-tags">
                        {rec.expertise.map((area, idx) => (
                          <span key={idx} className="expertise-tag">{area}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Alternatives */}
                  {rec.alternatives && rec.alternatives.length > 0 && (
                    <div className="detail-section">
                      <h5>Alternative Specialists</h5>
                      <div className="alternatives-list">
                        {rec.alternatives.map((alt, idx) => (
                          <div key={idx} className="alternative-item">
                            <span className="alternative-name">{alt.specialist}</span>
                            <span className="alternative-reason">{alt.reason}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Questions to Ask */}
                  {rec.questions && rec.questions.length > 0 && (
                    <div className="detail-section">
                      <h5>Questions to Ask</h5>
                      <ul className="questions-list">
                        {rec.questions.slice(0, 4).map((question, idx) => (
                          <li key={idx}>{question}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Preparation Advice */}
                  {rec.preparation && rec.preparation.length > 0 && (
                    <div className="detail-section">
                      <h5>How to Prepare</h5>
                      <ul className="preparation-list">
                        {rec.preparation.slice(0, 4).map((item, idx) => (
                          <li key={idx}>{item}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Overall Advice */}
      {overallAdvice && overallAdvice.length > 0 && (
        <div className="overall-advice">
          <h4>Important Reminders</h4>
          <ul>
            {overallAdvice.map((advice, index) => (
              <li key={index}>{advice}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Additional Resources */}
      <div className="additional-resources">
        <h4>Additional Resources</h4>
        <div className="resources-grid">
          <div className="resource-item">
            <h5>🏥 Find Healthcare Providers</h5>
            <p>Use your insurance provider's directory to find specialists in your network.</p>
          </div>
          <div className="resource-item">
            <h5>📞 Telehealth Options</h5>
            <p>Consider virtual consultations for initial assessments when appropriate.</p>
          </div>
          <div className="resource-item">
            <h5>📋 Medical Records</h5>
            <p>Gather relevant medical history and test results before your appointment.</p>
          </div>
          <div className="resource-item">
            <h5>💊 Medication List</h5>
            <p>Prepare a complete list of current medications, supplements, and allergies.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdvancedSpecialistRecommendations;
