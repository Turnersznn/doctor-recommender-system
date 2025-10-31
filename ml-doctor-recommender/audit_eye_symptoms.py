import pandas as pd

# Load cleaned data
df = pd.read_excel("Specialist_cleaned.xlsx")

# Find all columns related to eyes
eye_symptom_cols = [col for col in df.columns if 'eye' in col.lower()]

print("Eye-related symptom columns:")
for col in eye_symptom_cols:
    print(f"- {col}")

# For each eye symptom, print the value counts of the Specialist label where the symptom is present
for col in eye_symptom_cols:
    print(f"\n=== {col} ===")
    subset = df[df[col] == 1]
    print(subset['Specialist'].value_counts())
    print(f"Total cases: {len(subset)}") 