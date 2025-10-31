import pickle

# Define direct symptom-to-specialist mappings
symptom_to_specialist = {
    # Dermatologist
    'itching': 'Dermatologist',
    'skin_rash': 'Dermatologist',
    'nodal_skin_eruptions': 'Dermatologist',
    'dischromic _patches': 'Dermatologist',
    'pus_filled_pimples': 'Dermatologist',
    'blackheads': 'Dermatologist',
    'scurring': 'Dermatologist',
    'blister': 'Dermatologist',
    
    # Neurologist
    'headache': 'Neurologist',
    'dizziness': 'Neurologist',
    'loss_of_balance': 'Neurologist',
    'lack_of_concentration': 'Neurologist',
    'stiff_neck': 'Neurologist',
    'depression': 'Neurologist',
    'irritability': 'Neurologist',
    'back_pain': 'Neurologist',
    'neck_pain': 'Neurologist',
    
    # Gastroenterologist
    'nausea': 'Gastroenterologist',
    'vomiting': 'Gastroenterologist',
    'abdominal_pain': 'Gastroenterologist',
    'stomach_pain': 'Gastroenterologist',
    'diarrhoea': 'Gastroenterologist',
    'constipation': 'Gastroenterologist',
    'indigestion': 'Gastroenterologist',
    'acidity': 'Gastroenterologist',
    
    # Pulmonologist
    'cough': 'Pulmonologist',
    'breathlessness': 'Pulmonologist',
    'phlegm': 'Pulmonologist',
    'blood_in_sputum': 'Pulmonologist',
    'rusty_sputum': 'Pulmonologist',
    'mucoid_sputum': 'Pulmonologist',
    
    # Cardiologist
    'chest_pain': 'Cardiologist',
    'fast_heart_rate': 'Cardiologist',
    'palpitations': 'Cardiologist',
    
    # Ophthalmologist
    'watering_from_eyes': 'Ophthalmologist',
    'yellowing_of_eyes': 'Ophthalmologist',
    'sunken_eyes': 'Ophthalmologist',
    'pain_behind_the_eyes': 'Ophthalmologist',
    'redness_of_eyes': 'Ophthalmologist',
    'blurred_and_distorted_vision': 'Ophthalmologist',
    'visual_disturbances': 'Ophthalmologist',
    
    # Endocrinologist
    'irregular_sugar_level': 'Endocrinologist',
    'excessive_hunger': 'Endocrinologist',
    'weight_loss': 'Endocrinologist',
    'weight_gain': 'Endocrinologist',
    'obesity': 'Endocrinologist',
    'polyuria': 'Endocrinologist',
    'enlarged_thyroid': 'Endocrinologist',
    
    # Rheumatologists
    'joint_pain': 'Rheumatologists',
    'swelling_joints': 'Rheumatologists',
    'painful_walking': 'Rheumatologists',
    'movement_stiffness': 'Rheumatologists',
    'knee_pain': 'Rheumatologists',
    'hip_joint_pain': 'Rheumatologists',
    
    # Allergist
    'continuous_sneezing': 'Allergist',
    'shivering': 'Allergist',
    'chills': 'Allergist',
    'runny_nose': 'Allergist',
    'congestion': 'Allergist',
    'throat_irritation': 'Allergist',
    
    # Gynecologist
    'burning_micturition': 'Gynecologist',
    'bladder_discomfort': 'Gynecologist',
    'foul_smell_of urine': 'Gynecologist',
    'continuous_feel_of_urine': 'Gynecologist',
    'abnormal_menstruation': 'Gynecologist',
    
    # Internal Medicine
    'fatigue': 'Internal Medcine',
    'mild_fever': 'Internal Medcine',
    'high_fever': 'Internal Medcine',
    'sweating': 'Internal Medcine',
    'loss_of_appetite': 'Internal Medcine',
    'malaise': 'Internal Medcine',
    'lethargy': 'Internal Medcine'
}

class RuleBasedSpecialistPredictor:
    def __init__(self, mappings):
        self.mappings = mappings
    
    def predict(self, symptoms):
        """
        Predict specialist based on symptoms.
        symptoms: dict with symptom names as keys and 1/0 as values
        """
        # Find all active symptoms (value = 1)
        active_symptoms = [symptom for symptom, value in symptoms.items() if value == 1]
        
        if not active_symptoms:
            return 'Internal Medcine'  # Default for no symptoms
        
        # Check each active symptom for a specialist mapping
        for symptom in active_symptoms:
            if symptom in self.mappings:
                return self.mappings[symptom]
        
        # If no specific mapping found, return Internal Medicine
        return 'Internal Medcine'

# Create and save the rule-based model
model = RuleBasedSpecialistPredictor(symptom_to_specialist)

with open('rule_based_specialist_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Rule-based model created and saved")

# Test the model
test_cases = [
    {'itching': 1},
    {'headache': 1},
    {'nausea': 1},
    {'cough': 1},
    {'watering_from_eyes': 1},
    {'chest_pain': 1}
]

print("\nTesting rule-based model:")
for test_case in test_cases:
    prediction = model.predict(test_case)
    symptom = list(test_case.keys())[0]
    print(f"{symptom}: {prediction}") 