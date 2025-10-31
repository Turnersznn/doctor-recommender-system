import joblib
import pandas as pd

# Load the model
model = joblib.load("content_model_specialist_fixed.pkl")

# Load feature columns
feature_df = pd.read_excel("Specialist_simple.xlsx")
feature_columns = [col for col in feature_df.columns if col != 'Specialist']

# Test various eye symptoms
eye_symptoms = [
    "watering_from_eyes",
    "yellowing_of_eyes", 
    "sunken_eyes",
    "pain_behind_the_eyes",
    "redness_of_eyes",
    "blurred_and_distorted_vision",
    "visual_disturbances"
]

print("Testing eye symptoms:")
for symptom in eye_symptoms:
    if symptom in feature_columns:
        symptoms_dict = {symptom: 1}
        X = pd.DataFrame([[symptoms_dict.get(col, 0) for col in feature_columns]], columns=feature_columns)
        prediction = model.predict(X)[0]
        print(f"{symptom}: {prediction}")
    else:
        print(f"{symptom}: NOT FOUND in feature columns") 