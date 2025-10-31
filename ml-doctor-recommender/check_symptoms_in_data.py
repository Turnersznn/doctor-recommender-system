import pandas as pd

# Load the data
df = pd.read_excel("Specialist.xlsx")

# Get symptom columns (all except Disease and Unnamed: 0)
symptom_cols = [col for col in df.columns if col not in ['Disease', 'Unnamed: 0']]

print("Symptoms in the data:")
for i, symptom in enumerate(symptom_cols, 1):
    print(f"{i:2d}. {symptom}")

print(f"\nTotal symptoms: {len(symptom_cols)}")

# Check which symptoms are most common
print("\nMost common symptoms:")
symptom_counts = {}
for symptom in symptom_cols:
    count = df[symptom].sum()
    if count > 0:
        symptom_counts[symptom] = count

# Sort by count
sorted_symptoms = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)
for symptom, count in sorted_symptoms[:20]:
    print(f"{symptom}: {count}") 