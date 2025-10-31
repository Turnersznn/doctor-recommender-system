import React, { useState, useMemo, useEffect } from 'react';
import {
  SYMPTOM_CATEGORIES,
  SEVERITY_LEVELS,
  getSymptomDisplayName,
  organizeSymptomsByCategory
} from '../data/symptomCategories';
import { fetchAvailableSymptoms, transformSymptomsForFrontend } from '../services/symptomService';
import './EnhancedSymptomSelector.css';

const EnhancedSymptomSelector = ({
  selectedSymptoms,
  onSymptomsChange,
  availableSymptoms = []
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [showSeverity, setShowSeverity] = useState(false);
  const [backendSymptoms, setBackendSymptoms] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Use hardcoded symptoms instead of backend fetch
  useEffect(() => {
    setLoading(false);
    setBackendSymptoms(null);
  }, []);

  // Organize symptoms by category
  const organizedSymptoms = useMemo(() => {
    // Priority: 1. Backend symptoms, 2. Passed availableSymptoms, 3. Fallback to hardcoded
    if (backendSymptoms && backendSymptoms.length > 0) {
      console.log('🎯 Using backend symptoms:', backendSymptoms.length);
      return transformSymptomsForFrontend(backendSymptoms);
    } else if (availableSymptoms.length > 0) {
      console.log('🔄 Using passed availableSymptoms:', availableSymptoms.length);
      return organizeSymptomsByCategory(availableSymptoms);
    } else {
      console.log('⚠️ Using fallback hardcoded symptoms');
      console.log('SYMPTOM_CATEGORIES:', SYMPTOM_CATEGORIES);
      const allSymptoms = Object.values(SYMPTOM_CATEGORIES).flatMap(cat => cat.symptoms);
      console.log('All symptoms:', allSymptoms);
      return organizeSymptomsByCategory(allSymptoms);
    }
  }, [backendSymptoms, availableSymptoms]);

  // Filter symptoms based on search and category
  const filteredCategories = useMemo(() => {
    const filtered = {};
    
    Object.entries(organizedSymptoms).forEach(([categoryName, categoryData]) => {
      if (selectedCategory !== 'All' && selectedCategory !== categoryName) {
        return;
      }
      
      const filteredSymptoms = categoryData.symptoms.filter(symptom => {
        const displayName = getSymptomDisplayName(symptom);
        return displayName.toLowerCase().includes(searchTerm.toLowerCase()) ||
               symptom.toLowerCase().includes(searchTerm.toLowerCase());
      });
      
      if (filteredSymptoms.length > 0) {
        filtered[categoryName] = {
          ...categoryData,
          symptoms: filteredSymptoms
        };
      }
    });
    
    return filtered;
  }, [organizedSymptoms, searchTerm, selectedCategory]);

  const handleSymptomToggle = (symptom) => {
    const newSymptoms = { ...selectedSymptoms };
    
    if (newSymptoms[symptom]) {
      delete newSymptoms[symptom];
    } else {
      newSymptoms[symptom] = showSeverity ? { selected: true, severity: 'moderate' } : true;
    }
    
    onSymptomsChange(newSymptoms);
  };

  const handleSeverityChange = (symptom, severity) => {
    const newSymptoms = { ...selectedSymptoms };
    if (newSymptoms[symptom]) {
      if (typeof newSymptoms[symptom] === 'object') {
        newSymptoms[symptom].severity = severity;
      } else {
        newSymptoms[symptom] = { selected: true, severity };
      }
      onSymptomsChange(newSymptoms);
    }
  };

  const isSymptomSelected = (symptom) => {
    return !!selectedSymptoms[symptom];
  };

  const getSymptomSeverity = (symptom) => {
    const symptomData = selectedSymptoms[symptom];
    if (typeof symptomData === 'object' && symptomData.severity) {
      return symptomData.severity;
    }
    return 'moderate';
  };

  const selectedCount = Object.keys(selectedSymptoms).length;

  // Show loading state
  if (loading) {
    return (
      <div className="enhanced-symptom-selector">
        <div className="selector-header">
          <h3>Loading Symptoms...</h3>
          <p className="selector-description">
            🔄 Fetching available symptoms from backend...
          </p>
        </div>
        <div className="loading-spinner" style={{ textAlign: 'center', padding: '2rem' }}>
          <div style={{ fontSize: '2rem' }}>⏳</div>
          <p>Loading symptoms...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="enhanced-symptom-selector">
      <div className="selector-header">
        <h3>Select Your Symptoms</h3>
        <div className="selected-count">
          {selectedCount} symptom{selectedCount !== 1 ? 's' : ''} selected
          {backendSymptoms && (
            <span style={{ color: '#10B981', fontSize: '0.8rem', marginLeft: '0.5rem' }}>
              ✅ {backendSymptoms.length} backend symptoms loaded
            </span>
          )}
        </div>
      </div>

      <div className="selector-controls">
        <div className="search-container">
          <input
            type="text"
            placeholder="Search symptoms..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="symptom-search"
          />
        </div>

        <div className="category-filter">
          <select 
            value={selectedCategory} 
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="category-select"
          >
            <option value="All">All Categories</option>
            {Object.keys(organizedSymptoms).map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>

        <div className="severity-toggle">
          <label>
            <input
              type="checkbox"
              checked={showSeverity}
              onChange={(e) => setShowSeverity(e.target.checked)}
            />
            Include severity levels
          </label>
        </div>
      </div>

      <div className="symptom-categories">
        {Object.entries(filteredCategories).map(([categoryName, categoryData]) => (
          <div key={categoryName} className="symptom-category">
            <div className="category-header">
              <span className="category-icon">{categoryData.icon}</span>
              <h4 className="category-title" style={{ color: categoryData.color }}>
                {categoryName}
              </h4>
              <span className="category-count">
                ({categoryData.symptoms.length})
              </span>
            </div>

            <div className="symptoms-grid">
              {categoryData.symptoms.map(symptom => (
                <div key={symptom} className="symptom-item">
                  <label className={`symptom-label ${isSymptomSelected(symptom) ? 'selected' : ''}`}>
                    <input
                      type="checkbox"
                      checked={isSymptomSelected(symptom)}
                      onChange={() => handleSymptomToggle(symptom)}
                      className="symptom-checkbox"
                    />
                    <span className="symptom-name">
                      {getSymptomDisplayName(symptom)}
                    </span>
                  </label>

                  {showSeverity && isSymptomSelected(symptom) && (
                    <div className="severity-selector">
                      {Object.entries(SEVERITY_LEVELS).map(([level, levelData]) => (
                        <button
                          key={level}
                          className={`severity-btn ${getSymptomSeverity(symptom) === level ? 'active' : ''}`}
                          style={{ 
                            backgroundColor: getSymptomSeverity(symptom) === level ? levelData.color : 'transparent',
                            borderColor: levelData.color,
                            color: getSymptomSeverity(symptom) === level ? 'white' : levelData.color
                          }}
                          onClick={() => handleSeverityChange(symptom, level)}
                          title={levelData.description}
                        >
                          {levelData.label}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {selectedCount === 0 && (
        <div className="no-symptoms-message">
          <p>Please select at least one symptom to get recommendations.</p>
        </div>
      )}
    </div>
  );
};

export default EnhancedSymptomSelector;
