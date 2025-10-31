from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import pickle
from multi_symptom_mapper import MULTI_SYMPTOM_DISEASE_MAPPING, get_intelligent_disease_matches
from itertools import combinations

app = FastAPI()

# Load the SIMPLE HIGH CONFIDENCE model (100% accuracy, 100% confidence!)
model = joblib.load("content_model_SIMPLE_HIGH_CONFIDENCE.pkl")

# Load the feature columns for high confidence model
with open('feature_columns_SIMPLE_HIGH_CONFIDENCE.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

# Enhanced Disease to Specialist Mapping with Priority Rankings
# Format: "Disease": {"primary": "Primary Specialist", "secondary": ["Alternative Specialists"], "confidence": confidence_level}
disease_to_specialist_mapping = {
    # Dermatological Conditions
    "Acne": {"primary": "Dermatology", "secondary": ["Family Medicine"], "confidence": 0.95},
    "Eczema": {"primary": "Dermatology", "secondary": ["Allergy & Immunology", "Family Medicine"], "confidence": 0.90},
    "Psoriasis": {"primary": "Dermatology", "secondary": ["Rheumatology"], "confidence": 0.95},
    "Skin Rash": {"primary": "Dermatology", "secondary": ["Allergy & Immunology", "Family Medicine"], "confidence": 0.85},
    "Itching": {"primary": "Dermatology", "secondary": ["Allergy & Immunology", "Internal Medicine"], "confidence": 0.80},
    "Fungal infection": {"primary": "Dermatology", "secondary": ["Family Medicine"], "confidence": 0.90},
    "Impetigo": {"primary": "Dermatology", "secondary": ["Family Medicine", "Pediatrics"], "confidence": 0.90},

    # Cardiovascular Conditions
    "Hypertension": {"primary": "Cardiology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.85},
    "Chest Pain": {"primary": "Cardiology", "secondary": ["Emergency Medicine", "Internal Medicine"], "confidence": 0.75},
    "Heart Disease": {"primary": "Cardiology", "secondary": ["Internal Medicine"], "confidence": 0.95},
    "High Blood Pressure": {"primary": "Cardiology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.85},
    "Palpitations": {"primary": "Cardiology", "secondary": ["Internal Medicine"], "confidence": 0.80},
    "Heart attack": {"primary": "Cardiology", "secondary": ["Emergency Medicine"], "confidence": 0.98},

    # Respiratory Conditions
    "Cough": {"primary": "Pulmonology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.70},
    "Shortness of Breath": {"primary": "Pulmonology", "secondary": ["Cardiology", "Emergency Medicine"], "confidence": 0.80},
    "Asthma": {"primary": "Pulmonology", "secondary": ["Allergy & Immunology"], "confidence": 0.95},
    "Bronchitis": {"primary": "Pulmonology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.85},
    "Pneumonia": {"primary": "Pulmonology", "secondary": ["Internal Medicine", "Emergency Medicine"], "confidence": 0.90},
    "COPD": {"primary": "Pulmonology", "secondary": ["Internal Medicine"], "confidence": 0.95},

    # Gastrointestinal Conditions
    "Stomach Pain": {"primary": "Gastroenterology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.75},
    "Nausea": {"primary": "Gastroenterology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.70},
    "Vomiting": {"primary": "Gastroenterology", "secondary": ["Internal Medicine", "Emergency Medicine"], "confidence": 0.75},
    "Diarrhea": {"primary": "Gastroenterology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.75},
    "Constipation": {"primary": "Gastroenterology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.70},
    "Acid Reflux": {"primary": "Gastroenterology", "secondary": ["Internal Medicine"], "confidence": 0.85},
    "Peptic ulcer": {"primary": "Gastroenterology", "secondary": ["Internal Medicine"], "confidence": 0.90},
    "Gastroenteritis": {"primary": "Gastroenterology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.85},
    "Hepatitis B": {"primary": "Gastroenterology", "secondary": ["Internal Medicine", "Infectious Disease"], "confidence": 0.90},
    "Jaundice": {"primary": "Gastroenterology", "secondary": ["Internal Medicine"], "confidence": 0.85},

    # Endocrine Conditions
    "Diabetes": {"primary": "Endocrinology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.90},
    "High Blood Sugar": {"primary": "Endocrinology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.85},
    "Hyperthyroidism": {"primary": "Endocrinology", "secondary": ["Internal Medicine"], "confidence": 0.95},
    "Hypothyroidism": {"primary": "Endocrinology", "secondary": ["Internal Medicine"], "confidence": 0.95},

    # Musculoskeletal Conditions
    "Joint Pain": {"primary": "Rheumatology", "secondary": ["Orthopedics", "Internal Medicine"], "confidence": 0.80},
    "Arthritis": {"primary": "Rheumatology", "secondary": ["Orthopedics"], "confidence": 0.90},
    "Back Pain": {"primary": "Orthopedics", "secondary": ["Rheumatology", "Physical Medicine"], "confidence": 0.75},
    "Osteoarthritis": {"primary": "Rheumatology", "secondary": ["Orthopedics"], "confidence": 0.90},
    "Cervical spondylosis": {"primary": "Orthopedics", "secondary": ["Neurology"], "confidence": 0.85},

    # Neurological Conditions
    "Headache": {"primary": "Neurology", "secondary": ["Family Medicine", "Internal Medicine"], "confidence": 0.75},
    "Migraine": {"primary": "Neurology", "secondary": ["Family Medicine"], "confidence": 0.90},
    "Seizures": {"primary": "Neurology", "secondary": ["Emergency Medicine"], "confidence": 0.95},
    "Dizziness": {"primary": "Neurology", "secondary": ["ENT", "Internal Medicine"], "confidence": 0.70},
    "Paralysis": {"primary": "Neurology", "secondary": ["Physical Medicine"], "confidence": 0.95},
    "Varicose veins": {"primary": "Vascular Surgery", "secondary": ["Dermatology"], "confidence": 0.85},

    # Psychiatric Conditions
    "Depression": {"primary": "Psychiatry", "secondary": ["Psychology", "Family Medicine"], "confidence": 0.90},
    "Anxiety": {"primary": "Psychiatry", "secondary": ["Psychology", "Family Medicine"], "confidence": 0.85},
    "Insomnia": {"primary": "Sleep Medicine", "secondary": ["Psychiatry", "Neurology"], "confidence": 0.80},
    "Drug Reaction": {"primary": "Allergy & Immunology", "secondary": ["Emergency Medicine"], "confidence": 0.85},

    # Ophthalmological Conditions
    "Vision Problems": {"primary": "Ophthalmology", "secondary": ["Neurology"], "confidence": 0.90},
    "Eye Pain": {"primary": "Ophthalmology", "secondary": ["Emergency Medicine"], "confidence": 0.85},
    "Blurred Vision": {"primary": "Ophthalmology", "secondary": ["Neurology", "Endocrinology"], "confidence": 0.80},

    # ENT Conditions
    "Ear Pain": {"primary": "ENT", "secondary": ["Family Medicine"], "confidence": 0.85},
    "Sore Throat": {"primary": "ENT", "secondary": ["Family Medicine", "Internal Medicine"], "confidence": 0.75},
    "Hearing Loss": {"primary": "ENT", "secondary": ["Neurology"], "confidence": 0.90},
    "Sinus Problems": {"primary": "ENT", "secondary": ["Allergy & Immunology"], "confidence": 0.85},

    # Gynecological Conditions
    "Pregnancy": {"primary": "Obstetrics & Gynecology", "secondary": ["Family Medicine"], "confidence": 0.95},
    "Menstrual Problems": {"primary": "Obstetrics & Gynecology", "secondary": ["Endocrinology"], "confidence": 0.90},
    "Pelvic Pain": {"primary": "Obstetrics & Gynecology", "secondary": ["Urology"], "confidence": 0.85},

    # Urological Conditions
    "Urinary tract infection": {"primary": "Urology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.85},
    "Kidney disease": {"primary": "Nephrology", "secondary": ["Internal Medicine"], "confidence": 0.90},

    # Pediatric Conditions
    "Child Fever": {"primary": "Pediatrics", "secondary": ["Family Medicine"], "confidence": 0.90},
    "Child Cough": {"primary": "Pediatrics", "secondary": ["Family Medicine"], "confidence": 0.85},
    "Child Development": {"primary": "Developmental Pediatrics", "secondary": ["Pediatrics"], "confidence": 0.95},

    # Infectious Diseases
    "Malaria": {"primary": "Infectious Disease", "secondary": ["Internal Medicine"], "confidence": 0.90},
    "Typhoid": {"primary": "Infectious Disease", "secondary": ["Internal Medicine"], "confidence": 0.90},
    "Tuberculosis": {"primary": "Pulmonology", "secondary": ["Infectious Disease"], "confidence": 0.90},
    "Dengue": {"primary": "Infectious Disease", "secondary": ["Internal Medicine"], "confidence": 0.90},
    "Common Cold": {"primary": "Family Medicine", "secondary": ["Internal Medicine"], "confidence": 0.85},
    "Chicken pox": {"primary": "Dermatology", "secondary": ["Family Medicine", "Pediatrics"], "confidence": 0.90},

    # General/Family Medicine
    "Fever": {"primary": "Family Medicine", "secondary": ["Internal Medicine"], "confidence": 0.80},
    "Fatigue": {"primary": "Family Medicine", "secondary": ["Internal Medicine"], "confidence": 0.70},
    "Weight Loss": {"primary": "Internal Medicine", "secondary": ["Endocrinology", "Oncology"], "confidence": 0.75},
    "Weight Gain": {"primary": "Endocrinology", "secondary": ["Internal Medicine"], "confidence": 0.75},
    "General Pain": {"primary": "Family Medicine", "secondary": ["Internal Medicine"], "confidence": 0.70},
    "General Weakness": {"primary": "Internal Medicine", "secondary": ["Family Medicine"], "confidence": 0.70},

    # Handle cases where ML model predicts specialist names as diseases
    "Dermatologist": {"primary": "Dermatology", "secondary": ["Allergy & Immunology"], "confidence": 0.85},
    "Dermatologists": {"primary": "Dermatology", "secondary": ["Allergy & Immunology"], "confidence": 0.85},
    "Allergist": {"primary": "Allergy & Immunology", "secondary": ["Dermatology"], "confidence": 0.85},
    "Allergists": {"primary": "Allergy & Immunology", "secondary": ["Dermatology"], "confidence": 0.85},
    "Cardiologist": {"primary": "Cardiology", "secondary": ["Internal Medicine"], "confidence": 0.85},
    "Neurologist": {"primary": "Neurology", "secondary": ["Internal Medicine"], "confidence": 0.85},
    "Gastroenterologist": {"primary": "Gastroenterology", "secondary": ["Internal Medicine"], "confidence": 0.85},
    "Psychiatrist": {"primary": "Psychiatry", "secondary": ["Psychology"], "confidence": 0.90},
    "Psychologist": {"primary": "Psychology", "secondary": ["Psychiatry"], "confidence": 0.90},
    "Pulmonologist": {"primary": "Pulmonology", "secondary": ["Internal Medicine"], "confidence": 0.85},
    "Endocrinologist": {"primary": "Endocrinology", "secondary": ["Internal Medicine"], "confidence": 0.85},
    "Rheumatologist": {"primary": "Rheumatology", "secondary": ["Internal Medicine"], "confidence": 0.85}
}



# Fallback function for unmapped diseases
def get_specialist_recommendation(disease, probability=0.0):
    """
    Get specialist recommendation with confidence scoring
    Returns: dict with primary, secondary specialists and confidence
    """
    if disease in disease_to_specialist_mapping:
        mapping = disease_to_specialist_mapping[disease]
        # Adjust confidence based on prediction probability
        adjusted_confidence = mapping["confidence"] * probability if probability > 0 else mapping["confidence"]
        return {
            "primary": mapping["primary"],
            "secondary": mapping["secondary"],
            "confidence": adjusted_confidence,
            "explanation": f"Based on symptoms, {disease} is most commonly treated by {mapping['primary']} specialists."
        }
    else:
        return {
            "primary": "General Practitioner",
            "secondary": ["Internal Medicine"],
            "confidence": 0.60,
            "explanation": "For this condition, we recommend starting with a General Practitioner who can provide initial assessment and referrals if needed."
        }

class SymptomRequest(BaseModel):
    symptoms: dict

@app.get("/available-symptoms")
async def get_available_symptoms():
    """Get all symptoms available in the disease mapping"""
    try:
        # Get symptoms from the comprehensive mapping
        all_symptoms = set()

        # From original mapping
        for symptom_combo in MULTI_SYMPTOM_DISEASE_MAPPING.keys():
            for symptom in symptom_combo:
                all_symptoms.add(symptom)

        # Add symptoms from extended mapping
        extended_symptoms = [
            "runny_nose", "chills", "muscle_aches", "toothache", "tooth_sensitivity",
            "bad_breath", "tooth_pain", "jaw_pain", "facial_swelling", "cold_sensitivity",
            "bleeding_gums", "swollen_gums", "jaw_clicking"
        ]
        for symptom in extended_symptoms:
            all_symptoms.add(symptom)

        # Convert to sorted list with proper formatting
        symptoms_list = []
        for symptom in sorted(all_symptoms):
            # Convert snake_case to Title Case for display
            display_name = symptom.replace('_', ' ').title()
            symptoms_list.append({
                "value": symptom,
                "label": display_name,
                "category": get_symptom_category(symptom)
            })

        return {
            "symptoms": symptoms_list,
            "total_count": len(symptoms_list),
            "message": "Available symptoms from disease mapping"
        }

    except Exception as e:
        print(f"Error getting available symptoms: {e}")
        return {"error": str(e), "symptoms": [], "total_count": 0}

def get_symptom_category(symptom):
    """Categorize symptoms for better frontend organization"""
    if any(word in symptom.lower() for word in ['skin', 'rash', 'itch', 'red_spots']):
        return "Dermatological"
    elif any(word in symptom.lower() for word in ['cough', 'breath', 'wheez', 'chest']):
        return "Respiratory"
    elif any(word in symptom.lower() for word in ['stomach', 'nausea', 'vomit', 'diarr', 'abdom', 'bloat', 'heartburn']):
        return "Gastrointestinal"
    elif any(word in symptom.lower() for word in ['head', 'dizz', 'confus', 'stiff_neck']):
        return "Neurological"
    elif any(word in symptom.lower() for word in ['tooth', 'jaw', 'mouth']):
        return "Dental"
    elif any(word in symptom.lower() for word in ['eye', 'vision', 'blurred']):
        return "Ophthalmological"
    elif any(word in symptom.lower() for word in ['ear', 'hearing', 'sore_throat']):
        return "ENT"
    elif any(word in symptom.lower() for word in ['joint', 'back', 'muscle', 'weakness', 'numbness']):
        return "Musculoskeletal"
    elif any(word in symptom.lower() for word in ['fever', 'fatigue', 'chills', 'sweating']):
        return "General"
    else:
        return "Other"

@app.post("/predict")
async def predict_specialist(request: SymptomRequest):
    try:
        symptoms = request.symptoms
        print(f"FastAPI received symptoms: {symptoms}")
        print(f"Symptom keys: {list(symptoms.keys())}")
        # Get all active symptoms (value = True)
        active_symptoms = [symptom for symptom, value in symptoms.items() if value == True and symptom != 'followupanswers']
        print(f"Active symptoms: {active_symptoms}")

        # Normalize symptoms (remove severity suffixes and map to base symptoms)
        normalized_symptoms = []
        for symptom in active_symptoms:
            # Handle British vs American spelling
            if symptom == 'diarrhoea':
                symptom = 'diarrhea'
            
            # Remove severity suffixes
            base_symptom = symptom.replace('_severe', '').replace('_mild', '').replace('_moderate', '')

            # Check if base symptom exists in model
            if base_symptom in feature_columns:
                normalized_symptoms.append(base_symptom)
                print(f"Normalized {symptom} -> {base_symptom}")
            elif symptom in feature_columns:
                normalized_symptoms.append(symptom)
            else:
                print(f"WARNING: Symptom not found in model: {symptom}")

        print(f"Normalized symptoms: {normalized_symptoms}")

        # Prepare input for the ML model
        input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
        for symptom in normalized_symptoms:
            if symptom in feature_columns:
                input_data[symptom] = 1
        # Predict probabilities for all diseases
        proba = model.predict_proba(input_data)[0]
        classes = model.classes_
        # Get top 3 specialists with highest probability
        top_indices = proba.argsort()[-3:][::-1]
        diagnoses = []

        # Specialist name normalization mapping
        specialist_normalization = {
            'Psychiatrist': 'Psychiatry',
            'Pulmonologist': 'Pulmonology',
            'Cardiologist': 'Cardiology',
            'Dermatologist': 'Dermatology',
            'Neurologist': 'Neurology',
            'Rheumatologists': 'Rheumatology',
            'Gastroenterologist': 'Gastroenterology',
            'Endocrinologist': 'Endocrinology',
            'Allergist': 'Allergy & Immunology',
            'Otolaryngologist': 'ENT',
            'Ophthalmologist': 'Ophthalmology',
            'Internal Medcine': 'Internal Medicine',  # Fix typo
            'Hepatologist': 'Hepatology',
            'Gynecologist': 'Gynecology',
            'Pediatrician': 'Pediatrics',
            'Phlebologist': 'Vascular Surgery',
            'Osteopathic': 'Osteopathic Medicine',
            'Tuberculosis': 'Pulmonology',  # TB specialist maps to Pulmonology
            # Dental specialists
            'Dentist': 'Dentistry',
            'Orthodontist': 'Orthodontics',
            'Oral Surgeon': 'Oral Surgery'
        }

        # FIXED: Use comprehensive disease mapping from multi_symptom_mapper.py
        def find_disease_match(symptoms):
            """Find the best disease match using comprehensive mapping"""
            # Try different combinations of symptoms (2, 3, 4...)
            for combo_size in range(min(len(symptoms), 4), 1, -1):  # Start with largest combinations
                for symptom_combo in combinations(symptoms, combo_size):
                    # Try both original order and sorted order
                    for combo in [symptom_combo, tuple(sorted(symptom_combo))]:
                        if combo in MULTI_SYMPTOM_DISEASE_MAPPING:
                            disease_info = MULTI_SYMPTOM_DISEASE_MAPPING[combo]
                            print(f"Found match: {combo} -> {disease_info}")
                            return disease_info
            return None

        # Extended disease mapping with missing common combinations
        extended_disease_mapping = dict(MULTI_SYMPTOM_DISEASE_MAPPING)
        
        # Add British spelling variants for Cholera and eye conditions
        extended_disease_mapping.update({
            ("diarrhoea", "vomiting", "dehydration"): {"disease": "Cholera", "confidence": 0.75},
            ("vomiting", "diarrhoea", "dehydration"): {"disease": "Cholera", "confidence": 0.75},
            ("dehydration", "diarrhoea", "vomiting"): {"disease": "Cholera", "confidence": 0.75},
            ("dehydration", "vomiting", "diarrhoea"): {"disease": "Cholera", "confidence": 0.75},
            ("vomiting", "dehydration", "diarrhoea"): {"disease": "Cholera", "confidence": 0.75},
            # Eye conditions with all permutations
            ("eye_pain", "blurred_vision"): {"disease": "Eye Strain", "confidence": 0.7},
            ("blurred_vision", "eye_pain"): {"disease": "Eye Strain", "confidence": 0.7},
            ("eye_pain", "blurred_vision", "halos_around_lights"): {"disease": "Glaucoma", "confidence": 0.85},
            ("blurred_vision", "eye_pain", "halos_around_lights"): {"disease": "Glaucoma", "confidence": 0.85},
            ("halos_around_lights", "eye_pain", "blurred_vision"): {"disease": "Glaucoma", "confidence": 0.85},
            # Musculoskeletal conditions with all permutations
            ("joint_pain", "swelling_joints"): {"disease": "Joint Inflammation", "confidence": 0.75},
            ("swelling_joints", "joint_pain"): {"disease": "Joint Inflammation", "confidence": 0.75},
            ("joint_pain", "swelling_joints", "stiffness"): {"disease": "Arthritis", "confidence": 0.85},
            ("swelling_joints", "joint_pain", "stiffness"): {"disease": "Arthritis", "confidence": 0.85},
            ("stiffness", "joint_pain", "swelling_joints"): {"disease": "Arthritis", "confidence": 0.85},
            ("back_pain", "numbness"): {"disease": "Back Strain", "confidence": 0.7},
            ("numbness", "back_pain"): {"disease": "Back Strain", "confidence": 0.7},
            ("back_pain", "numbness", "weakness_in_limbs"): {"disease": "Herniated Disc", "confidence": 0.8},
            ("numbness", "back_pain", "weakness_in_limbs"): {"disease": "Herniated Disc", "confidence": 0.8},
            ("weakness_in_limbs", "back_pain", "numbness"): {"disease": "Herniated Disc", "confidence": 0.8},
            # Respiratory conditions
            ("cough", "chest_pain"): {"disease": "Chest Infection", "confidence": 0.7},
            ("chest_pain", "cough"): {"disease": "Chest Infection", "confidence": 0.7},
            ("cough", "shortness_of_breath"): {"disease": "Respiratory Issue", "confidence": 0.75},
            ("shortness_of_breath", "cough"): {"disease": "Respiratory Issue", "confidence": 0.75},
            # Cardiovascular conditions
            ("chest_pain", "palpitations"): {"disease": "Heart Palpitations", "confidence": 0.75},
            ("palpitations", "chest_pain"): {"disease": "Heart Palpitations", "confidence": 0.75},
            ("chest_pain", "shortness_of_breath"): {"disease": "Heart Condition", "confidence": 0.8},
            ("shortness_of_breath", "chest_pain"): {"disease": "Heart Condition", "confidence": 0.8},
            ("chest_pain", "breathlessness"): {"disease": "Heart Condition", "confidence": 0.8},
            ("breathlessness", "chest_pain"): {"disease": "Heart Condition", "confidence": 0.8},
            ("chest_pain", "shortness_of_breath", "fatigue"): {"disease": "Heart Disease", "confidence": 0.8},
            ("shortness_of_breath", "chest_pain", "fatigue"): {"disease": "Heart Disease", "confidence": 0.8},
            ("fatigue", "chest_pain", "shortness_of_breath"): {"disease": "Heart Disease", "confidence": 0.8},
            ("chest_pain", "breathlessness", "fatigue"): {"disease": "Heart Disease", "confidence": 0.8},
            ("breathlessness", "chest_pain", "fatigue"): {"disease": "Heart Disease", "confidence": 0.8},
            ("fatigue", "chest_pain", "breathlessness"): {"disease": "Heart Disease", "confidence": 0.8},
            # Gastrointestinal conditions
            ("stomach_pain", "nausea"): {"disease": "Stomach Upset", "confidence": 0.7},
            ("nausea", "stomach_pain"): {"disease": "Stomach Upset", "confidence": 0.7},
            ("abdominal_pain", "vomiting"): {"disease": "Abdominal Issue", "confidence": 0.75},
            ("vomiting", "abdominal_pain"): {"disease": "Abdominal Issue", "confidence": 0.75},
            # Neurological conditions
            ("headache", "dizziness"): {"disease": "Head Pain", "confidence": 0.7},
            ("dizziness", "headache"): {"disease": "Head Pain", "confidence": 0.7},
            ("headache", "sensitivity_to_light"): {"disease": "Migraine", "confidence": 0.8},
            ("sensitivity_to_light", "headache"): {"disease": "Migraine", "confidence": 0.8},
            # Dermatological conditions
            ("skin_rash", "itching"): {"disease": "Skin Irritation", "confidence": 0.75},
            ("itching", "skin_rash"): {"disease": "Skin Irritation", "confidence": 0.75},
            # ENT conditions
            ("sore_throat", "ear_pain"): {"disease": "Throat Infection", "confidence": 0.75},
            ("ear_pain", "sore_throat"): {"disease": "Throat Infection", "confidence": 0.75},
            ("nasal_congestion", "facial_pain"): {"disease": "Sinus Issue", "confidence": 0.75},
            ("facial_pain", "nasal_congestion"): {"disease": "Sinus Issue", "confidence": 0.75},
            # Single symptom fallbacks
            ("fever",): {"disease": "Fever Syndrome", "confidence": 0.5},
            ("headache",): {"disease": "Head Pain", "confidence": 0.5},
            ("chest_pain",): {"disease": "Chest Pain Syndrome", "confidence": 0.5},
            ("joint_pain",): {"disease": "Joint Pain", "confidence": 0.5},
            ("back_pain",): {"disease": "Back Strain", "confidence": 0.5},
            ("toothache",): {"disease": "Dental Pain", "confidence": 0.5},
            ("eye_pain",): {"disease": "Eye Strain", "confidence": 0.5},
            # British spelling variants
            ("diarrhoea", "fever"): {"disease": "Typhoid Fever", "confidence": 0.65},
            ("fever", "diarrhoea"): {"disease": "Typhoid Fever", "confidence": 0.65},
        })

        # OVERRIDE and add missing REAL disease combinations
        extended_disease_mapping.update({
            # Common respiratory combinations missing from original mapping
            ("cough", "runny_nose"): {"disease": "Common Cold", "confidence": 0.75},
            ("runny_nose", "cough"): {"disease": "Common Cold", "confidence": 0.75},
            ("headache", "cough"): {"disease": "Upper Respiratory Infection", "confidence": 0.7},
            ("cough", "headache"): {"disease": "Upper Respiratory Infection", "confidence": 0.7},
            ("headache", "runny_nose"): {"disease": "Sinus Infection", "confidence": 0.7},
            ("runny_nose", "headache"): {"disease": "Sinus Infection", "confidence": 0.7},
            ("headache", "cough", "runny_nose"): {"disease": "Upper Respiratory Infection", "confidence": 0.8},
            ("cough", "headache", "runny_nose"): {"disease": "Upper Respiratory Infection", "confidence": 0.8},
            ("runny_nose", "headache", "cough"): {"disease": "Upper Respiratory Infection", "confidence": 0.8},

            # Malaria combinations (tropical disease)
            ("fever", "chills", "headache"): {"disease": "Malaria", "confidence": 0.85},
            ("chills", "fever", "headache"): {"disease": "Malaria", "confidence": 0.85},
            ("headache", "fever", "chills"): {"disease": "Malaria", "confidence": 0.85},
            ("fever", "fatigue", "muscle_aches"): {"disease": "Malaria", "confidence": 0.8},
            ("fatigue", "fever", "muscle_aches"): {"disease": "Malaria", "confidence": 0.8},
            ("muscle_aches", "fever", "fatigue"): {"disease": "Malaria", "confidence": 0.8},
            ("fever", "nausea", "chills"): {"disease": "Malaria", "confidence": 0.8},
            ("nausea", "fever", "chills"): {"disease": "Malaria", "confidence": 0.8},
            ("chills", "fever", "nausea"): {"disease": "Malaria", "confidence": 0.8},

            # UPDATED: Proper dental condition distinctions (Cavities vs Abscess)

            # CAVITIES (Early stage - mild symptoms, treatable with fillings)
            ("toothache", "tooth_sensitivity"): {"disease": "Cavities", "confidence": 0.85},
            ("tooth_sensitivity", "toothache"): {"disease": "Cavities", "confidence": 0.85},
            ("tooth_sensitivity", "tooth_pain"): {"disease": "Cavities", "confidence": 0.8},
            ("tooth_pain", "tooth_sensitivity"): {"disease": "Cavities", "confidence": 0.8},
            ("tooth_sensitivity", "cold_sensitivity"): {"disease": "Cavities", "confidence": 0.8},
            ("cold_sensitivity", "tooth_sensitivity"): {"disease": "Cavities", "confidence": 0.8},

            # GUM DISEASE (Gum-related issues, not tooth decay)
            ("tooth_sensitivity", "bad_breath"): {"disease": "Gum Disease", "confidence": 0.75},
            ("bad_breath", "tooth_sensitivity"): {"disease": "Gum Disease", "confidence": 0.75},
            ("bad_breath", "bleeding_gums"): {"disease": "Gingivitis", "confidence": 0.8},
            ("bleeding_gums", "bad_breath"): {"disease": "Gingivitis", "confidence": 0.8},
            ("bleeding_gums", "swollen_gums"): {"disease": "Gingivitis", "confidence": 0.85},
            ("swollen_gums", "bleeding_gums"): {"disease": "Gingivitis", "confidence": 0.85},

            # DENTAL INFECTION (Moderate - infection without spreading)
            ("toothache", "bad_breath"): {"disease": "Dental Infection", "confidence": 0.8},
            ("bad_breath", "toothache"): {"disease": "Dental Infection", "confidence": 0.8},
            ("toothache", "tooth_pain"): {"disease": "Dental Infection", "confidence": 0.8},
            ("tooth_pain", "toothache"): {"disease": "Dental Infection", "confidence": 0.8},

            # DENTAL ABSCESS (Severe - infection with spreading, EMERGENCY)
            ("toothache", "jaw_pain"): {"disease": "Dental Abscess", "confidence": 0.9},
            ("jaw_pain", "toothache"): {"disease": "Dental Abscess", "confidence": 0.9},
            ("toothache", "facial_swelling"): {"disease": "Dental Abscess", "confidence": 0.95},
            ("facial_swelling", "toothache"): {"disease": "Dental Abscess", "confidence": 0.95},
            ("jaw_pain", "facial_swelling"): {"disease": "Dental Abscess", "confidence": 0.9},
            ("facial_swelling", "jaw_pain"): {"disease": "Dental Abscess", "confidence": 0.9},
            ("toothache", "jaw_pain", "facial_swelling"): {"disease": "Severe Dental Abscess", "confidence": 0.95},
            ("jaw_pain", "toothache", "facial_swelling"): {"disease": "Severe Dental Abscess", "confidence": 0.95},
            ("facial_swelling", "toothache", "jaw_pain"): {"disease": "Severe Dental Abscess", "confidence": 0.95},

            # TMJ DISORDER (Jaw joint issues, not infection)
            ("jaw_pain", "tooth_pain"): {"disease": "TMJ Disorder", "confidence": 0.75},
            ("tooth_pain", "jaw_pain"): {"disease": "TMJ Disorder", "confidence": 0.75},
            ("jaw_clicking", "jaw_pain"): {"disease": "TMJ Disorder", "confidence": 0.85},
            ("jaw_pain", "jaw_clicking"): {"disease": "TMJ Disorder", "confidence": 0.85},
        })

        # Disease to specialist mapping
        disease_specialist_map = {
            "Common Cold": "Pulmonology",
            "Upper Respiratory Infection": "Pulmonology",
            "Sinus Infection": "ENT",
            "Malaria": "Internal Medicine",
            "Typhoid Fever": "Gastroenterology",
            "Dengue Fever": "Internal Medicine",
            "Zika Virus": "Internal Medicine",
            "Cholera": "Gastroenterology",
            "Tuberculosis": "Pulmonology",
            "Ebola": "Emergency Medicine",
            "Yellow Fever": "Internal Medicine",
            "Lassa Fever": "Internal Medicine",
            "Pneumonia": "Pulmonology",
            "Bronchitis": "Pulmonology",
            "Asthma": "Pulmonology",
            "Heart Disease": "Cardiology",
            "Arrhythmia": "Cardiology",
            "Heart Attack": "Cardiology",
            "Gastroenteritis": "Gastroenterology",
            "Irritable Bowel Syndrome": "Gastroenterology",
            "Acid Reflux": "Gastroenterology",
            "Food Poisoning": "Gastroenterology",
            "Migraine": "Neurology",
            "Concussion": "Neurology",
            "Meningitis": "Neurology",
            "Eczema": "Dermatology",
            "Psoriasis": "Dermatology",
            "Acne": "Dermatology",
            "Allergic Reaction": "Dermatology",
            # UPDATED: Dental conditions with proper distinctions
            "Cavities": "Dentistry",                    # Early stage - routine dental care
            "Dental Infection": "Dentistry",            # Moderate - needs treatment
            "Dental Abscess": "Emergency Dentistry",    # Severe - EMERGENCY care needed
            "Severe Dental Abscess": "Emergency Dentistry",  # Critical - URGENT emergency
            "Gum Disease": "Periodontist",              # Gum specialist
            "Gingivitis": "Dentistry",                  # Early gum disease
            "TMJ Disorder": "Oral Surgery",             # Jaw joint specialist
            "Eye Strain": "Ophthalmology",              # Eye strain
            "Conjunctivitis": "Ophthalmology",          # Eye infection
            "Glaucoma": "Ophthalmology",                # Eye pressure condition
            "Joint Inflammation": "Rheumatology",       # Joint inflammation
            "Arthritis": "Rheumatology",                # Joint disease
            "Back Strain": "Orthopedics",               # Back muscle strain
            "Herniated Disc": "Orthopedics",            # Spinal disc problem
            "Chest Infection": "Pulmonology",           # Respiratory infection
            "Respiratory Issue": "Pulmonology",         # Breathing problems
            "Heart Palpitations": "Cardiology",         # Heart rhythm issues
            "Heart Condition": "Cardiology",            # General heart problems
            "Heart Disease": "Cardiology",              # Heart disease
            "Stomach Upset": "Gastroenterology",        # Stomach problems
            "Abdominal Issue": "Gastroenterology",      # Abdominal problems
            "Head Pain": "Neurology",                   # Head/brain issues
            "Migraine": "Neurology",                    # Migraine headaches
            "Skin Irritation": "Dermatology",           # Skin problems
            "Throat Infection": "ENT",                  # Throat/ear problems
            "Sinus Issue": "ENT",                       # Sinus problems
            "Fever Syndrome": "Internal Medicine",      # General fever
            "Head Pain": "Neurology",                   # General headache
            "Chest Pain Syndrome": "Internal Medicine", # General chest pain
            "Joint Pain": "Rheumatology",               # General joint pain
            "Back Strain": "Orthopedics",               # Back pain
            "Dental Pain": "Dentistry",                 # General tooth pain
            "Eye Strain": "Ophthalmology"               # General eye pain
        }

        # Check for real disease match (only once)
        disease_match = find_disease_match(active_symptoms)
        real_disease_info = None
        if disease_match:
            disease_name = disease_match["disease"]
            specialist = disease_specialist_map.get(disease_name, "Internal Medicine")
            real_disease_info = (disease_name, specialist)
            print(f"Final mapping: {active_symptoms} -> {real_disease_info}")

        # SMART DISEASE INFERENCE SYSTEM
        def find_multiple_diseases(symptoms, max_diseases=3):
            """Smart system to find diseases from any symptom combination"""
            found_diseases = []
            used_combinations = set()

            print(f"SMART ANALYSIS: Analyzing {len(symptoms)} symptoms: {symptoms}")

            # Step 1: Try exact matches from comprehensive mapping - FIND ALL POSSIBLE DISEASES
            used_diseases = set()

            for combo_size in range(min(len(symptoms), 4), 1, -1):
                for symptom_combo in combinations(symptoms, combo_size):
                    for combo in [symptom_combo, tuple(sorted(symptom_combo))]:
                        if combo in extended_disease_mapping and combo not in used_combinations:
                            disease_info = extended_disease_mapping[combo]
                            disease_name = disease_info["disease"]

                            # Skip if we already have this disease
                            if disease_name in used_diseases:
                                continue

                            specialist = disease_specialist_map.get(disease_name, "Internal Medicine")

                            found_diseases.append({
                                "disease": disease_name,
                                "confidence": disease_info["confidence"],
                                "specialist": specialist,
                                "symptoms": combo
                            })
                            used_combinations.add(combo)
                            used_diseases.add(disease_name)
                            print(f"EXACT MATCH #{len(found_diseases)}: {combo} -> {disease_name} ({specialist})")

                            if len(found_diseases) >= max_diseases:
                                return found_diseases

            # Step 1.5: If we found some diseases but need more, look for MEDICALLY RELEVANT related diseases
            if found_diseases and len(found_diseases) < max_diseases:
                print(f"EXPANDING SEARCH: Found {len(found_diseases)}, looking for {max_diseases - len(found_diseases)} more...")

                # Look for diseases with flexible overlap requirements
                candidates = []

                for combo in extended_disease_mapping:
                    if combo not in used_combinations:
                        # Count how many symptoms overlap
                        overlap_count = len(set(symptoms) & set(combo))

                        if overlap_count >= 1:  # At least 1 overlapping symptom
                            disease_info = extended_disease_mapping[combo]
                            disease_name = disease_info["disease"]

                            if disease_name not in used_diseases:
                                # Calculate relevance score
                                overlap_ratio = overlap_count / len(combo)
                                base_confidence = disease_info["confidence"]

                                # Prioritize diseases with more overlaps and higher base confidence
                                relevance_score = overlap_count * overlap_ratio * base_confidence

                                candidates.append({
                                    "disease": disease_name,
                                    "confidence": base_confidence * overlap_ratio * 0.7,
                                    "specialist": disease_specialist_map.get(disease_name, "Internal Medicine"),
                                    "symptoms": combo,
                                    "overlap_count": overlap_count,
                                    "relevance_score": relevance_score
                                })

                # Sort by relevance score and take the best ones
                candidates.sort(key=lambda x: x["relevance_score"], reverse=True)

                for candidate in candidates[:max_diseases - len(found_diseases)]:
                    found_diseases.append({
                        "disease": candidate["disease"],
                        "confidence": candidate["confidence"],
                        "specialist": candidate["specialist"],
                        "symptoms": candidate["symptoms"]
                    })
                    used_diseases.add(candidate["disease"])
                    print(f"RELATED MATCH #{len(found_diseases)}: {candidate['symptoms']} -> {candidate['disease']} ({candidate['specialist']}) [overlap: {candidate['overlap_count']}/{len(candidate['symptoms'])}, score: {candidate['relevance_score']:.3f}]")

            # Step 2: Smart inference for unmapped combinations
            if not found_diseases:
                print(f"SMART INFERENCE: No exact matches, using medical logic...")

                # Symptom category analysis
                skin_symptoms = [s for s in symptoms if any(skin_word in s.lower() for skin_word in ['skin', 'rash', 'itch', 'peel', 'burn', 'blister', 'acne', 'dry'])]
                dental_symptoms = [s for s in symptoms if any(dental_word in s.lower() for dental_word in ['tooth', 'dental', 'gum', 'jaw', 'mouth', 'bite'])]
                respiratory_symptoms = [s for s in symptoms if any(resp_word in s.lower() for resp_word in ['cough', 'breath', 'wheez', 'chest', 'lung'])]
                digestive_symptoms = [s for s in symptoms if any(dig_word in s.lower() for dig_word in ['stomach', 'nausea', 'vomit', 'diarr', 'constip', 'abdom'])]
                neuro_symptoms = [s for s in symptoms if any(neuro_word in s.lower() for neuro_word in ['head', 'dizz', 'migr', 'confus', 'memory'])]

                # Generate intelligent diseases based on symptom categories (FIXED: Allow single symptoms)
                if len(skin_symptoms) >= 1:
                    if 'itching' in symptoms and 'skin_rash' in symptoms:
                        found_diseases.append({"disease": "Eczema", "confidence": 0.75, "specialist": "Dermatology", "symptoms": skin_symptoms})
                    elif 'skin_peeling' in symptoms:
                        found_diseases.append({"disease": "Contact Dermatitis", "confidence": 0.7, "specialist": "Dermatology", "symptoms": skin_symptoms})
                    else:
                        found_diseases.append({"disease": "Skin Condition", "confidence": 0.65, "specialist": "Dermatology", "symptoms": skin_symptoms})
                    print(f"INFERRED: Skin condition from {skin_symptoms}")

                if len(dental_symptoms) >= 1:
                    if 'toothache' in symptoms:
                        found_diseases.append({"disease": "Dental Infection", "confidence": 0.8, "specialist": "Dentistry", "symptoms": dental_symptoms})
                    else:
                        found_diseases.append({"disease": "Dental Problem", "confidence": 0.7, "specialist": "Dentistry", "symptoms": dental_symptoms})
                    print(f"INFERRED: Dental condition from {dental_symptoms}")

                if len(respiratory_symptoms) >= 1:
                    found_diseases.append({"disease": "Respiratory Condition", "confidence": 0.7, "specialist": "Pulmonology", "symptoms": respiratory_symptoms})
                    print(f"INFERRED: Respiratory condition from {respiratory_symptoms}")

                if len(digestive_symptoms) >= 1:
                    found_diseases.append({"disease": "Gastrointestinal Disorder", "confidence": 0.7, "specialist": "Gastroenterology", "symptoms": digestive_symptoms})
                    print(f"INFERRED: Digestive condition from {digestive_symptoms}")

                if len(neuro_symptoms) >= 1:
                    found_diseases.append({"disease": "Neurological Condition", "confidence": 0.7, "specialist": "Neurology", "symptoms": neuro_symptoms})
                    print(f"INFERRED: Neurological condition from {neuro_symptoms}")

            return found_diseases[:max_diseases]

        # Get multiple real diseases
        multiple_diseases = find_multiple_diseases(active_symptoms, max_diseases=3)

        if multiple_diseases:
            # Use real diseases for all diagnoses
            for i, disease_info in enumerate(multiple_diseases):
                priority = "PRIMARY" if i == 0 else "SECONDARY"
                print(f"{priority}: {disease_info['disease']} -> {disease_info['specialist']}")

                diagnoses.append({
                    "disease": disease_info["disease"],
                    "probability": disease_info["confidence"],
                    "specialist": disease_info["specialist"],
                    "alternative_specialists": [],
                    "confidence": disease_info["confidence"],
                    "explanation": f"Based on your symptoms, {disease_info['disease']} is {'likely' if i == 0 else 'possible'}. Recommended specialist: {disease_info['specialist']}"
                })

            # NO MORE GENERIC FILLERS - Only show real diseases we found
            print(f"FINAL RESULT: Found {len(multiple_diseases)} real diseases, no generic fillers needed!")
        else:
            # No real disease matches, use ML predictions
            for idx in top_indices:
                predicted_specialist = classes[idx]
                probability = float(proba[idx])
                normalized_specialist = specialist_normalization.get(predicted_specialist, predicted_specialist)

                diagnoses.append({
                    "disease": f"Condition requiring {normalized_specialist} consultation",
                    "probability": probability,
                    "specialist": normalized_specialist,
                    "alternative_specialists": [],
                    "confidence": probability,
                    "explanation": f"Based on your symptoms, we recommend consulting with a {normalized_specialist} specialist."
                })
                print(f"ML ONLY: Generic -> {normalized_specialist}")

            # Debug output
            print(f"Prediction {idx+1}: {predicted_specialist} -> {normalized_specialist} (prob: {probability:.6f})")
        print(f"Top diagnoses: {diagnoses}")

        # Extract specialists from diagnoses for backend compatibility (preserve order!)
        specialists = []
        for diag in diagnoses:
            if diag['specialist'] not in specialists:
                specialists.append(diag['specialist'])

        # Primary specialist is the TOP prediction (first in diagnoses list)
        primary_specialist = diagnoses[0]['specialist'] if diagnoses else "General Practitioner"
        print(f"Primary specialist selected: {primary_specialist}")

        # Return format expected by backend
        return {
            "diagnoses": diagnoses,
            "predicted_specialist": primary_specialist,
            "confidence": diagnoses[0]['confidence'] if diagnoses else 0.6,
            "suggested_diseases": [diag['disease'] for diag in diagnoses],
            "active_symptoms": active_symptoms,
            "ml_prediction": primary_specialist,
            "disease_based_specialists": specialists
        }
    except Exception as e:
        print(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002) 