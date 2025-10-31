import pandas as pd
import numpy as np

# Define clear symptom-specialist mappings (only core symptoms)
simple_mappings = {
    'Dermatologist': ['itching', 'skin_rash'],
    'Neurologist': ['headache', 'dizziness'],
    'Gastroenterologist': ['nausea', 'vomiting', 'abdominal_pain'],
    'Pulmonologist': ['cough', 'breathlessness'],
    'Cardiologist': ['chest_pain', 'palpitations'],
    'Ophthalmologist': ['watering_from_eyes', 'pain_behind_the_eyes', 'redness_of_eyes'],
    'Endocrinologist': ['irregular_sugar_level', 'excessive_hunger'],
    'Rheumatologists': ['joint_pain', 'swelling_joints'],
    'Allergist': ['continuous_sneezing', 'runny_nose'],
    'Gynecologist': ['burning_micturition', 'abnormal_menstruation'],
    'Internal Medcine': ['fatigue', 'mild_fever']
}

# Load original data to get all possible symptoms
df_original = pd.read_excel("Specialist_cleaned.xlsx")
all_symptoms = [col for col in df_original.columns if col != 'Specialist']

print("Available symptoms in original data:")
print(all_symptoms[:10])  # Show first 10

# Check which symptoms from our mappings exist
print("\nChecking symptom mappings:")
for specialist, symptoms in simple_mappings.items():
    missing = [s for s in symptoms if s not in all_symptoms]
    if missing:
        print(f"{specialist}: Missing symptoms - {missing}")
    else:
        print(f"{specialist}: All symptoms found ✓")

# Create simple training data
simple_rows = []

# For each specialist, create multiple rows with ONLY their symptoms
for specialist, symptoms in simple_mappings.items():
    # Create 50 rows per specialist
    for i in range(50):
        row = {symptom: 0 for symptom in all_symptoms}
        row['Specialist'] = specialist
        
        # Add exactly one symptom from this specialist's list
        available_symptoms = [s for s in symptoms if s in all_symptoms]
        if available_symptoms:
            selected_symptom = np.random.choice(available_symptoms)
            row[selected_symptom] = 1
        
        simple_rows.append(row)

# Convert to DataFrame
simple_df = pd.DataFrame(simple_rows)

# Save simple training data
simple_df.to_excel("Specialist_simple.xlsx", index=False)
print(f"✅ Created simple training data with {len(simple_df)} rows")
print("Specialist distribution:")
print(simple_df['Specialist'].value_counts())

# Test a few rows
print("\nSample rows:")
for specialist in ['Dermatologist', 'Neurologist', 'Gastroenterologist']:
    sample = simple_df[simple_df['Specialist'] == specialist].head(1)
    symptoms = [col for col in all_symptoms if sample[col].iloc[0] == 1]
    print(f"{specialist}: {symptoms}") 