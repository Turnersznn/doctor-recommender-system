import pandas as pd

# Create mapping that uses actual specialist names from the doctor database
specialist_mapping = {
    # Direct matches
    "Dermatologist": "Dermatology",
    "Dermatologists": "Dermatology",
    "Cardiologist": "Internal Medicine, Cardiovascular Disease",
    "Gastroenterologist": "Internal Medicine, Gastroenterology",
    "Endocrinologist": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "Pulmonologist": "Internal Medicine, Pulmonary Disease",
    "Neurologist": "Neurological Surgery",
    "Allergist": "Allergy & Immunology",
    "Otolaryngologist": "Otolaryngology",
    "Gynecologist": "Obstetrics & Gynecology",
    "Pediatrician": "Pediatrics",
    "Rheumatologists": "Internal Medicine, Rheumatology",
    
    # Close matches
    "Internal Medcine": "Internal Medicine",  # Typo in original data
    "Hepatologist": "Internal Medicine, Gastroenterology",  # Liver specialist
    "Phlebologist": "Internal Medicine, Cardiovascular Disease",  # Vein specialist
    "Osteopathic": "Family Medicine",  # General practice
    "Osteoarthristis": "Internal Medicine, Rheumatology",  # Joint specialist
    "Common Cold": "Family Medicine",  # General practice
}

# Load the original data
df = pd.read_excel("Specialist.xlsx")

# Create the new specialist column using our mapping
df['Specialist'] = df['Disease'].map(specialist_mapping)

# Fill any missing values with Family Medicine (which exists in doctor data)
df['Specialist'] = df['Specialist'].fillna('Family Medicine')

# Save the updated data
df.to_excel("Specialist_with_specialist.xlsx", index=False)

print("✅ Created correct mapping and saved as Specialist_with_specialist.xlsx")
print(f"Total rows: {len(df)}")
print(f"Unique specialists: {df['Specialist'].nunique()}")
print("\nSpecialist distribution:")
print(df['Specialist'].value_counts())

print("\nAvailable specialists in training data:")
print(df['Specialist'].unique()) 