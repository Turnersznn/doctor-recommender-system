import pandas as pd
import numpy as np

# Load the data
df = pd.read_excel("Specialist.xlsx")
cols = [col for col in df.columns if not col.lower().startswith('unnamed')]
df = df[cols]

# Get symptom columns (all except Disease)
symptom_cols = [col for col in df.columns if col != 'Disease']

print("=== SYMPTOM DISTRIBUTION BY SPECIALIST ===\n")

# For each specialist, show the most common symptoms
for specialist in df['Disease'].unique():
    specialist_data = df[df['Disease'] == specialist]
    print(f"\n{specialist} ({len(specialist_data)} rows):")
    
    # Get symptom counts for this specialist
    symptom_counts = {}
    for symptom in symptom_cols:
        count = specialist_data[symptom].sum()
        if count > 0:
            symptom_counts[symptom] = count
    
    # Sort by count and show top 10
    sorted_symptoms = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)
    for symptom, count in sorted_symptoms[:10]:
        percentage = (count / len(specialist_data)) * 100
        print(f"  {symptom}: {count} ({percentage:.1f}%)")

print("\n=== SPECIALIST BALANCE ===\n")
print("Current distribution:")
print(df['Disease'].value_counts())

print("\n=== MOST INFORMATIVE SYMPTOMS ===\n")
# Find symptoms that are most useful for distinguishing between specialists
symptom_info = {}
for symptom in symptom_cols:
    # Calculate how many specialists have this symptom
    specialists_with_symptom = 0
    total_specialists = len(df['Disease'].unique())
    
    for specialist in df['Disease'].unique():
        specialist_data = df[df['Disease'] == specialist]
        if specialist_data[symptom].sum() > 0:
            specialists_with_symptom += 1
    
    # Symptoms that appear in 2-5 specialists are most informative
    if 2 <= specialists_with_symptom <= 5:
        symptom_info[symptom] = specialists_with_symptom

print("Symptoms that appear in 2-5 specialists (most informative):")
for symptom, count in sorted(symptom_info.items(), key=lambda x: x[1]):
    print(f"  {symptom}: appears in {count} specialists") 