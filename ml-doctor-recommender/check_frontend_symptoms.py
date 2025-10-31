# Frontend symptoms from home.js
frontend_symptoms = [
  "fever", "cough", "headache", "chest_pain", "abdominal_pain", "nausea", "vomiting", 
  "diarrhoea", "constipation", "joint_pain", "back_pain", "muscle_weakness", "fatigue", 
  "dizziness", "shortness_of_breath", "palpitations", "skin_rash", "itching", "red_eyes", 
  "visual_disturbances", "hearing_loss", "sore_throat", "runny_nose", "swelling_joints", 
  "weight_loss", "weight_gain", "anxiety", "depression", "irregular_sugar_level", 
  "excessive_hunger", "abnormal_menstruation", "painful_urination", "blood_in_urine", 
  "night_sweats", "loss_of_appetite", "blurred_and_distorted_vision"
]

# Model symptoms (with spaces)
model_symptoms = [
    'itching', ' skin_rash', 'cough', ' loss_of_appetite', ' sweating', 
    ' joint_pain', ' chills', ' nausea', ' diarrhoea', ' malaise',
    ' abdominal_pain', ' weight_loss', ' lethargy', ' breathlessness', 
    ' dizziness', ' loss_of_balance', ' muscle_pain', ' mild_fever',
    ' swelled_lymph_nodes', ' phlegm', ' continuous_sneezing', ' stomach_pain',
    ' acidity', ' yellowish_skin', ' yellowing_of_eyes', ' burning_micturition',
    ' indigestion', ' blurred_and_distorted_vision', ' obesity', ' excessive_hunger',
    ' family_history', ' stiff_neck', ' depression', ' irritability', ' back_pain',
    ' neck_pain', ' dark_urine', ' red_spots_over_body', ' constipation',
    ' fast_heart_rate', ' muscle_weakness', ' swelling_joints', ' painful_walking'
]

print("Frontend symptoms that need mapping:")
for symptom in frontend_symptoms:
    # Check if it exists in model symptoms
    found = False
    for model_symptom in model_symptoms:
        if symptom.strip() == model_symptom.strip():
            found = True
            break
    if not found:
        print(f"  '{symptom}' → needs mapping")

print("\nSuggested mapping for frontend symptoms:")
mapping = {
    "fever": " mild_fever",
    "cough": "cough", 
    "headache": " headache",
    "chest_pain": " chest_pain",
    "abdominal_pain": " abdominal_pain",
    "nausea": " nausea",
    "vomiting": " vomiting",
    "diarrhoea": " diarrhoea",
    "constipation": " constipation",
    "joint_pain": " joint_pain",
    "back_pain": " back_pain",
    "muscle_weakness": " muscle_weakness",
    "fatigue": " lethargy",
    "dizziness": " dizziness",
    "shortness_of_breath": " breathlessness",
    "palpitations": " fast_heart_rate",
    "skin_rash": " skin_rash",
    "itching": "itching",
    "red_eyes": " redness_of_eyes",
    "visual_disturbances": " blurred_and_distorted_vision",
    "hearing_loss": " hearing_loss",
    "sore_throat": " throat_irritation",
    "runny_nose": " runny_nose",
    "swelling_joints": " swelling_joints",
    "weight_loss": " weight_loss",
    "weight_gain": " obesity",
    "anxiety": " irritability",
    "depression": " depression",
    "irregular_sugar_level": " irregular_sugar_level",
    "excessive_hunger": " excessive_hunger",
    "abnormal_menstruation": " abnormal_menstruation",
    "painful_urination": " burning_micturition",
    "blood_in_urine": " dark_urine",
    "night_sweats": " sweating",
    "loss_of_appetite": " loss_of_appetite",
    "blurred_and_distorted_vision": " blurred_and_distorted_vision"
}

for frontend_symptom, model_symptom in mapping.items():
    print(f"  '{frontend_symptom}' → '{model_symptom}'") 