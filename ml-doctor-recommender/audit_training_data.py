import pandas as pd

# Load the current training data
df = pd.read_excel("Specialist_eye_augmented.xlsx")

print("Current training data specialist distribution:")
print(df['Specialist'].value_counts())

print("\nSample rows for each specialist:")
for specialist in df['Specialist'].unique():
    sample = df[df['Specialist'] == specialist].head(2)
    print(f"\n=== {specialist} ===")
    for _, row in sample.iterrows():
        symptoms = [col for col in df.columns if col != 'Specialist' and row[col] == 1]
        print(f"  Symptoms: {symptoms}")

print(f"\nTotal rows: {len(df)}")
print(f"Unique specialists: {df['Specialist'].nunique()}") 