import joblib
import pandas as pd
import pickle

# Load the model and feature columns
model = joblib.load("content_model_specialist_fixed.pkl")
with open('feature_columns.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

# Test diarrhoea prediction
print("Testing diarrhoea prediction:")
input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
if 'diarrhoea' in feature_columns:
    input_data['diarrhoea'] = 1
    prediction = model.predict(input_data)[0]
    print(f"diarrhoea: {prediction}")
    
    if prediction == 'Gastroenterologist':
        print("✅ Correct! diarrhoea predicts Gastroenterologist")
    else:
        print(f"❌ Wrong! diarrhoea predicts {prediction} but should predict Gastroenterologist")

# Test other gastrointestinal symptoms
test_symptoms = ['nausea', 'vomiting', 'abdominal_pain', 'stomach_pain']
for symptom in test_symptoms:
    if symptom in feature_columns:
        input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
        input_data[symptom] = 1
        prediction = model.predict(input_data)[0]
        print(f"{symptom}: {prediction}") 