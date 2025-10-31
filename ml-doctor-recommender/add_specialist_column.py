import pandas as pd

# Load the main data
df = pd.read_excel("Specialist.xlsx")

# Load the mapping data
mapping = pd.read_csv("Doctor_Versus_Disease.csv", encoding="latin1")
mapping.columns = ['Disease', 'Specialist']

# Create the mapping dictionary
disease_to_specialist = dict(zip(mapping['Disease'].str.strip(), mapping['Specialist'].str.strip()))

# Map diseases to specialists, fill missing with "General Practitioner"
df['Specialist'] = df['Disease'].map(disease_to_specialist).fillna('General Practitioner')

# Save the updated data
df.to_excel("Specialist_with_specialist.xlsx", index=False)

# Print some stats
print("✅ Added Specialist column and saved as Specialist_with_specialist.xlsx")
print(f"Total rows: {len(df)}")
print(f"Unique specialists: {df['Specialist'].nunique()}")
print("\nSpecialist distribution:")
print(df['Specialist'].value_counts()) 