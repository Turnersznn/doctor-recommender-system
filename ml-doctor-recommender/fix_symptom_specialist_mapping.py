import pandas as pd

# Load the data
df = pd.read_excel("Specialist.xlsx")
cols = [col for col in df.columns if not col.lower().startswith('unnamed')]
df = df[cols]

# Define symptom-specialist fixes
# Format: {'symptom_column': 'correct_specialist'}
symptom_fixes = {
    ' nausea': 'Gastroenterologist',
    ' vomiting': 'Gastroenterologist', 
    ' abdominal_pain': 'Gastroenterologist',
    ' diarrhoea': 'Gastroenterologist',
    ' constipation': 'Gastroenterologist',
    ' stomach_pain': 'Gastroenterologist',
    ' indigestion': 'Gastroenterologist',
    ' acidity': 'Gastroenterologist',
    ' headache': 'Neurologist',
    ' dizziness': 'Neurologist',
    ' chest_pain': 'Cardiologist',
    ' breathlessness': 'Pulmonologist',
    ' cough': 'Pulmonologist',
    ' skin_rash': 'Dermatologist',
    'itching': 'Dermatologist',
    ' joint_pain': 'Rheumatologists',
    ' back_pain': 'Neurologist',
    ' muscle_weakness': 'Neurologist',
    ' fatigue': 'Internal Medcine',
    ' mild_fever': 'Internal Medcine',
    ' fast_heart_rate': 'Cardiologist',
    ' loss_of_appetite': 'Gastroenterologist',
    ' weight_loss': 'Endocrinologist'
}

print("Fixing symptom-specialist mappings...")
print("Before fixes:")
for symptom, correct_specialist in symptom_fixes.items():
    if symptom in df.columns:
        current_distribution = df[df[symptom] == 1]['Disease'].value_counts()
        print(f"{symptom}: {current_distribution.index[0]} ({current_distribution.iloc[0]} cases)")

# Apply fixes
for symptom, correct_specialist in symptom_fixes.items():
    if symptom in df.columns:
        # Change all rows where this symptom is present to the correct specialist
        mask = df[symptom] == 1
        df.loc[mask, 'Disease'] = correct_specialist
        print(f"Fixed {symptom} → {correct_specialist}")

print("\nAfter fixes:")
for symptom, correct_specialist in symptom_fixes.items():
    if symptom in df.columns:
        new_distribution = df[df[symptom] == 1]['Disease'].value_counts()
        print(f"{symptom}: {new_distribution.index[0]} ({new_distribution.iloc[0]} cases)")

# Save the corrected data
df.to_excel("Specialist_fixed.xlsx", index=False)
print("\n✅ Fixed data saved as 'Specialist_fixed.xlsx'")

# Show some examples of the fixes
print("\nExample fixes:")
for symptom in [' nausea', ' vomiting', ' abdominal_pain', ' headache', ' chest_pain']:
    if symptom in df.columns:
        distribution = df[df[symptom] == 1]['Disease'].value_counts()
        print(f"{symptom}: {distribution.to_dict()}") 