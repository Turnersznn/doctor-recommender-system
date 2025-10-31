import joblib
import pandas as pd

# Load the model
model = joblib.load("content_model_specialist_fixed.pkl")

# Load feature columns
feature_df = pd.read_excel("Specialist_clean_clinical.xlsx")
feature_columns = [col for col in feature_df.columns if col != 'Specialist']

# Test itching
itching_symptoms = {"itching": 1}
X = pd.DataFrame([[itching_symptoms.get(col, 0) for col in feature_columns]], columns=feature_columns)
prediction = model.predict(X)[0]

print(f"Itching prediction: {prediction}")

# Test a few other symptoms
test_symptoms = {
    "nausea": {"nausea": 1},
    "headache": {"headache": 1},
    "cough": {"cough": 1},
    "chest_pain": {"chest_pain": 1},
    "skin_rash": {"skin_rash": 1}
}

print("\nOther symptom predictions:")
for symptom_name, symptoms in test_symptoms.items():
    X = pd.DataFrame([[symptoms.get(col, 0) for col in feature_columns]], columns=feature_columns)
    prediction = model.predict(X)[0]
    print(f"{symptom_name}: {prediction}") 