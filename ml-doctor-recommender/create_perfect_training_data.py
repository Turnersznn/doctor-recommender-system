import pandas as pd
import numpy as np

# Create a perfect training dataset with explicit mappings
def create_perfect_training_data():
    # Define explicit symptom-specialist mappings
    mappings = {
        'Dermatologist': ['itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic _patches', 'pus_filled_pimples', 'blackheads', 'scurring', 'blister'],
        'Neurologist': ['headache', 'dizziness', 'loss_of_balance', 'lack_of_concentration', 'stiff_neck', 'depression', 'irritability', 'neck_pain', 'anxiety'],
        'Gastroenterologist': ['nausea', 'vomiting', 'abdominal_pain', 'stomach_pain', 'diarrhoea', 'constipation', 'indigestion', 'acidity'],
        'Pulmonologist': ['cough', 'breathlessness', 'phlegm', 'blood_in_sputum', 'rusty_sputum', 'mucoid_sputum'],
        'Cardiologist': ['chest_pain', 'fast_heart_rate', 'palpitations'],
        'Ophthalmologist': ['watering_from_eyes', 'yellowing_of_eyes', 'sunken_eyes', 'pain_behind_the_eyes', 'redness_of_eyes', 'blurred_and_distorted_vision', 'visual_disturbances'],
        'Endocrinologist': ['irregular_sugar_level', 'excessive_hunger', 'weight_loss', 'weight_gain', 'obesity', 'polyuria', 'enlarged_thyroid'],
        'Rheumatologists': ['joint_pain', 'swelling_joints', 'painful_walking', 'movement_stiffness', 'knee_pain', 'hip_joint_pain', 'back_pain'],
        'Allergist': ['continuous_sneezing', 'shivering', 'chills', 'runny_nose', 'congestion', 'throat_irritation'],
        'Gynecologist': ['burning_micturition', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'abnormal_menstruation'],
        'Internal Medcine': ['fatigue', 'mild_fever', 'high_fever', 'sweating', 'loss_of_appetite', 'malaise', 'lethargy']
    }
    
    # Load original data to get all possible symptoms
    df_original = pd.read_excel("Specialist_cleaned.xlsx")
    all_symptoms = [col for col in df_original.columns if col != 'Specialist']
    
    training_rows = []
    
    # Create training data with explicit symptom-specialist pairs
    for specialist, symptoms in mappings.items():
        # Create 200 rows per specialist for better training
        for i in range(200):
            row = {symptom: 0 for symptom in all_symptoms}
            row['Specialist'] = specialist
            
            # Add 1-2 symptoms from this specialist's list
            available_symptoms = [s for s in symptoms if s in all_symptoms]
            
            if available_symptoms:
                # For some rows, add multiple symptoms from the same specialist
                if i < 100:
                    # Single symptom rows
                    selected_symptom = available_symptoms[i % len(available_symptoms)]
                    row[selected_symptom] = 1
                else:
                    # Multiple symptom rows (2 symptoms from same specialist)
                    num_symptoms = min(2, len(available_symptoms))
                    selected_symptoms = np.random.choice(available_symptoms, num_symptoms, replace=False)
                    for symptom in selected_symptoms:
                        row[symptom] = 1
            
            training_rows.append(row)
    
    return pd.DataFrame(training_rows)

# Create perfect training data
print("Creating perfect training data...")
df = create_perfect_training_data()

# Save the training data
df.to_excel("Specialist_perfect.xlsx", index=False)
print(f"✅ Created perfect training data with {len(df)} rows")
print("Specialist distribution:")
print(df['Specialist'].value_counts())

# Test a few rows to make sure they're correct
print("\nSample rows:")
for specialist in ['Dermatologist', 'Neurologist', 'Gastroenterologist']:
    sample = df[df['Specialist'] == specialist].head(3)
    for _, row in sample.iterrows():
        symptoms = [col for col in df.columns if col != 'Specialist' and row[col] == 1]
        print(f"{specialist}: {symptoms}") 