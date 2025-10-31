// Confidence Analysis and Threshold Management
export class ConfidenceAnalyzer {
  constructor() {
    this.confidenceThresholds = {
      HIGH: 0.8,
      MODERATE: 0.6,
      LOW: 0.4,
      VERY_LOW: 0.0
    };

    this.symptomWeights = {
      // High-specificity symptoms (strongly indicate specific conditions)
      'chest_pain': 0.9,
      'seizures': 0.95,
      'blurred_and_distorted_vision': 0.85,
      'blood_in_urine': 0.9,
      'abnormal_menstruation': 0.8,
      'burning_micturition': 0.85,
      
      // Moderate-specificity symptoms
      'headache': 0.6,
      'joint_pain': 0.65,
      'back_pain': 0.6,
      'abdominal_pain': 0.7,
      'skin_rash': 0.75,
      
      // Low-specificity symptoms (common across many conditions)
      'fatigue': 0.4,
      'fever': 0.45,
      'nausea': 0.5,
      'dizziness': 0.55,
      'anxiety': 0.5
    };
  }

  analyzeConfidence(diagnoses, selectedSymptoms) {
    return diagnoses.map(diagnosis => {
      const enhancedDiagnosis = { ...diagnosis };
      
      // Calculate symptom-based confidence
      const symptomConfidence = this.calculateSymptomConfidence(selectedSymptoms);
      
      // Calculate prediction confidence based on probability
      const predictionConfidence = this.calculatePredictionConfidence(diagnosis.probability);
      
      // Calculate specialist mapping confidence
      const specialistConfidence = diagnosis.confidence || 0.7;
      
      // Combined confidence score
      const combinedConfidence = (
        symptomConfidence * 0.3 + 
        predictionConfidence * 0.4 + 
        specialistConfidence * 0.3
      );
      
      enhancedDiagnosis.confidence = Math.round(combinedConfidence * 100) / 100;
      enhancedDiagnosis.confidenceLevel = this.getConfidenceLevel(combinedConfidence);
      enhancedDiagnosis.explanation = this.generateExplanation(diagnosis, combinedConfidence, selectedSymptoms);
      enhancedDiagnosis.recommendations = this.generateRecommendations(diagnosis, combinedConfidence);
      
      return enhancedDiagnosis;
    });
  }

  calculateSymptomConfidence(selectedSymptoms) {
    const symptoms = Object.keys(selectedSymptoms);
    if (symptoms.length === 0) return 0.3;
    
    let totalWeight = 0;
    let weightedSum = 0;
    
    symptoms.forEach(symptom => {
      const weight = this.symptomWeights[symptom] || 0.5; // Default weight
      const severityMultiplier = this.getSeverityMultiplier(selectedSymptoms[symptom]);
      
      weightedSum += weight * severityMultiplier;
      totalWeight += 1;
    });
    
    const baseConfidence = weightedSum / totalWeight;
    
    // Bonus for multiple symptoms (more symptoms = higher confidence)
    const symptomCountBonus = Math.min(symptoms.length * 0.05, 0.2);
    
    return Math.min(baseConfidence + symptomCountBonus, 1.0);
  }

  getSeverityMultiplier(symptomValue) {
    if (typeof symptomValue === 'object' && symptomValue.severity) {
      switch (symptomValue.severity) {
        case 'severe': return 1.2;
        case 'moderate': return 1.0;
        case 'mild': return 0.8;
        default: return 1.0;
      }
    }
    return 1.0;
  }

  calculatePredictionConfidence(probability) {
    // Convert probability to confidence score
    if (probability >= 0.8) return 0.9;
    if (probability >= 0.6) return 0.75;
    if (probability >= 0.4) return 0.6;
    if (probability >= 0.2) return 0.45;
    return 0.3;
  }

  getConfidenceLevel(confidence) {
    if (confidence >= this.confidenceThresholds.HIGH) return 'HIGH';
    if (confidence >= this.confidenceThresholds.MODERATE) return 'MODERATE';
    if (confidence >= this.confidenceThresholds.LOW) return 'LOW';
    return 'VERY_LOW';
  }

  generateExplanation(diagnosis, confidence, selectedSymptoms) {
    const symptomCount = Object.keys(selectedSymptoms).length;
    const confidenceLevel = this.getConfidenceLevel(confidence);
    
    let explanation = `Based on your ${symptomCount} symptom${symptomCount !== 1 ? 's' : ''}, `;
    
    switch (confidenceLevel) {
      case 'HIGH':
        explanation += `there is a strong indication that ${diagnosis.disease} could be the cause. `;
        explanation += `The symptoms you've described are highly characteristic of this condition. `;
        explanation += `We recommend consulting with a ${diagnosis.specialist} for proper diagnosis and treatment.`;
        break;
        
      case 'MODERATE':
        explanation += `${diagnosis.disease} is a possible diagnosis that should be considered. `;
        explanation += `Your symptoms align with this condition, though additional evaluation may be needed. `;
        explanation += `A ${diagnosis.specialist} can provide a more definitive assessment.`;
        break;
        
      case 'LOW':
        explanation += `${diagnosis.disease} is one of several possible conditions that could explain your symptoms. `;
        explanation += `While there is some alignment, further investigation is recommended. `;
        explanation += `Consider starting with a consultation with a ${diagnosis.specialist} or General Practitioner.`;
        break;
        
      default:
        explanation += `${diagnosis.disease} is a potential consideration, but the symptom match is not strong. `;
        explanation += `We recommend consulting with a General Practitioner first for a comprehensive evaluation `;
        explanation += `before seeing a specialist.`;
    }
    
    return explanation;
  }

  generateRecommendations(diagnosis, confidence) {
    const confidenceLevel = this.getConfidenceLevel(confidence);
    const recommendations = [];
    
    switch (confidenceLevel) {
      case 'HIGH':
        recommendations.push({
          priority: 'urgent',
          action: `Schedule an appointment with a ${diagnosis.specialist} within 1-2 weeks`,
          reason: 'High symptom match indicates this specialist can provide the most appropriate care'
        });
        recommendations.push({
          priority: 'important',
          action: 'Prepare a detailed symptom timeline and any relevant medical history',
          reason: 'This will help the specialist make an accurate diagnosis'
        });
        break;
        
      case 'MODERATE':
        recommendations.push({
          priority: 'important',
          action: `Consider scheduling with a ${diagnosis.specialist} within 2-4 weeks`,
          reason: 'Moderate confidence suggests this specialist is likely appropriate'
        });
        recommendations.push({
          priority: 'optional',
          action: 'You may also consult with a General Practitioner first',
          reason: 'They can provide initial assessment and referral if needed'
        });
        break;
        
      case 'LOW':
        recommendations.push({
          priority: 'important',
          action: 'Start with a General Practitioner consultation',
          reason: 'Lower confidence suggests a broader evaluation is needed first'
        });
        recommendations.push({
          priority: 'optional',
          action: `Keep ${diagnosis.specialist} as a potential referral option`,
          reason: 'May be relevant depending on GP assessment'
        });
        break;
        
      default:
        recommendations.push({
          priority: 'important',
          action: 'Consult with a General Practitioner for comprehensive evaluation',
          reason: 'Very low confidence requires broad medical assessment'
        });
        recommendations.push({
          priority: 'monitor',
          action: 'Monitor symptoms and seek immediate care if they worsen',
          reason: 'Symptom changes may provide additional diagnostic clues'
        });
    }
    
    // Add general recommendations
    recommendations.push({
      priority: 'general',
      action: 'Keep a symptom diary noting onset, duration, and triggers',
      reason: 'Detailed records help healthcare providers make better diagnoses'
    });
    
    if (confidence < this.confidenceThresholds.MODERATE) {
      recommendations.push({
        priority: 'important',
        action: 'Consider seeking a second opinion if initial consultation is inconclusive',
        reason: 'Multiple perspectives can be valuable for complex cases'
      });
    }
    
    return recommendations;
  }

  shouldShowWarning(diagnoses) {
    // Show warning if all diagnoses have low confidence
    const highConfidenceDiagnoses = diagnoses.filter(d => 
      this.getConfidenceLevel(d.confidence) === 'HIGH' || 
      this.getConfidenceLevel(d.confidence) === 'MODERATE'
    );
    
    return highConfidenceDiagnoses.length === 0;
  }

  generateWarningMessage(selectedSymptoms) {
    const symptomCount = Object.keys(selectedSymptoms).length;
    
    if (symptomCount < 2) {
      return "Consider providing more symptoms for a more accurate analysis. Additional symptoms help improve diagnostic confidence.";
    }
    
    return "The symptoms provided don't strongly point to a specific condition. We recommend consulting with a General Practitioner for a comprehensive evaluation.";
  }
}

export default ConfidenceAnalyzer;
