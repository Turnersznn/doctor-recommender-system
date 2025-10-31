import joblib
import pandas as pd
import pickle

# Load the model and feature columns
model = joblib.load("content_model_specialist_fixed.pkl")
with open('feature_columns.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

# Test depression prediction
print("Testing depression prediction:")
input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
if 'depression' in feature_columns:
    input_data['depression'] = 1
    prediction = model.predict(input_data)[0]
    print(f"depression: {prediction}")
    
    if prediction == 'Neurologist':
        print("✅ Correct! depression predicts Neurologist")
    else:
        print(f"❌ Wrong! depression predicts {prediction} but should predict Neurologist")

# Test other neurological symptoms
test_symptoms = ['headache', 'dizziness', 'irritability']
for symptom in test_symptoms:
    if symptom in feature_columns:
        input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
        input_data[symptom] = 1
        prediction = model.predict(input_data)[0]
        print(f"{symptom}: {prediction}") 