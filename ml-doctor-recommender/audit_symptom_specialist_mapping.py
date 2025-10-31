import pandas as pd

# Load the data
df = pd.read_excel("Specialist.xlsx")
cols = [col for col in df.columns if not col.lower().startswith('unnamed')]
df = df[cols]

# List of key symptoms to audit (with correct column names including leading spaces)
key_symptoms = [
    ' nausea', ' vomiting', ' abdominal_pain', ' diarrhoea', ' constipation',
    ' headache', ' dizziness', ' chest_pain', 'cough', ' skin_rash', 'itching',
    ' joint_pain', ' back_pain', ' muscle_weakness', ' fatigue', ' mild_fever',
    ' breathlessness', ' fast_heart_rate', ' loss_of_appetite', ' weight_loss'
]

# Print which specialists are assigned for each key symptom
for symptom in key_symptoms:
    if symptom not in df.columns:
        print(f"Symptom '{symptom}' not found in data.")
        continue
    print(f"\n=== {symptom.upper()} ===")
    # Get all rows where this symptom is present
    present = df[df[symptom] == 1]
    if present.empty:
        print("  No cases with this symptom.")
        continue
    # Count specialists
    counts = present['Disease'].value_counts()
    print(counts) 