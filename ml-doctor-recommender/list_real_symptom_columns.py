import pandas as pd
import re

df = pd.read_excel("Specialist.xlsx")
cols = [col for col in df.columns if not col.lower().startswith('unnamed')]
df = df[cols]

symptom_columns = [col for col in df.columns if col != 'Disease']

print("All actual symptom columns (with spaces):")
for i, col in enumerate(symptom_columns, 1):
    print(f"{i:2d}. '{col}'")

# Generate mapping: user-friendly (no spaces, all lowercase, underscores) to real column name
mapping = {}
for col in symptom_columns:
    # Remove leading/trailing spaces, replace multiple spaces/underscores with single underscore, lowercase
    friendly = re.sub(r'\s+', '_', col.strip()).lower()
    mapping[friendly] = col

print("\nUser-friendly to real column name mapping:")
for friendly, real in mapping.items():
    print(f"  '{friendly}': '{real}',") 