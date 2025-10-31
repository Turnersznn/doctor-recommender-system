from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import pickle

app = FastAPI()

# Load the trained ML model
model = joblib.load("content_model_specialist_fixed.pkl")

# Load the feature columns
with open('feature_columns.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

# Import the enhanced mapping from content_api
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from content_api import disease_to_specialist_mapping, get_specialist_recommendation

# Disease-Specialist mapping based on common medical knowledge
DISEASE_SPECIALIST_MAPPING = {
    # Dermatology
    "Skin Rash": "Dermatologist",
    "Acne": "Dermatologist", 
    "Eczema": "Dermatologist",
    "Psoriasis": "Dermatologist",
    "Skin Infection": "Dermatologist",
    
    # Neurology
    "Headache": "Neurologist",
    "Migraine": "Neurologist",
    "Seizures": "Neurologist",
    "Stroke": "Neurologist",
    "Multiple Sclerosis": "Neurologist",
    "Parkinson's Disease": "Neurologist",
    
    # Gastroenterology
    "Stomach Pain": "Gastroenterologist",
    "Acid Reflux": "Gastroenterologist",
    "Ulcer": "Gastroenterologist",
    "Inflammatory Bowel Disease": "Gastroenterologist",
    "Liver Disease": "Gastroenterologist",
    "Gallbladder Disease": "Gastroenterologist",
    
    # Pulmonology
    "Cough": "Pulmonologist",
    "Shortness of Breath": "Pulmonologist",
    "Asthma": "Pulmonologist",
    "Pneumonia": "Pulmonologist",
    "COPD": "Pulmonologist",
    "Lung Cancer": "Pulmonologist",
    
    # Cardiology
    "Chest Pain": "Cardiologist",
    "Heart Attack": "Cardiologist",
    "Heart Failure": "Cardiologist",
    "Arrhythmia": "Cardiologist",
    "High Blood Pressure": "Cardiologist",
    "Coronary Artery Disease": "Cardiologist",
    
    # Ophthalmology
    "Vision Problems": "Ophthalmologist",
    "Eye Pain": "Ophthalmologist",
    "Cataracts": "Ophthalmologist",
    "Glaucoma": "Ophthalmologist",
    "Retinal Disease": "Ophthalmologist",
    "Eye Infection": "Ophthalmologist",
    
    # Endocrinology
    "Diabetes": "Endocrinologist",
    "Thyroid Problems": "Endocrinologist",
    "Hormone Imbalance": "Endocrinologist",
    "Obesity": "Endocrinologist",
    "Metabolic Disorder": "Endocrinologist",
    
    # Rheumatology
    "Joint Pain": "Rheumatologists",
    "Arthritis": "Rheumatologists",
    "Lupus": "Rheumatologists",
    "Fibromyalgia": "Rheumatologists",
    "Autoimmune Disease": "Rheumatologists",
    
    # Allergy & Immunology
    "Allergies": "Allergist",
    "Hay Fever": "Allergist",
    "Food Allergies": "Allergist",
    "Asthma": "Allergist",
    "Immune System Disorders": "Allergist",
    
    # Gynecology
    "Menstrual Problems": "Gynecologist",
    "Pregnancy": "Gynecologist",
    "Ovarian Cysts": "Gynecologist",
    "Endometriosis": "Gynecologist",
    "Menopause": "Gynecologist"
}

# Symptom to Disease mapping
SYMPTOM_DISEASE_MAPPING = {
    # Skin symptoms
    "itching": "Skin Rash",
    "skin_rash": "Skin Rash", 
    "nodal_skin_eruptions": "Skin Infection",
    "dischromic _patches": "Skin Rash",
    "blister": "Skin Infection",
    "red_sore_around_nose": "Skin Infection",
    "yellow_crust_ooze": "Skin Infection",
    
    # Neurological symptoms
    "headache": "Headache",
    "altered_sensorium": "Neurological Disorder",
    "slurred_speech": "Stroke",
    "spinning_movements": "Vertigo",
    "unsteadiness": "Balance Disorder",
    "weakness_of_one_body_side": "Stroke",
    
    # Gastrointestinal symptoms
    "stomach_pain": "Stomach Pain",
    "abdominal_pain": "Stomach Pain",
    "belly_pain": "Stomach Pain",
    "acidity": "Acid Reflux",
    "ulcers_on_tongue": "Oral Ulcers",
    "vomiting": "Gastroenteritis",
    "nausea": "Gastroenteritis",
    "loss_of_appetite": "Gastroenteritis",
    "indigestion": "Indigestion",
    "constipation": "Constipation",
    "diarrhoea": "Diarrhea",
    
    # Respiratory symptoms
    "cough": "Cough",
    "chest_pain": "Chest Pain",
    "shortness_of_breath": "Shortness of Breath",
    "phlegm": "Respiratory Infection",
    "blood_in_sputum": "Respiratory Infection",
    "rusty_sputum": "Respiratory Infection",
    
    # Cardiovascular symptoms
    "palpitations": "Heart Arrhythmia",
    "fast_heart_rate": "Tachycardia",
    "chest_pain": "Chest Pain",
    
    # Eye symptoms
    "watering_from_eyes": "Eye Irritation",
    "redness_of_eyes": "Eye Infection",
    "blurred_and_distorted_vision": "Vision Problems",
    "pain_behind_the_eyes": "Eye Pain",
    
    # Endocrine symptoms
    "irregular_sugar_level": "Diabetes",
    "excessive_hunger": "Diabetes",
    "increased_appetite": "Diabetes",
    "polyuria": "Diabetes",
    "weight_loss": "Weight Loss",
    "weight_gain": "Weight Gain",
    "obesity": "Obesity",
    
    # Rheumatological symptoms
    "joint_pain": "Joint Pain",
    "back_pain": "Back Pain",
    "neck_pain": "Neck Pain",
    "knee_pain": "Knee Pain",
    "hip_joint_pain": "Hip Pain",
    "swelling_joints": "Arthritis",
    "painful_walking": "Joint Pain",
    "movement_stiffness": "Arthritis",
    
    # General symptoms
    "fever": "Fever",
    "high_fever": "High Fever",
    "mild_fever": "Mild Fever",
    "fatigue": "Fatigue",
    "weakness_in_limbs": "Muscle Weakness",
    "muscle_pain": "Muscle Pain",
    "muscle_weakness": "Muscle Weakness",
    "anxiety": "Anxiety",
    "depression": "Depression"
}

class SymptomRequest(BaseModel):
    symptoms: dict

@app.post("/predict")
async def predict_specialist(request: SymptomRequest):
    try:
        symptoms = request.symptoms
        print(f"FastAPI received symptoms: {symptoms}")
        
        # Get all active symptoms (value = True)
        active_symptoms = [symptom for symptom, value in symptoms.items() if value == True]
        print(f"Active symptoms: {active_symptoms}")
        
        # Step 1: Predict specialist using ML model
        input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
        
        for symptom in active_symptoms:
            if symptom in feature_columns:
                input_data[symptom] = 1
        
        predicted_specialist = model.predict(input_data)[0]
        print(f"ML Model prediction: {predicted_specialist}")
        
        # Step 2: Get disease probabilities (if available from model)
        try:
            # Try to get probabilities for disease prediction
            proba = model.predict_proba(input_data)[0] if hasattr(model, 'predict_proba') else None
            classes = model.classes_ if hasattr(model, 'classes_') else None

            diagnoses = []
            if proba is not None and classes is not None:
                # Get top 3 diseases with highest probability
                top_indices = proba.argsort()[-3:][::-1]
                for idx in top_indices:
                    disease = classes[idx]
                    probability = float(proba[idx])

                    # Get enhanced specialist recommendation
                    specialist_info = get_specialist_recommendation(disease, probability)

                    diagnoses.append({
                        "disease": disease,
                        "probability": probability,
                        "specialist": specialist_info["primary"],
                        "alternative_specialists": specialist_info["secondary"],
                        "confidence": specialist_info["confidence"],
                        "explanation": specialist_info["explanation"]
                    })
            else:
                # Fallback: use predicted specialist directly
                specialist_info = get_specialist_recommendation(predicted_specialist, 0.8)
                diagnoses.append({
                    "disease": predicted_specialist,
                    "probability": 0.8,
                    "specialist": specialist_info["primary"],
                    "alternative_specialists": specialist_info["secondary"],
                    "confidence": specialist_info["confidence"],
                    "explanation": specialist_info["explanation"]
                })

        except Exception as e:
            print(f"Error getting probabilities: {e}")
            # Fallback to basic prediction
            specialist_info = get_specialist_recommendation(predicted_specialist, 0.7)
            diagnoses = [{
                "disease": predicted_specialist,
                "probability": 0.7,
                "specialist": specialist_info["primary"],
                "alternative_specialists": specialist_info["secondary"],
                "confidence": specialist_info["confidence"],
                "explanation": specialist_info["explanation"]
            }]

        return {
            "diagnoses": diagnoses,
            "active_symptoms": active_symptoms,
            "ml_prediction": predicted_specialist,
            "total_symptoms": len(active_symptoms)
        }
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001) 