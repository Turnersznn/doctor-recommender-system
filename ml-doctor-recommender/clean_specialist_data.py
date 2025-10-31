import pandas as pd

# Load the data
input_file = "Specialist_fixed.xlsx"
df = pd.read_excel(input_file)

# Drop Unnamed: 0 if present
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# Strip leading/trailing spaces from all column names
cleaned_columns = [col.strip() for col in df.columns]
df.columns = cleaned_columns

# Rename Disease to Specialist if present
if 'Disease' in df.columns:
    df = df.rename(columns={'Disease': 'Specialist'})

# Ensure all symptom columns are 0/1 (except Specialist)
for col in df.columns:
    if col != 'Specialist':
        df[col] = df[col].fillna(0)
        df[col] = df[col].apply(lambda x: 1 if x == 1 else 0)

# Print unique specialists
print("Unique specialists:")
print(df['Specialist'].value_counts())

# Save cleaned data
output_file = "Specialist_cleaned.xlsx"
df.to_excel(output_file, index=False)
print(f"✅ Cleaned data saved to {output_file}") 