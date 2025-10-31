import pandas as pd

# Load cleaned data
df = pd.read_excel("Specialist_cleaned.xlsx")

# Find all columns related to eyes
eye_symptom_cols = [col for col in df.columns if 'eye' in col.lower()]
non_eye_symptom_cols = [col for col in df.columns if col not in eye_symptom_cols + ['Specialist']]

# Set Specialist to 'Ophthalmologist' if at least one eye symptom is 1 and all non-eye symptoms are 0
mask = (df[eye_symptom_cols].sum(axis=1) > 0) & (df[non_eye_symptom_cols].sum(axis=1) == 0)
df.loc[mask, 'Specialist'] = 'Ophthalmologist'

# Save the fixed data
df.to_excel("Specialist_eye_fixed.xlsx", index=False)
print("✅ Eye specialist labels fixed (only for pure eye symptoms) and saved to Specialist_eye_fixed.xlsx") 