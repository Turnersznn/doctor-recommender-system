import pandas as pd
import numpy as np

# Define clinical symptom-specialist mappings
clinical_mappings = {
    'Gastroenterologist': [
        'nausea', 'vomiting', 'abdominal_pain', 'stomach_pain', 'diarrhoea', 
        'constipation', 'indigestion', 'acidity', 'passage_of_gases', 'belly_pain',
        'yellowish_skin', 'yellowing_of_eyes', 'burning_micturition', 'dark_urine',
        'yellow_urine', 'bloody_stool', 'pain_during_bowel_movements'
    ],
    'Neurologist': [
        'headache', 'dizziness', 'loss_of_balance', 'lack_of_concentration', 
        'stiff_neck', 'depression', 'irritability', 'back_pain', 'neck_pain',
        'altered_sensorium', 'slurred_speech', 'muscle_weakness', 'weakness_in_limbs',
        'weakness_of_one_body_side', 'spinning_movements', 'unsteadiness'
    ],
    'Dermatologist': [
        'itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic _patches',
        'pus_filled_pimples', 'blackheads', 'scurring', 'blister', 'red_sore_around_nose',
        'yellow_crust_ooze', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails',
        'inflammatory_nails', 'red_spots_over_body'
    ],
    'Cardiologist': [
        'chest_pain', 'fast_heart_rate', 'palpitations', 'breathlessness'
    ],
    'Pulmonologist': [
        'cough', 'breathlessness', 'phlegm', 'blood_in_sputum', 'rusty_sputum',
        'mucoid_sputum', 'throat_irritation', 'runny_nose', 'continuous_sneezing',
        'congestion', 'loss_of_smell', 'sinus_pressure'
    ],
    'Endocrinologist': [
        'irregular_sugar_level', 'excessive_hunger', 'weight_loss', 'weight_gain',
        'obesity', 'polyuria', 'enlarged_thyroid', 'excessive_hunger', 'increased_appetite',
        'mood_swings', 'puffy_face_and_eyes', 'brittle_nails', 'swollen_extremeties'
    ],
    'Rheumatologists': [
        'joint_pain', 'swelling_joints', 'painful_walking', 'movement_stiffness',
        'knee_pain', 'hip_joint_pain', 'neck_pain', 'back_pain'
    ],
    'Ophthalmologist': [
        'watering_from_eyes', 'yellowing_of_eyes', 'sunken_eyes', 'pain_behind_the_eyes',
        'redness_of_eyes', 'puffy_face_and_eyes', 'blurred_and_distorted_vision',
        'visual_disturbances', 'loss_of_vision', 'eye_pain', 'photophobia',
        'double_vision', 'swelling_around_eyes', 'discharge_from_eyes', 'itching_eyes',
        'dry_eyes', 'foreign_body_sensation_in_eyes'
    ],
    'Allergist': [
        'continuous_sneezing', 'shivering', 'chills', 'watering_from_eyes',
        'runny_nose', 'congestion', 'throat_irritation'
    ],
    'Gynecologist': [
        'burning_micturition', 'bladder_discomfort', 'foul_smell_of urine',
        'continuous_feel_of_urine', 'abnormal_menstruation'
    ],
    'Internal Medcine': [
        'fatigue', 'mild_fever', 'high_fever', 'chills', 'sweating',
        'loss_of_appetite', 'malaise', 'lethargy', 'restlessness', 'anxiety',
        'dehydration', 'sunken_eyes', 'family_history', 'extra_marital_contacts',
        'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma',
        'stomach_bleeding', 'acute_liver_failure', 'swelling_of_stomach',
        'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload'
    ]
}

# Load original data to get all possible symptoms
df_original = pd.read_excel("Specialist_cleaned.xlsx")
all_symptoms = [col for col in df_original.columns if col != 'Specialist']

# Create clean training data
clean_rows = []

# For each specialist, create multiple rows with their symptoms
for specialist, symptoms in clinical_mappings.items():
    # Create 50-100 rows per specialist
    num_rows = min(100, max(50, len(symptoms) * 10))
    
    for _ in range(num_rows):
        row = {symptom: 0 for symptom in all_symptoms}
        row['Specialist'] = specialist
        
        # Add 1-3 symptoms from this specialist's list
        num_symptoms = np.random.randint(1, min(4, len(symptoms) + 1))
        selected_symptoms = np.random.choice(symptoms, num_symptoms, replace=False)
        
        for symptom in selected_symptoms:
            if symptom in all_symptoms:  # Make sure symptom exists in original data
                row[symptom] = 1
        
        clean_rows.append(row)

# Convert to DataFrame
clean_df = pd.DataFrame(clean_rows)

# Save clean training data
clean_df.to_excel("Specialist_clean_clinical.xlsx", index=False)
print(f"✅ Created clean clinical training data with {len(clean_df)} rows")
print("Specialist distribution:")
print(clean_df['Specialist'].value_counts()) 