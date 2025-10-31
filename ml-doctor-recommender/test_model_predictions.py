import pickle
import pandas as pd
import numpy as np

# Load the model
with open('content_model_specialist_fixed.pkl', 'rb') as f:
    model = pickle.load(f)

# Load training data to get feature columns
df = pd.read_excel('Specialist_simple.xlsx')
feature_columns = [col for col in df.columns if col != 'Specialist']

# Test symptoms that should NOT predict Ophthalmologist
test_symptoms = [
    'headache', 'cough', 'nausea', 'chest_pain', 'abdominal_pain',
    'itching', 'skin_rash', 'fatigue', 'fever', 'dizziness'
]

print("Testing symptoms that should NOT predict Ophthalmologist:")
print("=" * 60)

for symptom in test_symptoms:
    # Create input with just this symptom
    input_data = {col: 0 for col in feature_columns}
    if symptom in feature_columns:
        input_data[symptom] = 1
    
    # Convert to array for prediction
    input_array = np.array([[input_data[col] for col in feature_columns]])
    
    # Predict
    prediction = model.predict(input_array)[0]
    
    print(f"{symptom:20} -> {prediction}")
    
    if prediction == 'Ophthalmologist':
        print(f"  ⚠️  WARNING: {symptom} incorrectly predicts Ophthalmologist!")

print("\n" + "=" * 60)
print("Testing eye symptoms that SHOULD predict Ophthalmologist:")

eye_symptoms = [
    'watering_from_eyes', 'yellowing_of_eyes', 'sunken_eyes', 
    'pain_behind_the_eyes', 'redness_of_eyes', 'blurred_and_distorted_vision'
]

for symptom in eye_symptoms:
    input_data = {col: 0 for col in feature_columns}
    if symptom in feature_columns:
        input_data[symptom] = 1
    
    input_array = np.array([[input_data[col] for col in feature_columns]])
    prediction = model.predict(input_array)[0]
    
    print(f"{symptom:25} -> {prediction}")
    
    if prediction != 'Ophthalmologist':
        print(f"  ⚠️  WARNING: {symptom} should predict Ophthalmologist but predicts {prediction}!") 