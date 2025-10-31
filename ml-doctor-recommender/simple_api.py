from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random

app = FastAPI()

class SymptomRequest(BaseModel):
    symptoms: dict

# Simple rule-based disease prediction for testing
SYMPTOM_DISEASE_MAPPING = {
    'chest_pain': [
        {'disease': 'Heart Disease', 'probability': 0.85, 'specialist': 'Cardiology'},
        {'disease': 'Anxiety', 'probability': 0.65, 'specialist': 'Psychiatry'},
        {'disease': 'Acid Reflux', 'probability': 0.45, 'specialist': 'Gastroenterology'}
    ],
    'headache': [
        {'disease': 'Migraine', 'probability': 0.75, 'specialist': 'Neurology'},
        {'disease': 'Tension Headache', 'probability': 0.85, 'specialist': 'Family Medicine'},
        {'disease': 'Hypertension', 'probability': 0.55, 'specialist': 'Cardiology'}
    ],
    'abdominal_pain': [
        {'disease': 'Gastritis', 'probability': 0.70, 'specialist': 'Gastroenterology'},
        {'disease': 'Appendicitis', 'probability': 0.60, 'specialist': 'General Surgery'},
        {'disease': 'IBS', 'probability': 0.65, 'specialist': 'Gastroenterology'}
    ],
    'cough': [
        {'disease': 'Bronchitis', 'probability': 0.75, 'specialist': 'Pulmonology'},
        {'disease': 'Common Cold', 'probability': 0.80, 'specialist': 'Family Medicine'},
        {'disease': 'Asthma', 'probability': 0.60, 'specialist': 'Pulmonology'}
    ],
    'fever': [
        {'disease': 'Viral Infection', 'probability': 0.80, 'specialist': 'Family Medicine'},
        {'disease': 'Bacterial Infection', 'probability': 0.65, 'specialist': 'Internal Medicine'},
        {'disease': 'Flu', 'probability': 0.70, 'specialist': 'Family Medicine'}
    ],
    'fatigue': [
        {'disease': 'Anemia', 'probability': 0.60, 'specialist': 'Internal Medicine'},
        {'disease': 'Depression', 'probability': 0.55, 'specialist': 'Psychiatry'},
        {'disease': 'Thyroid Disorder', 'probability': 0.50, 'specialist': 'Endocrinology'}
    ],
    'joint_pain': [
        {'disease': 'Arthritis', 'probability': 0.75, 'specialist': 'Rheumatology'},
        {'disease': 'Fibromyalgia', 'probability': 0.55, 'specialist': 'Rheumatology'},
        {'disease': 'Lupus', 'probability': 0.45, 'specialist': 'Rheumatology'}
    ],
    'skin_rash': [
        {'disease': 'Eczema', 'probability': 0.70, 'specialist': 'Dermatology'},
        {'disease': 'Allergic Reaction', 'probability': 0.65, 'specialist': 'Allergy & Immunology'},
        {'disease': 'Psoriasis', 'probability': 0.50, 'specialist': 'Dermatology'}
    ],
    'itching': [
        {'disease': 'Eczema', 'probability': 0.75, 'specialist': 'Dermatology'},
        {'disease': 'Allergic Reaction', 'probability': 0.70, 'specialist': 'Allergy & Immunology'},
        {'disease': 'Contact Dermatitis', 'probability': 0.60, 'specialist': 'Dermatology'}
    ],
    'nausea': [
        {'disease': 'Gastroenteritis', 'probability': 0.75, 'specialist': 'Gastroenterology'},
        {'disease': 'Food Poisoning', 'probability': 0.70, 'specialist': 'Family Medicine'},
        {'disease': 'Migraine', 'probability': 0.45, 'specialist': 'Neurology'}
    ],
    'dizziness': [
        {'disease': 'Vertigo', 'probability': 0.70, 'specialist': 'ENT'},
        {'disease': 'Low Blood Pressure', 'probability': 0.60, 'specialist': 'Cardiology'},
        {'disease': 'Inner Ear Infection', 'probability': 0.55, 'specialist': 'ENT'}
    ]
}

# Enhanced specialist mapping
SPECIALIST_MAPPING = {
    "Cardiology": {"primary": "Cardiology", "secondary": ["Internal Medicine", "Family Medicine"], "confidence": 0.90},
    "Neurology": {"primary": "Neurology", "secondary": ["Family Medicine"], "confidence": 0.85},
    "Gastroenterology": {"primary": "Gastroenterology", "secondary": ["Internal Medicine"], "confidence": 0.85},
    "Pulmonology": {"primary": "Pulmonology", "secondary": ["Internal Medicine"], "confidence": 0.80},
    "Family Medicine": {"primary": "Family Medicine", "secondary": ["Internal Medicine"], "confidence": 0.75},
    "Internal Medicine": {"primary": "Internal Medicine", "secondary": ["Family Medicine"], "confidence": 0.80},
    "Psychiatry": {"primary": "Psychiatry", "secondary": ["Psychology"], "confidence": 0.85},
    "Endocrinology": {"primary": "Endocrinology", "secondary": ["Internal Medicine"], "confidence": 0.80},
    "Rheumatology": {"primary": "Rheumatology", "secondary": ["Internal Medicine"], "confidence": 0.85},
    "Dermatology": {"primary": "Dermatology", "secondary": ["Family Medicine"], "confidence": 0.90},
    "Allergy & Immunology": {"primary": "Allergy & Immunology", "secondary": ["Dermatology"], "confidence": 0.80},
    "General Surgery": {"primary": "General Surgery", "secondary": ["Emergency Medicine"], "confidence": 0.85},
    "ENT": {"primary": "ENT", "secondary": ["Family Medicine"], "confidence": 0.80}
}

@app.get("/")
async def root():
    return {"message": "Simple Doctor Recommender API is running!"}

@app.post("/predict")
async def predict_specialist(request: SymptomRequest):
    try:
        symptoms = request.symptoms
        print(f"Received symptoms: {symptoms}")
        
        # Get active symptoms
        active_symptoms = [symptom for symptom, value in symptoms.items() if value == True]
        print(f"Active symptoms: {active_symptoms}")
        
        if not active_symptoms:
            return {"diagnoses": []}
        
        # Collect all possible diagnoses
        all_diagnoses = []
        
        for symptom in active_symptoms:
            if symptom in SYMPTOM_DISEASE_MAPPING:
                for diagnosis in SYMPTOM_DISEASE_MAPPING[symptom]:
                    # Check if this disease is already in our list
                    existing = next((d for d in all_diagnoses if d['disease'] == diagnosis['disease']), None)
                    if existing:
                        # Increase probability if symptom supports this disease
                        existing['probability'] = min(0.95, existing['probability'] + 0.1)
                        existing['symptom_count'] += 1
                    else:
                        # Add new diagnosis
                        new_diagnosis = diagnosis.copy()
                        new_diagnosis['symptom_count'] = 1
                        all_diagnoses.append(new_diagnosis)
        
        # Sort by probability and symptom count
        all_diagnoses.sort(key=lambda x: (x['symptom_count'], x['probability']), reverse=True)
        
        # Get top 3 diagnoses
        top_diagnoses = all_diagnoses[:3]
        
        # Enhance with specialist information
        enhanced_diagnoses = []
        for diag in top_diagnoses:
            specialist_info = SPECIALIST_MAPPING.get(diag['specialist'], {
                "primary": diag['specialist'], 
                "secondary": ["General Practitioner"], 
                "confidence": 0.70
            })
            
            enhanced_diagnoses.append({
                "disease": diag['disease'],
                "probability": diag['probability'],
                "specialist": specialist_info["primary"],
                "alternative_specialists": specialist_info["secondary"],
                "confidence": specialist_info["confidence"],
                "explanation": f"Based on your symptoms, {diag['disease']} is a likely diagnosis. {specialist_info['primary']} specialists are best equipped to diagnose and treat this condition."
            })
        
        # If no specific matches, provide general recommendation
        if not enhanced_diagnoses:
            enhanced_diagnoses = [{
                "disease": "General Health Concern",
                "probability": 0.60,
                "specialist": "General Practitioner",
                "alternative_specialists": ["Family Medicine"],
                "confidence": 0.60,
                "explanation": "Based on your symptoms, we recommend starting with a General Practitioner for comprehensive evaluation."
            }]
        
        print(f"Returning {len(enhanced_diagnoses)} diagnoses")

        # Extract specialists from diagnoses
        specialists = list(set([diag['specialist'] for diag in enhanced_diagnoses]))
        primary_specialist = specialists[0] if specialists else "General Practitioner"

        # Return format expected by backend
        return {
            "diagnoses": enhanced_diagnoses,
            "predicted_specialist": primary_specialist,
            "confidence": enhanced_diagnoses[0]['confidence'] if enhanced_diagnoses else 0.6,
            "suggested_diseases": [diag['disease'] for diag in enhanced_diagnoses],
            "active_symptoms": active_symptoms,
            "ml_prediction": primary_specialist,
            "disease_based_specialists": specialists
        }
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
