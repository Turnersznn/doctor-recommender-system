import pandas as pd

# Improved mapping for curated symptoms
symptom_specialist_mapping = {
    # General
    "fever": "Family Medicine",
    "fatigue": "Family Medicine",
    "weight_loss": "Family Medicine",
    "weight_gain": "Family Medicine",
    "night_sweats": "Family Medicine",
    "loss_of_appetite": "Family Medicine",

    # Respiratory
    "cough": "Internal Medicine, Pulmonary Disease",
    "shortness_of_breath": "Internal Medicine, Pulmonary Disease",
    "runny_nose": "Internal Medicine, Pulmonary Disease",
    "sore_throat": "Otolaryngology",

    # Cardiac
    "chest_pain": "Internal Medicine, Cardiovascular Disease",
    "palpitations": "Internal Medicine, Cardiovascular Disease",

    # GI
    "abdominal_pain": "Internal Medicine, Gastroenterology",
    "nausea": "Internal Medicine, Gastroenterology",
    "vomiting": "Internal Medicine, Gastroenterology",
    "diarrhoea": "Internal Medicine, Gastroenterology",
    "constipation": "Internal Medicine, Gastroenterology",
    "painful_urination": "Internal Medicine, Gastroenterology",
    "blood_in_urine": "Internal Medicine, Gastroenterology",

    # Neuro
    "headache": "Neurological Surgery",
    "dizziness": "Neurological Surgery",
    "visual_disturbances": "Ophthalmology",
    "blurred_and_distorted_vision": "Ophthalmology",
    "hearing_loss": "Otolaryngology",
    "anxiety": "Psychiatry & Neurology, Psychiatry",
    "depression": "Psychiatry & Neurology, Psychiatry",

    # Musculoskeletal
    "joint_pain": "Internal Medicine, Rheumatology",
    "back_pain": "Internal Medicine, Rheumatology",
    "muscle_weakness": "Internal Medicine, Rheumatology",
    "swelling_joints": "Internal Medicine, Rheumatology",

    # Skin
    "skin_rash": "Dermatology",
    "itching": "Dermatology",
    "red_eyes": "Ophthalmology",

    # Endocrine
    "irregular_sugar_level": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "excessive_hunger": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "abnormal_menstruation": "Obstetrics & Gynecology",
}

# Load the original data
df = pd.read_excel("Specialist.xlsx")

# For each disease, check all symptoms present in the curated mapping and assign the first matching specialist
symptom_cols = [col for col in df.columns if col not in ['Disease', 'Unnamed: 0']]
disease_specialist_mapping = {}

for disease in df['Disease'].unique():
    disease_data = df[df['Disease'] == disease]
    found_specialist = None
    for symptom in symptom_specialist_mapping.keys():
        if symptom in disease_data.columns and disease_data[symptom].sum() > 0:
            found_specialist = symptom_specialist_mapping[symptom]
            break
    if found_specialist:
        disease_specialist_mapping[disease] = found_specialist
    else:
        disease_specialist_mapping[disease] = "Family Medicine"

# Apply the mapping
df['Specialist'] = df['Disease'].map(disease_specialist_mapping)

df.to_excel("Specialist_with_specialist.xlsx", index=False)

print("✅ Created improved mapping for curated symptoms (all symptoms checked)")
print(f"Total rows: {len(df)}")
print(f"Unique specialists: {df['Specialist'].nunique()}")
print("\nSpecialist distribution:")
print(df['Specialist'].value_counts()) 