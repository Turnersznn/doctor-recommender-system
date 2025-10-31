import joblib
import pandas as pd
import pickle

# Load the model and feature columns
model = joblib.load("content_model_specialist_fixed.pkl")
with open('feature_columns.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

# Test back_pain prediction
print("Testing back_pain prediction:")
input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
if 'back_pain' in feature_columns:
    input_data['back_pain'] = 1
    prediction = model.predict(input_data)[0]
    print(f"back_pain: {prediction}")
    
    if prediction == 'Rheumatologists':
        print("✅ Correct! back_pain predicts Rheumatologists")
    else:
        print(f"❌ Wrong! back_pain predicts {prediction} but should predict Rheumatologists")

# Test other symptoms for comparison
test_symptoms = ['headache', 'joint_pain', 'neck_pain']
for symptom in test_symptoms:
    if symptom in feature_columns:
        input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
        input_data[symptom] = 1
        prediction = model.predict(input_data)[0]
        print(f"{symptom}: {prediction}") 