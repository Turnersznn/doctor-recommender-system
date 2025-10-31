import pandas as pd

# Load the data
df = pd.read_excel("Specialist.xlsx")
cols = [col for col in df.columns if not col.lower().startswith('unnamed')]
df = df[cols]

# Get all symptom columns (excluding the target column 'Disease')
symptom_columns = [col for col in df.columns if col != 'Disease']

print(f"Total symptoms available: {len(symptom_columns)}")
print("\nAll available symptoms:")
for i, symptom in enumerate(symptom_columns, 1):
    print(f"{i:2d}. {symptom}")

print(f"\nTarget specialists (Disease column):")
print(df['Disease'].unique())

print(f"\nSample data for first few rows:")
print(df[['Disease'] + symptom_columns[:5]].head()) 