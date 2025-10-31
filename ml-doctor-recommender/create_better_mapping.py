import pandas as pd

# Create a better mapping using actual specialist names from the data
disease_to_specialist_mapping = {
    # Skin related
    "Acne": "Dermatology",
    "Eczema": "Dermatology", 
    "Psoriasis": "Dermatology",
    "Skin Rash": "Dermatology",
    "Itching": "Dermatology",
    
    # Heart related
    "Hypertension": "Internal Medicine, Cardiovascular Disease",
    "Chest Pain": "Internal Medicine, Cardiovascular Disease",
    "Heart Disease": "Internal Medicine, Cardiovascular Disease",
    "High Blood Pressure": "Internal Medicine, Cardiovascular Disease",
    
    # Respiratory
    "Cough": "Internal Medicine, Pulmonary Disease",
    "Shortness of Breath": "Internal Medicine, Pulmonary Disease",
    "Asthma": "Internal Medicine, Pulmonary Disease",
    "Bronchitis": "Internal Medicine, Pulmonary Disease",
    
    # Digestive
    "Stomach Pain": "Internal Medicine, Gastroenterology",
    "Nausea": "Internal Medicine, Gastroenterology",
    "Vomiting": "Internal Medicine, Gastroenterology",
    "Diarrhea": "Internal Medicine, Gastroenterology",
    "Constipation": "Internal Medicine, Gastroenterology",
    "Acid Reflux": "Internal Medicine, Gastroenterology",
    
    # Diabetes
    "Diabetes": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "High Blood Sugar": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    
    # Joint/Muscle
    "Joint Pain": "Internal Medicine, Rheumatology",
    "Arthritis": "Internal Medicine, Rheumatology",
    "Back Pain": "Internal Medicine, Rheumatology",
    
    # Brain/Nervous System
    "Headache": "Neurological Surgery",
    "Migraine": "Neurological Surgery",
    "Seizures": "Neurological Surgery",
    "Dizziness": "Neurological Surgery",
    
    # Mental Health
    "Depression": "Psychiatry & Neurology, Psychiatry",
    "Anxiety": "Psychiatry & Neurology, Psychiatry",
    "Insomnia": "Psychiatry & Neurology, Sleep Medicine",
    
    # Eye related
    "Vision Problems": "Ophthalmology",
    "Eye Pain": "Ophthalmology",
    "Blurred Vision": "Ophthalmology",
    
    # Ear/Nose/Throat
    "Ear Pain": "Otolaryngology",
    "Sore Throat": "Otolaryngology",
    "Hearing Loss": "Otolaryngology",
    "Sinus Problems": "Otolaryngology",
    
    # Women's Health
    "Pregnancy": "Obstetrics & Gynecology",
    "Menstrual Problems": "Obstetrics & Gynecology",
    "Pelvic Pain": "Obstetrics & Gynecology",
    
    # Children
    "Child Fever": "Pediatrics",
    "Child Cough": "Pediatrics",
    "Child Development": "Pediatrics, Developmental - Behavioral Pediatrics",
    
    # General/Default
    "Fever": "Family Medicine",
    "Fatigue": "Family Medicine",
    "Weight Loss": "Family Medicine",
    "Weight Gain": "Family Medicine",
    "General Pain": "Family Medicine",
    "General Weakness": "Family Medicine"
}

# Load the original data
df = pd.read_excel("Specialist.xlsx")

# Create the new specialist column using our better mapping
df['Specialist'] = df['Disease'].map(disease_to_specialist_mapping)

# Fill any missing values with Family Medicine (general practitioner)
df['Specialist'] = df['Specialist'].fillna('Family Medicine')

# Save the updated data
df.to_excel("Specialist_with_specialist.xlsx", index=False)

print("✅ Created better mapping and saved as Specialist_with_specialist.xlsx")
print(f"Total rows: {len(df)}")
print(f"Unique specialists: {df['Specialist'].nunique()}")
print("\nSpecialist distribution:")
print(df['Specialist'].value_counts()) 