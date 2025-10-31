import pandas as pd
import joblib
from rule_based_model import RuleBasedSpecialistPredictor

# Define clinical symptom-specialist mappings
symptom_specialist_rules = {
    # Gastrointestinal symptoms
    ' nausea': 'Gastroenterologist',
    ' vomiting': 'Gastroenterologist',
    ' abdominal_pain': 'Gastroenterologist',
    ' diarrhoea': 'Gastroenterologist',
    ' constipation': 'Gastroenterologist',
    ' stomach_pain': 'Gastroenterologist',
    ' indigestion': 'Gastroenterologist',
    ' acidity': 'Gastroenterologist',
    
    # Neurological symptoms
    ' headache': 'Neurologist',
    ' dizziness': 'Neurologist',
    ' back_pain': 'Neurologist',
    ' muscle_weakness': 'Neurologist',
    ' loss_of_balance': 'Neurologist',
    ' altered_sensorium': 'Neurologist',
    ' slurred_speech': 'Neurologist',
    
    # Cardiovascular symptoms
    ' chest_pain': 'Cardiologist',
    ' fast_heart_rate': 'Cardiologist',
    ' palpitations': 'Cardiologist',
    
    # Respiratory symptoms
    ' breathlessness': 'Pulmonologist',
    'cough': 'Pulmonologist',
    ' phlegm': 'Pulmonologist',
    ' blood_in_sputum': 'Pulmonologist',
    ' rusty_sputum': 'Pulmonologist',
    
    # Dermatological symptoms
    ' skin_rash': 'Dermatologist',
    'itching': 'Dermatologist',
    ' nodal_skin_eruptions': 'Dermatologist',
    ' dischromic _patches': 'Dermatologist',
    ' pus_filled_pimples': 'Dermatologist',
    ' blackheads': 'Dermatologist',
    ' blister': 'Dermatologist',
    
    # Rheumatological symptoms
    ' joint_pain': 'Rheumatologists',
    ' swelling_joints': 'Rheumatologists',
    ' painful_walking': 'Rheumatologists',
    ' movement_stiffness': 'Rheumatologists',
    
    # Endocrine symptoms
    ' irregular_sugar_level': 'Endocrinologist',
    ' excessive_hunger': 'Endocrinologist',
    ' weight_loss': 'Endocrinologist',
    ' weight_gain': 'Endocrinologist',
    ' obesity': 'Endocrinologist',
    ' polyuria': 'Endocrinologist',
    ' enlarged_thyroid': 'Endocrinologist',
    
    # General symptoms (default to Internal Medicine)
    ' fatigue': 'Internal Medcine',
    ' mild_fever': 'Internal Medcine',
    ' high_fever': 'Internal Medcine',
    ' chills': 'Internal Medcine',
    ' sweating': 'Internal Medcine',
    ' loss_of_appetite': 'Internal Medcine',
    ' malaise': 'Internal Medcine',
    ' lethargy': 'Internal Medcine',
    
    # Urological symptoms
    ' burning_micturition': 'Urologist',
    ' dark_urine': 'Urologist',
    ' bladder_discomfort': 'Urologist',
    
    # ENT symptoms
    ' throat_irritation': 'Otolaryngologist',
    ' runny_nose': 'Otolaryngologist',
    ' continuous_sneezing': 'Otolaryngologist',
    ' loss_of_smell': 'Otolaryngologist',
    
    # Eye symptoms
    ' blurred_and_distorted_vision': 'Ophthalmologist',
    'blurred_and_distorted_vision': 'Ophthalmologist',
    ' visual_disturbances': 'Ophthalmologist',
    'visual_disturbances': 'Ophthalmologist',
    ' redness_of_eyes': 'Ophthalmologist',
    'redness_of_eyes': 'Ophthalmologist',
    ' watering_from_eyes': 'Ophthalmologist',
    'watering_from_eyes': 'Ophthalmologist',
    ' loss_of_vision': 'Ophthalmologist',
    'loss_of_vision': 'Ophthalmologist',
    ' pain_behind_the_eyes': 'Ophthalmologist',
    'pain_behind_the_eyes': 'Ophthalmologist',
    ' eye_pain': 'Ophthalmologist',
    'eye_pain': 'Ophthalmologist',
    ' photophobia': 'Ophthalmologist',
    'photophobia': 'Ophthalmologist',
    ' double_vision': 'Ophthalmologist',
    'double_vision': 'Ophthalmologist',
    ' swelling_around_eyes': 'Ophthalmologist',
    'swelling_around_eyes': 'Ophthalmologist',
    ' discharge_from_eyes': 'Ophthalmologist',
    'discharge_from_eyes': 'Ophthalmologist',
    ' itching_eyes': 'Ophthalmologist',
    'itching_eyes': 'Ophthalmologist',
    ' dry_eyes': 'Ophthalmologist',
    'dry_eyes': 'Ophthalmologist',
    ' foreign_body_sensation_in_eyes': 'Ophthalmologist',
    'foreign_body_sensation_in_eyes': 'Ophthalmologist',
    ' eye_redness': 'Ophthalmologist',
    'eye_redness': 'Ophthalmologist',
    ' eye_swelling': 'Ophthalmologist',
    'eye_swelling': 'Ophthalmologist',
    ' eye_discharge': 'Ophthalmologist',
    'eye_discharge': 'Ophthalmologist',
    ' eye_itching': 'Ophthalmologist',
    'eye_itching': 'Ophthalmologist',
}

# Create and save the rule-based model
model = RuleBasedSpecialistPredictor(symptom_specialist_rules)
joblib.dump(model, "rule_based_specialist_model.pkl")

print("✅ Rule-based model saved as rule_based_specialist_model.pkl")

# Test the rule-based model
test_cases = [
    {" nausea": 1},
    {" abdominal_pain": 1},
    {" headache": 1},
    {"itching": 1},
    {" skin_rash": 1},
    {" chest_pain": 1},
    {" joint_pain": 1},
    {"cough": 1},
    {" irregular_sugar_level": 1},
    {" burning_micturition": 1},
]

print("\nTest predictions with rule-based model:")
for i, symptoms in enumerate(test_cases, 1):
    prediction = model.predict(symptoms)
    print(f"Test {i}: {symptoms} → {prediction}") 