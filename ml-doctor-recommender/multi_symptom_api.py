from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import pickle
from typing import List, Dict, Any

# Import the multi-symptom mapper
from multi_symptom_mapper import get_multi_symptom_recommendations

# Import the disease-to-specialist mapping from content_api
from content_api import disease_to_specialist_mapping, get_specialist_recommendation

app = FastAPI()

# Load the trained ML model
try:
    model = joblib.load("content_model_SIMPLE_HIGH_CONFIDENCE.pkl")
    # Load the feature columns
    with open('feature_columns_SIMPLE_HIGH_CONFIDENCE.pkl', 'rb') as f:
        feature_columns = pickle.load(f)
    print("Loaded SIMPLE_HIGH_CONFIDENCE model")
except Exception as e:
    print(f"Error loading SIMPLE_HIGH_CONFIDENCE model: {e}")
    try:
        model = joblib.load("content_model_specialist_fixed.pkl")
        # Load the feature columns
        with open('feature_columns.pkl', 'rb') as f:
            feature_columns = pickle.load(f)
        print("Loaded specialist_fixed model as fallback")
    except Exception as e:
        print(f"Error loading fallback model: {e}")
        model = None
        feature_columns = []

class SymptomRequest(BaseModel):
    symptoms: dict

@app.get("/")
async def root():
    return {"message": "Multi-Symptom Recommendation API Running"}

@app.post("/predict")
async def predict_specialist(request: SymptomRequest):
    try:
        symptoms = request.symptoms
        print(f"FastAPI received symptoms: {symptoms}")
        
        # Get all active symptoms (value = True)
        active_symptoms = [symptom for symptom, value in symptoms.items() if value == True]
        print(f"Active symptoms: {active_symptoms}")
        
        # If no active symptoms, return empty response
        if not active_symptoms:
            return {
                "diagnoses": [],
                "message": "No active symptoms provided"
            }
        
        # Step 1: Get multi-symptom based recommendations
        multi_symptom_diagnoses = get_multi_symptom_recommendations(active_symptoms, disease_to_specialist_mapping)
        
        # Step 2: If we have a model, also get ML-based recommendations
        ml_diagnoses = []
        if model is not None and feature_columns:
            # Prepare input for the ML model
            input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
            
            for symptom in active_symptoms:
                if symptom in feature_columns:
                    input_data[symptom] = 1
            
            # Get ML predictions
            try:
                # Predict probabilities for all diseases
                proba = model.predict_proba(input_data)[0]
                classes = model.classes_
                # Get top 3 specialists with highest probability
                top_indices = proba.argsort()[-3:][::-1]
                
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
                    'Internal Medcine': 'Internal Medicine',
                    'Hepatologist': 'Hepatology',
                    'Gynecologist': 'Gynecology',
                    'Pediatrician': 'Pediatrics',
                    'Dentist': 'Dentistry',
                }
                
                for idx in top_indices:
                    predicted_specialist = classes[idx]
                    probability = float(proba[idx])
                    
                    # Skip very low probability predictions
                    if probability < 0.1:
                        continue
                    
                    # Normalize specialist name
                    normalized_specialist = specialist_normalization.get(predicted_specialist, predicted_specialist)
                    
                    # Get enhanced specialist recommendation
                    specialist_info = get_specialist_recommendation(normalized_specialist, probability)
                    
                    ml_diagnoses.append({
                        "disease": f"Condition requiring {normalized_specialist} consultation",
                        "probability": probability,
                        "specialist": specialist_info["primary"],
                        "alternative_specialists": specialist_info["secondary"],
                        "confidence": specialist_info["confidence"],
                        "explanation": specialist_info["explanation"],
                        "source": "ml_model"
                    })
            except Exception as e:
                print(f"Error in ML prediction: {e}")
        
        # Step 3: Combine and rank all diagnoses
        # Add source information to multi-symptom diagnoses
        for diagnosis in multi_symptom_diagnoses:
            diagnosis["source"] = "symptom_mapping"
            # Ensure explanation field exists
            if "explanation" not in diagnosis:
                diagnosis["explanation"] = f"Based on symptoms matching {diagnosis['disease']}"
        
        # Combine all diagnoses
        all_diagnoses = multi_symptom_diagnoses + ml_diagnoses
        
        # Sort by confidence (highest first)
        all_diagnoses.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Limit to top 5 diagnoses
        top_diagnoses = all_diagnoses[:5]
        
        # Extract specialists from diagnoses (preserve order!)
        specialists = []
        for diag in top_diagnoses:
            if diag['specialist'] not in specialists:
                specialists.append(diag['specialist'])
        
        # Primary specialist is the TOP prediction (first in diagnoses list)
        primary_specialist = top_diagnoses[0]['specialist'] if top_diagnoses else "General Practitioner"
        
        # Return format expected by backend
        response_data = {
            "diagnoses": top_diagnoses,
            "predicted_specialist": primary_specialist,
            "confidence": top_diagnoses[0]['confidence'] if top_diagnoses else 0.6,
            "suggested_diseases": [diag['disease'] for diag in top_diagnoses],
            "active_symptoms": active_symptoms,
            "ml_prediction": primary_specialist,
            "disease_based_specialists": specialists
        }
        
        # Ensure all diagnoses have required fields
        for diag in response_data["diagnoses"]:
            if "explanation" not in diag or diag["explanation"] is None:
                diag["explanation"] = f"Based on symptoms matching {diag['disease']}"
        
        return response_data
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)