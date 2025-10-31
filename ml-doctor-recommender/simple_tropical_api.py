from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Simple tropical disease mapping
TROPICAL_DISEASES = {
    ("fever", "chills", "headache", "muscle_aches"): {"disease": "Malaria", "specialist": "Infectious Disease", "confidence": 0.77},
    ("fever", "headache", "abdominal_pain", "diarrhea"): {"disease": "Typhoid Fever", "specialist": "Infectious Disease", "confidence": 0.74},
    ("fever", "skin_rash", "joint_pain", "pain_behind_the_eyes"): {"disease": "Dengue Fever", "specialist": "Infectious Disease", "confidence": 0.75},
    ("diarrhea", "vomiting", "dehydration"): {"disease": "Cholera", "specialist": "Infectious Disease", "confidence": 0.75},
    ("cough", "fever", "weight_loss", "night_sweats"): {"disease": "Tuberculosis", "specialist": "Pulmonology", "confidence": 0.78},
}

class SymptomRequest(BaseModel):
    symptoms: dict

@app.post("/predict")
async def predict(request: SymptomRequest):
    active_symptoms = [k for k, v in request.symptoms.items() if v]
    
    # Find matching disease
    for symptom_combo, disease_info in TROPICAL_DISEASES.items():
        if all(s in active_symptoms for s in symptom_combo):
            return {
                "diagnoses": [{
                    "disease": disease_info["disease"],
                    "specialist": disease_info["specialist"],
                    "confidence": disease_info["confidence"],
                    "probability": disease_info["confidence"]
                }],
                "predicted_specialist": disease_info["specialist"],
                "confidence": disease_info["confidence"]
            }
    
    return {"diagnoses": [], "predicted_specialist": "General Practitioner", "confidence": 0.6}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)