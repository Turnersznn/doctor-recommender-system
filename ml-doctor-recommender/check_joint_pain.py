#!/usr/bin/env python3
import pandas as pd

# Load datasets
original_df = pd.read_csv('Original_Dataset.csv', encoding='latin-1')
doctor_disease_df = pd.read_csv('Doctor_Versus_Disease.csv', names=['Disease', 'Specialist'], encoding='latin-1')

print("🔍 Checking joint pain in datasets...")

# Find joint pain rows
joint_rows = original_df[original_df.apply(lambda row: 'joint' in str(row).lower(), axis=1)]
print(f"\nFound {len(joint_rows)} rows with joint symptoms")
print("Diseases with joint symptoms:")
print(joint_rows['Disease'].unique())

# Check what specialists these diseases map to
for disease in joint_rows['Disease'].unique():
    specialist_row = doctor_disease_df[doctor_disease_df['Disease'] == disease]
    if not specialist_row.empty:
        specialist = specialist_row.iloc[0]['Specialist']
        print(f"  {disease} -> {specialist}")

print("\n🔍 Checking arthritis specifically...")
arthritis_rows = original_df[original_df['Disease'].str.contains('arthritis', case=False, na=False)]
print(f"Found {len(arthritis_rows)} arthritis rows")
for disease in arthritis_rows['Disease'].unique():
    specialist_row = doctor_disease_df[doctor_disease_df['Disease'] == disease]
    if not specialist_row.empty:
        specialist = specialist_row.iloc[0]['Specialist']
        print(f"  {disease} -> {specialist}")

print("\n🔍 All rheumatology diseases:")
rheum_diseases = doctor_disease_df[doctor_disease_df['Specialist'].str.contains('Rheumat', case=False, na=False)]
print(rheum_diseases)
