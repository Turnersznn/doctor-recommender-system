import joblib
import pandas as pd

# Load the model
model = joblib.load("content_model_specialist.pkl")

# Load the feature columns
df = pd.read_excel("Specialist_with_specialist.xlsx")
df = df.drop(columns=["Unnamed: 0"], errors="ignore")
feature_columns = df.columns[:-2].tolist()  # All columns except last two (Disease, Specialist)

print("Feature columns:", feature_columns[:10], "...")

# Test different symptom combinations
test_cases = [
    {"fever": 1, "cough": 0, "headache": 0},
    {"itching": 1, "skin_rash": 0, "fever": 0},
    {"headache": 1, "dizziness": 0, "fever": 0},
    {"stomach_pain": 1, "nausea": 0, "fever": 0},
    {"chest_pain": 1, "shortness_of_breath": 0, "fever": 0},
]

for i, symptoms in enumerate(test_cases, 1):
    # Create input data
    input_data = {col: symptoms.get(col, 0) for col in feature_columns}
    X = pd.DataFrame([input_data])
    
    # Predict
    prediction = model.predict(X)[0]
    print(f"Test {i}: {symptoms} → Predicted: {prediction}")

print("\nAll unique predictions from training data:")
print(df['Specialist'].unique()) 