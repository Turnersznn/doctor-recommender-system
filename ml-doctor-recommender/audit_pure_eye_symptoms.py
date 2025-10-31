import pandas as pd

# Load the fixed data
df = pd.read_excel("Specialist_eye_fixed.xlsx")

# Find all columns related to eyes
eye_symptom_cols = [col for col in df.columns if 'eye' in col.lower()]
non_eye_symptom_cols = [col for col in df.columns if col not in eye_symptom_cols + ['Specialist']]

# Find pure eye symptom rows
mask = (df[eye_symptom_cols].sum(axis=1) > 0) & (df[non_eye_symptom_cols].sum(axis=1) == 0)
pure_eye_df = df[mask]

print(f"Total pure eye symptom rows: {len(pure_eye_df)}")
print("Specialist value counts for pure eye symptom rows:")
print(pure_eye_df['Specialist'].value_counts())
print("\nSample rows:")
print(pure_eye_df.head(10)) 