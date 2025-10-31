from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from multi_symptom_mapper import get_multi_symptom_recommendations
from content_api import disease_to_specialist_mapping

app = FastAPI()

class SymptomRequest(BaseModel):
    symptoms: dict

@app.get("/")
async def root():
    return {"message": "Pure Multi-Symptom Recommendation API Running"}

@app.post("/predict")
async def predict_specialist(request: SymptomRequest):
    try:
        symptoms = request.symptoms
        print(f"FastAPI received symptoms: {symptoms}")
        
        # Get all active symptoms (value = True)
        active_symptoms = [symptom for symptom, value in symptoms.items() if value == True and symptom != 'followupanswers']
        print(f"Active symptoms: {active_symptoms}")
        
        # If no active symptoms, return empty response
        if not active_symptoms:
            return {
                "diagnoses": [],
                "predicted_specialist": "General Practitioner",
                "confidence": 0.6,
                "suggested_diseases": [],
                "active_symptoms": [],
                "ml_prediction": "General Practitioner",
                "disease_based_specialists": ["General Practitioner"],
                "message": "No active symptoms provided"
            }
        
        # Use multi-symptom mapper to get disease and specialist recommendations
        multi_symptom_diagnoses = get_multi_symptom_recommendations(active_symptoms, disease_to_specialist_mapping)
        
        print(f"Multi-symptom diagnoses: {multi_symptom_diagnoses}")
        
        # If no multi-symptom matches found, return general practitioner
        if not multi_symptom_diagnoses:
            return {
                "diagnoses": [{
                    "disease": "General Assessment Needed",
                    "probability": 0.6,
                    "specialist": "General Practitioner",
                    "alternative_specialists": ["Internal Medicine"],
                    "confidence": 0.6,
                    "explanation": "No specific disease pattern identified. Recommend starting with a General Practitioner for initial assessment.",
                    "matching_symptoms": active_symptoms
                }],
                "predicted_specialist": "General Practitioner",
                "confidence": 0.6,
                "suggested_diseases": ["General Assessment Needed"],
                "active_symptoms": active_symptoms,
                "ml_prediction": "General Practitioner",
                "disease_based_specialists": ["General Practitioner"]
            }
        
        # Convert multi-symptom results to the expected format
        diagnoses = []
        specialists = []
        
        for result in multi_symptom_diagnoses:
            diagnosis = {
                "disease": result["disease"],
                "probability": result["probability"],
                "specialist": result["specialist"],
                "alternative_specialists": result.get("alternative_specialists", []),
                "confidence": result["confidence"],
                "explanation": result.get("explanation", f"Based on symptoms matching {result['disease']}"),
                "matching_symptoms": result.get("matching_symptoms", active_symptoms)
            }
            diagnoses.append(diagnosis)
            
            # Collect unique specialists
            if result["specialist"] not in specialists:
                specialists.append(result["specialist"])
            for alt_spec in result.get("alternative_specialists", []):
                if alt_spec not in specialists:
                    specialists.append(alt_spec)
        
        # Primary specialist is the top recommendation
        primary_specialist = diagnoses[0]["specialist"] if diagnoses else "General Practitioner"
        
        print(f"🎯 Primary specialist selected: {primary_specialist}")
        print(f"📋 Total diagnoses: {len(diagnoses)}")
        
        # Return format expected by backend
        response_data = {
            "diagnoses": diagnoses,
            "predicted_specialist": primary_specialist,
            "confidence": diagnoses[0]["confidence"] if diagnoses else 0.6,
            "suggested_diseases": [diag["disease"] for diag in diagnoses],
            "active_symptoms": active_symptoms,
            "ml_prediction": primary_specialist,
            "disease_based_specialists": specialists
        }
        
        print(f"🚀 Returning response: {response_data}")
        return response_data
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003)
