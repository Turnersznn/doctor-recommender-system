// Advanced Specialist Recommendation System
export class AdvancedSpecialistRecommender {
  constructor() {
    this.specialistHierarchy = {
      // Primary care and general specialists
      'General Practitioner': {
        priority: 1,
        description: 'First point of contact for most health concerns',
        whenToConsult: 'Initial assessment, routine care, referrals',
        expertise: ['General health', 'Preventive care', 'Common conditions'],
        referralPower: 10
      },
      'Family Medicine': {
        priority: 1,
        description: 'Comprehensive care for all ages',
        whenToConsult: 'Family health, ongoing care, health maintenance',
        expertise: ['All-age care', 'Chronic disease management', 'Preventive medicine'],
        referralPower: 10
      },
      'Internal Medicine': {
        priority: 2,
        description: 'Adult medicine and complex conditions',
        whenToConsult: 'Adult health issues, multiple conditions',
        expertise: ['Adult medicine', 'Complex diagnoses', 'Chronic diseases'],
        referralPower: 9
      },

      // Specialized fields
      'Cardiology': {
        priority: 3,
        description: 'Heart and cardiovascular system',
        whenToConsult: 'Heart problems, chest pain, blood pressure issues',
        expertise: ['Heart disease', 'Arrhythmias', 'Hypertension', 'Heart failure'],
        referralPower: 8,
        urgencyIndicators: ['chest_pain', 'palpitations', 'shortness_of_breath']
      },
      'Dermatology': {
        priority: 3,
        description: 'Skin, hair, and nail conditions',
        whenToConsult: 'Skin problems, rashes, moles, hair loss',
        expertise: ['Skin cancer', 'Acne', 'Eczema', 'Psoriasis', 'Cosmetic procedures'],
        referralPower: 7
      },
      'Neurology': {
        priority: 3,
        description: 'Brain and nervous system disorders',
        whenToConsult: 'Headaches, seizures, memory problems, neurological symptoms',
        expertise: ['Stroke', 'Epilepsy', 'Migraines', 'Dementia', 'Multiple sclerosis'],
        referralPower: 8,
        urgencyIndicators: ['seizures', 'severe_headache', 'paralysis']
      },
      'Gastroenterology': {
        priority: 3,
        description: 'Digestive system and liver',
        whenToConsult: 'Stomach problems, digestive issues, liver concerns',
        expertise: ['IBD', 'Liver disease', 'Endoscopy', 'Acid reflux', 'Colon cancer screening'],
        referralPower: 7
      },
      'Pulmonology': {
        priority: 3,
        description: 'Lungs and respiratory system',
        whenToConsult: 'Breathing problems, lung conditions, persistent cough',
        expertise: ['Asthma', 'COPD', 'Lung cancer', 'Sleep apnea', 'Pneumonia'],
        referralPower: 7,
        urgencyIndicators: ['severe_breathlessness', 'chest_pain']
      },
      'Endocrinology': {
        priority: 3,
        description: 'Hormones and metabolism',
        whenToConsult: 'Diabetes, thyroid problems, hormone imbalances',
        expertise: ['Diabetes', 'Thyroid disorders', 'Adrenal disorders', 'Osteoporosis'],
        referralPower: 7
      },
      'Rheumatology': {
        priority: 3,
        description: 'Joints, muscles, and autoimmune conditions',
        whenToConsult: 'Joint pain, arthritis, autoimmune diseases',
        expertise: ['Rheumatoid arthritis', 'Lupus', 'Fibromyalgia', 'Gout'],
        referralPower: 6
      },
      'Orthopedics': {
        priority: 3,
        description: 'Bones, joints, and musculoskeletal system',
        whenToConsult: 'Bone fractures, joint problems, sports injuries',
        expertise: ['Fractures', 'Joint replacement', 'Sports medicine', 'Spine surgery'],
        referralPower: 6
      },
      'Psychiatry': {
        priority: 3,
        description: 'Mental health and psychiatric conditions',
        whenToConsult: 'Depression, anxiety, mental health concerns',
        expertise: ['Depression', 'Anxiety', 'Bipolar disorder', 'Schizophrenia', 'ADHD'],
        referralPower: 8,
        urgencyIndicators: ['severe_depression', 'suicidal_thoughts', 'psychosis']
      },
      'Ophthalmology': {
        priority: 3,
        description: 'Eyes and vision',
        whenToConsult: 'Vision problems, eye pain, eye diseases',
        expertise: ['Cataracts', 'Glaucoma', 'Retinal disorders', 'Eye surgery'],
        referralPower: 6
      },
      'ENT': {
        priority: 3,
        description: 'Ear, nose, and throat',
        whenToConsult: 'Hearing problems, sinus issues, throat problems',
        expertise: ['Hearing loss', 'Sinus surgery', 'Throat cancer', 'Sleep apnea'],
        referralPower: 6
      },
      'Urology': {
        priority: 3,
        description: 'Urinary system and male reproductive health',
        whenToConsult: 'Urinary problems, kidney issues, male health',
        expertise: ['Kidney stones', 'Prostate problems', 'Bladder cancer', 'Erectile dysfunction'],
        referralPower: 6
      },
      'Obstetrics & Gynecology': {
        priority: 3,
        description: 'Women\'s reproductive health',
        whenToConsult: 'Pregnancy, menstrual problems, reproductive health',
        expertise: ['Pregnancy care', 'Gynecologic surgery', 'Fertility', 'Menopause'],
        referralPower: 7
      },
      'Oncology': {
        priority: 4,
        description: 'Cancer diagnosis and treatment',
        whenToConsult: 'Cancer diagnosis, cancer treatment, tumor evaluation',
        expertise: ['Chemotherapy', 'Cancer staging', 'Tumor management', 'Palliative care'],
        referralPower: 9,
        urgencyIndicators: ['unexplained_weight_loss', 'persistent_pain', 'lumps']
      },
      'Emergency Medicine': {
        priority: 5,
        description: 'Urgent and life-threatening conditions',
        whenToConsult: 'Medical emergencies, severe symptoms, life-threatening situations',
        expertise: ['Trauma', 'Acute conditions', 'Life support', 'Emergency procedures'],
        referralPower: 10,
        urgencyIndicators: ['severe_chest_pain', 'difficulty_breathing', 'severe_bleeding']
      }
    };

    this.symptomUrgencyMap = {
      'chest_pain': 'urgent',
      'severe_headache': 'urgent',
      'difficulty_breathing': 'urgent',
      'seizures': 'urgent',
      'severe_bleeding': 'urgent',
      'loss_of_consciousness': 'urgent',
      'severe_abdominal_pain': 'urgent',
      'high_fever': 'semi-urgent',
      'persistent_vomiting': 'semi-urgent',
      'severe_dizziness': 'semi-urgent',
      'blood_in_urine': 'semi-urgent',
      'blood_in_stool': 'semi-urgent'
    };
  }

  generateAdvancedRecommendations(diagnoses, selectedSymptoms, confidence) {
    const recommendations = [];
    
    // Analyze urgency
    const urgencyLevel = this.assessUrgency(selectedSymptoms);
    
    // Generate recommendations for each diagnosis
    diagnoses.forEach((diagnosis, index) => {
      const specialist = diagnosis.specialist;
      const specialistInfo = this.specialistHierarchy[specialist] || this.getGenericSpecialistInfo(specialist);
      
      const recommendation = {
        rank: index + 1,
        specialist: specialist,
        disease: diagnosis.disease,
        probability: diagnosis.probability,
        confidence: diagnosis.confidence,
        confidenceLevel: diagnosis.confidenceLevel,
        urgency: this.calculateSpecialistUrgency(specialist, selectedSymptoms),
        ...specialistInfo,
        reasoning: this.generateReasoning(diagnosis, specialistInfo, selectedSymptoms),
        timeline: this.generateTimeline(diagnosis, urgencyLevel, specialistInfo),
        alternatives: this.generateAlternatives(specialist, diagnosis),
        questions: this.generateQuestionsToAsk(specialist, diagnosis),
        preparation: this.generatePreparationAdvice(specialist, selectedSymptoms)
      };
      
      recommendations.push(recommendation);
    });

    // Add emergency recommendation if needed
    if (urgencyLevel === 'urgent') {
      recommendations.unshift(this.generateEmergencyRecommendation(selectedSymptoms));
    }

    // Add general practitioner recommendation for low confidence
    if (confidence?.showWarning) {
      recommendations.push(this.generateGPRecommendation(selectedSymptoms));
    }

    return {
      recommendations: recommendations.slice(0, 5), // Limit to top 5
      urgencyLevel,
      overallAdvice: this.generateOverallAdvice(recommendations, urgencyLevel, confidence)
    };
  }

  assessUrgency(symptoms) {
    const urgentSymptoms = Object.keys(symptoms).filter(symptom => 
      this.symptomUrgencyMap[symptom] === 'urgent'
    );
    
    const semiUrgentSymptoms = Object.keys(symptoms).filter(symptom => 
      this.symptomUrgencyMap[symptom] === 'semi-urgent'
    );

    if (urgentSymptoms.length > 0) return 'urgent';
    if (semiUrgentSymptoms.length > 1) return 'semi-urgent';
    if (semiUrgentSymptoms.length > 0) return 'moderate';
    return 'routine';
  }

  calculateSpecialistUrgency(specialist, symptoms) {
    const specialistInfo = this.specialistHierarchy[specialist];
    if (!specialistInfo || !specialistInfo.urgencyIndicators) return 'routine';

    const matchingUrgentSymptoms = specialistInfo.urgencyIndicators.filter(indicator =>
      Object.keys(symptoms).some(symptom => symptom.includes(indicator))
    );

    if (matchingUrgentSymptoms.length > 0) return 'urgent';
    return 'routine';
  }

  generateReasoning(diagnosis, specialistInfo, symptoms) {
    const symptomCount = Object.keys(symptoms).length;
    const confidenceText = diagnosis.confidenceLevel === 'HIGH' ? 'strong' : 
                          diagnosis.confidenceLevel === 'MODERATE' ? 'moderate' : 'limited';
    
    return `Based on ${confidenceText} evidence from your ${symptomCount} symptoms, ${diagnosis.disease} shows a ${(diagnosis.probability * 100).toFixed(1)}% match. ${specialistInfo.description} specialists are best equipped to ${specialistInfo.whenToConsult.toLowerCase()}.`;
  }

  generateTimeline(diagnosis, urgencyLevel, specialistInfo) {
    const baseTimeline = {
      'urgent': 'Seek immediate care (within hours)',
      'semi-urgent': 'Schedule within 1-3 days',
      'moderate': 'Schedule within 1-2 weeks',
      'routine': 'Schedule within 2-4 weeks'
    };

    const timeline = baseTimeline[urgencyLevel] || baseTimeline['routine'];
    
    if (diagnosis.confidenceLevel === 'HIGH' && urgencyLevel === 'routine') {
      return 'Schedule within 1-2 weeks (high confidence in diagnosis)';
    }
    
    return timeline;
  }

  generateAlternatives(primarySpecialist, diagnosis) {
    const alternatives = diagnosis.alternative_specialists || [];
    return alternatives.map(alt => ({
      specialist: alt,
      reason: `Alternative option if ${primarySpecialist} is not available`,
      info: this.specialistHierarchy[alt] || this.getGenericSpecialistInfo(alt)
    }));
  }

  generateQuestionsToAsk(specialist, diagnosis) {
    const baseQuestions = [
      "What tests or examinations will be needed?",
      "What are the possible treatment options?",
      "How long might treatment take?",
      "Are there any lifestyle changes I should make?"
    ];

    const specialistSpecific = {
      'Cardiology': ["Should I avoid certain activities?", "Do I need cardiac monitoring?"],
      'Dermatology': ["Is this condition contagious?", "Will this affect my appearance long-term?"],
      'Neurology': ["Could this affect my cognitive function?", "Are there any warning signs to watch for?"],
      'Gastroenterology': ["Are there dietary restrictions?", "Could this be related to other digestive issues?"],
      'Endocrinology': ["How will this affect my metabolism?", "Do I need regular monitoring?"]
    };

    return [...baseQuestions, ...(specialistSpecific[specialist] || [])];
  }

  generatePreparationAdvice(specialist, symptoms) {
    const general = [
      "Bring a list of all current medications",
      "Prepare a timeline of when symptoms started",
      "Bring any relevant medical records or test results",
      "Write down questions you want to ask"
    ];

    const specific = {
      'Cardiology': ["Note any family history of heart disease", "Record blood pressure readings if available"],
      'Dermatology': ["Take photos of skin changes", "List any new products or exposures"],
      'Neurology': ["Keep a headache/symptom diary", "Note any triggers or patterns"],
      'Gastroenterology': ["Keep a food diary", "Note bowel movement patterns"]
    };

    return [...general, ...(specific[specialist] || [])];
  }

  generateEmergencyRecommendation(symptoms) {
    return {
      rank: 0,
      specialist: 'Emergency Medicine',
      urgency: 'urgent',
      ...this.specialistHierarchy['Emergency Medicine'],
      reasoning: 'Your symptoms indicate a potentially serious condition that requires immediate medical attention.',
      timeline: 'Seek emergency care immediately',
      alternatives: [],
      questions: ["What caused this emergency?", "What immediate treatment is needed?"],
      preparation: ["Bring identification and insurance cards", "List current medications", "Have emergency contact ready"]
    };
  }

  generateGPRecommendation(symptoms) {
    return {
      rank: 99,
      specialist: 'General Practitioner',
      urgency: 'routine',
      ...this.specialistHierarchy['General Practitioner'],
      reasoning: 'Given the uncertainty in diagnosis, a General Practitioner can provide comprehensive evaluation and appropriate referrals.',
      timeline: 'Schedule within 1-2 weeks',
      alternatives: [{ specialist: 'Family Medicine', reason: 'Similar comprehensive care approach' }],
      questions: ["What other tests might be helpful?", "Should I see a specialist?", "What should I monitor?"],
      preparation: ["Complete medical history", "List all symptoms with timeline", "Bring previous medical records"]
    };
  }

  generateOverallAdvice(recommendations, urgencyLevel, confidence) {
    let advice = [];

    if (urgencyLevel === 'urgent') {
      advice.push("⚠️ Your symptoms suggest an urgent medical condition. Seek immediate medical attention.");
    } else if (urgencyLevel === 'semi-urgent') {
      advice.push("🟡 Your symptoms warrant prompt medical evaluation within the next few days.");
    }

    if (confidence?.showWarning) {
      advice.push("💡 Consider providing more symptom details for better recommendations.");
    }

    advice.push("📋 Always consult with healthcare professionals for proper diagnosis and treatment.");
    advice.push("🔄 If symptoms worsen or new symptoms appear, seek medical attention promptly.");

    return advice;
  }

  getGenericSpecialistInfo(specialist) {
    return {
      priority: 3,
      description: `Specialist in ${specialist}`,
      whenToConsult: `Conditions related to ${specialist}`,
      expertise: [`${specialist} conditions`],
      referralPower: 6
    };
  }
}

export default AdvancedSpecialistRecommender;
