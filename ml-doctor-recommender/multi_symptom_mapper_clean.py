from collections import defaultdict

# Multi-symptom to disease mapping
MULTI_SYMPTOM_DISEASE_MAPPING = {
    # Respiratory conditions
    ("cough", "fever"): {"disease": "Common Cold", "confidence": 0.7},
    ("cough", "fever", "shortness_of_breath"): {"disease": "Pneumonia", "confidence": 0.8},
    ("cough", "shortness_of_breath", "chest_pain"): {"disease": "Bronchitis", "confidence": 0.75},
    ("cough", "wheezing", "shortness_of_breath"): {"disease": "Asthma", "confidence": 0.85},
    
    # Cardiovascular conditions
    ("chest_pain", "shortness_of_breath", "fatigue"): {"disease": "Heart Disease", "confidence": 0.8},
    ("chest_pain", "palpitations", "dizziness"): {"disease": "Arrhythmia", "confidence": 0.75},
    ("chest_pain", "sweating", "nausea"): {"disease": "Heart Attack", "confidence": 0.9},
    
    # Gastrointestinal conditions
    ("stomach_pain", "nausea", "vomiting"): {"disease": "Gastroenteritis", "confidence": 0.8},
    ("abdominal_pain", "nausea", "vomiting"): {"disease": "Gastroenteritis", "confidence": 0.8},
    ("stomach_pain", "bloating", "constipation"): {"disease": "Irritable Bowel Syndrome", "confidence": 0.7},
    ("stomach_pain", "heartburn", "regurgitation"): {"disease": "Acid Reflux", "confidence": 0.85},
    ("stomach_pain", "diarrhoea", "fever"): {"disease": "Food Poisoning", "confidence": 0.8},
    
    # Neurological conditions
    ("headache", "sensitivity_to_light", "nausea"): {"disease": "Migraine", "confidence": 0.85},
    ("headache", "dizziness", "confusion"): {"disease": "Concussion", "confidence": 0.8},
    ("headache", "fever", "stiff_neck"): {"disease": "Meningitis", "confidence": 0.9},
    
    # Dermatological conditions
    ("skin_rash", "itching"): {"disease": "Eczema", "confidence": 0.75},
    ("skin_rash", "itching", "red_spots"): {"disease": "Chicken Pox", "confidence": 0.85},
    ("skin_rash", "fever", "sore_throat"): {"disease": "Scarlet Fever", "confidence": 0.8},
    
    # Musculoskeletal conditions
    ("joint_pain", "swelling_joints", "stiffness"): {"disease": "Arthritis", "confidence": 0.85},
    ("back_pain", "numbness", "weakness_in_limbs"): {"disease": "Herniated Disc", "confidence": 0.8},
    ("joint_pain", "fever", "fatigue"): {"disease": "Rheumatoid Arthritis", "confidence": 0.8},
    
    # Endocrine conditions
    ("excessive_hunger", "excessive_thirst", "frequent_urination"): {"disease": "Diabetes", "confidence": 0.9},
    ("weight_gain", "fatigue", "cold_intolerance"): {"disease": "Hypothyroidism", "confidence": 0.85},
    ("weight_loss", "anxiety", "heat_intolerance"): {"disease": "Hyperthyroidism", "confidence": 0.85},
    
    # Ophthalmological conditions
    ("eye_pain", "redness_of_eyes", "blurred_vision"): {"disease": "Conjunctivitis", "confidence": 0.8},
    ("eye_pain", "blurred_vision", "halos_around_lights"): {"disease": "Glaucoma", "confidence": 0.85},
    
    # ENT conditions
    ("sore_throat", "fever", "difficulty_swallowing"): {"disease": "Strep Throat", "confidence": 0.8},
    ("ear_pain", "fever", "reduced_hearing"): {"disease": "Ear Infection", "confidence": 0.85},
    ("nasal_congestion", "facial_pain", "headache"): {"disease": "Sinusitis", "confidence": 0.8},
    
    # Tropical and Infectious Diseases
    ("fever", "chills", "headache", "muscle_aches"): {"disease": "Malaria", "confidence": 0.77},
    ("fever", "headache", "abdominal_pain", "diarrhea"): {"disease": "Typhoid Fever", "confidence": 0.74},
    ("fever", "skin_rash", "joint_pain", "headache"): {"disease": "Zika Virus", "confidence": 0.74},
    ("fever", "skin_rash", "joint_pain", "pain_behind_the_eyes"): {"disease": "Dengue Fever", "confidence": 0.75},
    ("diarrhea", "vomiting", "dehydration"): {"disease": "Cholera", "confidence": 0.75},
    ("diarrhea", "vomiting", "dehydration", "abdominal_pain"): {"disease": "Cholera", "confidence": 0.78},
    ("cough", "fever", "weight_loss", "night_sweats"): {"disease": "Tuberculosis", "confidence": 0.78},
    ("fever", "muscle_aches", "headache"): {"disease": "Ebola", "confidence": 0.76},
    ("fever", "headache", "muscle_aches"): {"disease": "Yellow Fever", "confidence": 0.73},
    ("muscle_aches", "fever", "headache"): {"disease": "Lassa Fever", "confidence": 0.69},
    
    # Additional combinations for better coverage
    ("fever", "chills"): {"disease": "Malaria", "confidence": 0.65},
    ("fever", "muscle_aches"): {"disease": "Malaria", "confidence": 0.60},
    ("chills", "headache"): {"disease": "Malaria", "confidence": 0.58},
    ("abdominal_pain", "fever"): {"disease": "Typhoid Fever", "confidence": 0.60},
    ("diarrhea", "fever"): {"disease": "Typhoid Fever", "confidence": 0.65},
    ("skin_rash", "fever"): {"disease": "Dengue Fever", "confidence": 0.60},
    ("joint_pain", "fever"): {"disease": "Dengue Fever", "confidence": 0.58}
}

# Enhanced disease to specialist mapping for tropical diseases
TROPICAL_DISEASE_SPECIALISTS = {
    "Malaria": "Infectious Disease",
    "Typhoid Fever": "Infectious Disease", 
    "Dengue Fever": "Infectious Disease",
    "Zika Virus": "Infectious Disease",
    "Cholera": "Infectious Disease",
    "Tuberculosis": "Pulmonology",
    "Ebola": "Emergency Infectious Disease",
    "Yellow Fever": "Infectious Disease",
    "Lassa Fever": "Infectious Disease",
    "Heart Attack": "Emergency Cardiology",
    "Meningitis": "Emergency Neurology",
    "Diabetes Type 1": "Endocrinology"
}

def get_disease_from_symptoms(active_symptoms):
    normalized_symptoms = [s.lower().replace(' ', '_') for s in active_symptoms]
    matched_diseases = []
    
    for symptom_set, disease_info in MULTI_SYMPTOM_DISEASE_MAPPING.items():
        symptom_set = set(symptom_set)
        active_set = set(normalized_symptoms)
        matching_symptoms = symptom_set.intersection(active_set)
        
        if len(matching_symptoms) == len(symptom_set):
            matched_diseases.append({
                "disease": disease_info["disease"],
                "confidence": disease_info["confidence"],
                "matching_symptoms": list(matching_symptoms)
            })
        elif len(matching_symptoms) >= 2 and len(matching_symptoms) / len(symptom_set) >= 0.7:
            adjusted_confidence = disease_info["confidence"] * (len(matching_symptoms) / len(symptom_set))
            matched_diseases.append({
                "disease": disease_info["disease"],
                "confidence": adjusted_confidence,
                "matching_symptoms": list(matching_symptoms)
            })
    
    matched_diseases.sort(key=lambda x: x["confidence"], reverse=True)
    return matched_diseases

def get_intelligent_disease_matches(active_symptoms, max_results=5):
    normalized_symptoms = [s.lower().replace(' ', '_') for s in active_symptoms]
    potential_matches = []
    
    for symptom_set, disease_info in MULTI_SYMPTOM_DISEASE_MAPPING.items():
        symptom_set = set(symptom_set)
        active_set = set(normalized_symptoms)
        matching_symptoms = symptom_set.intersection(active_set)
        
        if len(matching_symptoms) > 0:
            coverage = len(matching_symptoms) / len(symptom_set)
            adjusted_confidence = disease_info["confidence"] * coverage
            
            if len(matching_symptoms) == len(symptom_set):
                adjusted_confidence *= 1.1
            
            if disease_info["disease"] in TROPICAL_DISEASE_SPECIALISTS:
                adjusted_confidence *= 1.05
            
            potential_matches.append({
                "disease": disease_info["disease"],
                "confidence": min(adjusted_confidence, 0.95),
                "matching_symptoms": list(matching_symptoms),
                "coverage": coverage,
                "specialist": TROPICAL_DISEASE_SPECIALISTS.get(disease_info["disease"], "Internal Medicine")
            })
    
    potential_matches.sort(key=lambda x: (x["confidence"], x["coverage"]), reverse=True)
    return potential_matches[:max_results]

def get_specialist_for_disease(disease, disease_to_specialist_mapping):
    if disease in disease_to_specialist_mapping:
        return disease_to_specialist_mapping[disease]
    else:
        return {
            "primary": "General Practitioner",
            "secondary": ["Internal Medicine"],
            "confidence": 0.60,
            "explanation": f"For {disease}, we recommend starting with a General Practitioner who can provide initial assessment and referrals if needed."
        }

def get_multi_symptom_recommendations(active_symptoms, disease_to_specialist_mapping):
    potential_diseases = get_intelligent_disease_matches(active_symptoms, max_results=5)
    
    if not potential_diseases:
        potential_diseases = get_disease_from_symptoms(active_symptoms)
    
    if not potential_diseases:
        return []
    
    recommendations = []
    for disease_info in potential_diseases:
        disease = disease_info["disease"]
        confidence = disease_info["confidence"]
        matching_symptoms = disease_info.get("matching_symptoms", active_symptoms)
        
        if disease in TROPICAL_DISEASE_SPECIALISTS:
            specialist = TROPICAL_DISEASE_SPECIALISTS[disease]
            specialist_confidence = 0.90
        else:
            specialist_info = get_specialist_for_disease(disease, disease_to_specialist_mapping)
            specialist = specialist_info["primary"]
            specialist_confidence = specialist_info["confidence"]
        
        recommendation = {
            "disease": disease,
            "probability": confidence,
            "specialist": specialist,
            "alternative_specialists": [],
            "confidence": specialist_confidence * confidence,
            "explanation": f"Based on symptoms matching {disease}, recommended specialist: {specialist}",
            "matching_symptoms": matching_symptoms
        }
        
        recommendations.append(recommendation)
    
    return recommendations