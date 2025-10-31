import pandas as pd

# Create a more intelligent symptom-to-specialist mapping
symptom_specialist_mapping = {
    # Skin symptoms → Dermatology
    "itching": "Dermatology",
    "skin_rash": "Dermatology", 
    "nodal_skin_eruptions": "Dermatology",
    "dischromic _patches": "Dermatology",
    "red_spots_over_body": "Dermatology",
    "skin_peeling": "Dermatology",
    "silver_like_dusting": "Dermatology",
    "pus_filled_pimples": "Dermatology",
    "blackheads": "Dermatology",
    "scurring": "Dermatology",
    "blister": "Dermatology",
    "red_sore_around_nose": "Dermatology",
    "yellow_crust_ooze": "Dermatology",
    
    # Respiratory symptoms → Internal Medicine, Pulmonary Disease
    "cough": "Internal Medicine, Pulmonary Disease",
    "breathlessness": "Internal Medicine, Pulmonary Disease",
    "mucoid_sputum": "Internal Medicine, Pulmonary Disease",
    "blood_in_sputum": "Internal Medicine, Pulmonary Disease",
    "rusty_sputum": "Internal Medicine, Pulmonary Disease",
    "phlegm": "Internal Medicine, Pulmonary Disease",
    "fast_heart_rate": "Internal Medicine, Pulmonary Disease",
    
    # Heart/Chest symptoms → Internal Medicine, Cardiovascular Disease
    "chest_pain": "Internal Medicine, Cardiovascular Disease",
    "palpitations": "Internal Medicine, Cardiovascular Disease",
    "swollen_legs": "Internal Medicine, Cardiovascular Disease",
    "swollen_blood_vessels": "Internal Medicine, Cardiovascular Disease",
    "prominent_veins_on_calf": "Internal Medicine, Cardiovascular Disease",
    "cold_hands_and_feets": "Internal Medicine, Cardiovascular Disease",
    
    # Digestive symptoms → Internal Medicine, Gastroenterology
    "stomach_pain": "Internal Medicine, Gastroenterology",
    "abdominal_pain": "Internal Medicine, Gastroenterology",
    "belly_pain": "Internal Medicine, Gastroenterology",
    "nausea": "Internal Medicine, Gastroenterology",
    "vomiting": "Internal Medicine, Gastroenterology",
    "diarrhoea": "Internal Medicine, Gastroenterology",
    "constipation": "Internal Medicine, Gastroenterology",
    "acidity": "Internal Medicine, Gastroenterology",
    "ulcers_on_tongue": "Internal Medicine, Gastroenterology",
    "loss_of_appetite": "Internal Medicine, Gastroenterology",
    "indigestion": "Internal Medicine, Gastroenterology",
    "passage_of_gases": "Internal Medicine, Gastroenterology",
    "burning_micturition": "Internal Medicine, Gastroenterology",
    "spotting_ urination": "Internal Medicine, Gastroenterology",
    "internal_itching": "Internal Medicine, Gastroenterology",
    "dark_urine": "Internal Medicine, Gastroenterology",
    "yellow_urine": "Internal Medicine, Gastroenterology",
    "bladder_discomfort": "Internal Medicine, Gastroenterology",
    "foul_smell_of urine": "Internal Medicine, Gastroenterology",
    "continuous_feel_of_urine": "Internal Medicine, Gastroenterology",
    "pain_during_bowel_movements": "Internal Medicine, Gastroenterology",
    "pain_in_anal_region": "Internal Medicine, Gastroenterology",
    "bloody_stool": "Internal Medicine, Gastroenterology",
    "irritation_in_anus": "Internal Medicine, Gastroenterology",
    "swelling_of_stomach": "Internal Medicine, Gastroenterology",
    "distention_of_abdomen": "Internal Medicine, Gastroenterology",
    "acute_liver_failure": "Internal Medicine, Gastroenterology",
    "stomach_bleeding": "Internal Medicine, Gastroenterology",
    "yellowish_skin": "Internal Medicine, Gastroenterology",
    "yellowing_of_eyes": "Internal Medicine, Gastroenterology",
    
    # Brain/Nervous system → Neurological Surgery
    "headache": "Neurological Surgery",
    "dizziness": "Neurological Surgery",
    "loss_of_balance": "Neurological Surgery",
    "lack_of_concentration": "Neurological Surgery",
    "stiff_neck": "Neurological Surgery",
    "visual_disturbances": "Neurological Surgery",
    "weakness_in_limbs": "Neurological Surgery",
    "neck_pain": "Neurological Surgery",
    "weakness_of_one_body_side": "Neurological Surgery",
    "altered_sensorium": "Neurological Surgery",
    "slurred_speech": "Neurological Surgery",
    "spinning_movements": "Neurological Surgery",
    "unsteadiness": "Neurological Surgery",
    "pain_behind_the_eyes": "Neurological Surgery",
    
    # Mental Health → Psychiatry & Neurology, Psychiatry
    "depression": "Psychiatry & Neurology, Psychiatry",
    "irritability": "Psychiatry & Neurology, Psychiatry",
    "anxiety": "Psychiatry & Neurology, Psychiatry",
    "mood_swings": "Psychiatry & Neurology, Psychiatry",
    "restlessness": "Psychiatry & Neurology, Psychiatry",
    
    # Eye symptoms → Ophthalmology
    "watering_from_eyes": "Ophthalmology",
    "redness_of_eyes": "Ophthalmology",
    "blurred_and_distorted_vision": "Ophthalmology",
    
    # Ear/Nose/Throat → Otolaryngology
    "patches_in_throat": "Otolaryngology",
    "throat_irritation": "Otolaryngology",
    "sinus_pressure": "Otolaryngology",
    "runny_nose": "Otolaryngology",
    "congestion": "Otolaryngology",
    "loss_of_smell": "Otolaryngology",
    
    # Joint/Muscle → Internal Medicine, Rheumatology
    "joint_pain": "Internal Medicine, Rheumatology",
    "swelling_joints": "Internal Medicine, Rheumatology",
    "painful_walking": "Internal Medicine, Rheumatology",
    "movement_stiffness": "Internal Medicine, Rheumatology",
    "knee_pain": "Internal Medicine, Rheumatology",
    "hip_joint_pain": "Internal Medicine, Rheumatology",
    "back_pain": "Internal Medicine, Rheumatology",
    "muscle_pain": "Internal Medicine, Rheumatology",
    "muscle_wasting": "Internal Medicine, Rheumatology",
    "muscle_weakness": "Internal Medicine, Rheumatology",
    "bruising": "Internal Medicine, Rheumatology",
    "cramps": "Internal Medicine, Rheumatology",
    
    # Diabetes/Endocrine → Internal Medicine, Endocrinology, Diabetes & Metabolism
    "irregular_sugar_level": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "polyuria": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "excessive_hunger": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "increased_appetite": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "weight_gain": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "weight_loss": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "obesity": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "enlarged_thyroid": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    "puffy_face_and_eyes": "Internal Medicine, Endocrinology, Diabetes & Metabolism",
    
    # Allergies → Allergy & Immunology
    "continuous_sneezing": "Allergy & Immunology",
    "shivering": "Allergy & Immunology",
    "chills": "Allergy & Immunology",
    
    # Women's Health → Obstetrics & Gynecology
    "abnormal_menstruation": "Obstetrics & Gynecology",
    
    # Children → Pediatrics
    "extra_marital_contacts": "Pediatrics",  # This seems like a data quality issue
    
    # General symptoms → Family Medicine
    "fever": "Family Medicine",
    "high_fever": "Family Medicine",
    "mild_fever": "Family Medicine",
    "fatigue": "Family Medicine",
    "lethargy": "Family Medicine",
    "malaise": "Family Medicine",
    "sweating": "Family Medicine",
    "dehydration": "Family Medicine",
    "sunken_eyes": "Family Medicine",
    "swelled_lymph_nodes": "Family Medicine",
    "toxic_look_(typhos)": "Family Medicine",
    "coma": "Family Medicine",
    "fluid_overload": "Family Medicine",
    "history_of_alcohol_consumption": "Family Medicine",
    "receiving_blood_transfusion": "Family Medicine",
    "receiving_unsterile_injections": "Family Medicine",
    "family_history": "Family Medicine",
    "swollen_extremeties": "Family Medicine",
    "brittle_nails": "Family Medicine",
    "small_dents_in_nails": "Family Medicine",
    "inflammatory_nails": "Family Medicine",
}

# Load the original data
df = pd.read_excel("Specialist.xlsx")

# Create a new column based on the most common symptom for each disease
# For each disease, find the most common symptom and map it to specialist
disease_specialist_mapping = {}

for disease in df['Disease'].unique():
    disease_data = df[df['Disease'] == disease]
    # Get the symptom columns (all except Disease and any other non-symptom columns)
    symptom_cols = [col for col in disease_data.columns if col not in ['Disease', 'Unnamed: 0']]
    
    # Find the most common symptom for this disease
    most_common_symptom = None
    max_count = 0
    
    for symptom in symptom_cols:
        count = disease_data[symptom].sum()
        if count > max_count:
            max_count = count
            most_common_symptom = symptom
    
    # Map the most common symptom to specialist
    if most_common_symptom and most_common_symptom in symptom_specialist_mapping:
        disease_specialist_mapping[disease] = symptom_specialist_mapping[most_common_symptom]
    else:
        disease_specialist_mapping[disease] = "Family Medicine"

# Apply the mapping
df['Specialist'] = df['Disease'].map(disease_specialist_mapping)

# Save the updated data
df.to_excel("Specialist_with_specialist.xlsx", index=False)

print("✅ Created symptom-based specialist mapping")
print(f"Total rows: {len(df)}")
print(f"Unique specialists: {df['Specialist'].nunique()}")
print("\nSpecialist distribution:")
print(df['Specialist'].value_counts()) 