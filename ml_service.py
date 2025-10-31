from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class SymptomRequest(BaseModel):
    symptoms: dict

@app.get("/")
async def root():
    return {"message": "ML Service Running"}

@app.post("/predict")
async def predict(request: SymptomRequest):
    symptoms = request.symptoms
    active = [s for s, v in symptoms.items() if v]
    
    diseases = {
        'chest_pain': [{'disease': 'Heart Disease', 'probability': 0.85, 'specialist': 'Cardiology'}],
        'headache': [{'disease': 'Migraine', 'probability': 0.75, 'specialist': 'Neurology'}],
        'fatigue': [{'disease': 'Anemia', 'probability': 0.60, 'specialist': 'Internal Medicine'}]
    }
    
    diagnoses = []
    for symptom in active:
        if symptom in diseases:
            for disease in diseases[symptom]:
                diagnoses.append({
                    'disease': disease['disease'],
                    'probability': disease['probability'],
                    'specialist': disease['specialist'],
                    'confidence': 0.8
                })
    
    return {'diagnoses': diagnoses[:3]}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
