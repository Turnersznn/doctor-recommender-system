import pandas as pd
import joblib

# Load model
model = joblib.load("content_model.pkl")

# Load column structure
df = pd.read_excel("Specialist.xlsx")
df = df.drop(columns=["Unnamed: 0"], errors="ignore")
columns = df.columns[:-1]  # All symptom columns

# User symptoms (EXAMPLE)
input_symptoms = ["itching", "skin rash", "red spots"]

# Convert input symptoms to vector
input_data = {col: 0 for col in columns}

for symptom in input_symptoms:
    # Case-insensitive matching
    for col in columns:
        if symptom.lower().replace(" ", "") == col.lower().replace(" ", ""):
            input_data[col] = 1
            break

input_df = pd.DataFrame([input_data])

# Predict
prediction = model.predict(input_df)
print("🔍 Predicted Specialist:", prediction[0])
