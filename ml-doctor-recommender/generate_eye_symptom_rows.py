import pandas as pd
import itertools

# Load the fixed data
df = pd.read_excel("Specialist_eye_fixed.xlsx")

# Find all columns related to eyes
eye_symptom_cols = [col for col in df.columns if 'eye' in col.lower()]
non_eye_symptom_cols = [col for col in df.columns if col not in eye_symptom_cols + ['Specialist']]

# Generate synthetic rows for each single eye symptom
synthetic_rows = []
for col in eye_symptom_cols:
    row = {c: 0 for c in df.columns if c != 'Specialist'}
    row[col] = 1
    row['Specialist'] = 'Ophthalmologist'
    synthetic_rows.append(row)

# Optionally, generate combinations of two eye symptoms
for combo in itertools.combinations(eye_symptom_cols, 2):
    row = {c: 0 for c in df.columns if c != 'Specialist'}
    for c in combo:
        row[c] = 1
    row['Specialist'] = 'Ophthalmologist'
    synthetic_rows.append(row)

# Convert to DataFrame and append
synthetic_df = pd.DataFrame(synthetic_rows)
augmented_df = pd.concat([df, synthetic_df], ignore_index=True)

# Save the augmented data
augmented_df.to_excel("Specialist_eye_augmented.xlsx", index=False)
print(f"✅ Added {len(synthetic_df)} synthetic eye symptom rows. Saved to Specialist_eye_augmented.xlsx")
print("Sample synthetic rows:")
print(synthetic_df.head(10)) 