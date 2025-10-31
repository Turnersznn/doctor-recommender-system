#!/usr/bin/env python3
import pandas as pd
import joblib
import pickle

# Load model
model = joblib.load('content_model_WITH_DENTAL_AND_EYE.pkl')
with open('feature_columns_WITH_DENTAL_AND_EYE.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

print('Available dental symptoms in model:')
dental_symptoms = [s for s in feature_columns if 'tooth' in s or 'dental' in s or 'gum' in s or 'jaw' in s]
for symptom in dental_symptoms:
    print(f'  {symptom}')

print(f'\nChecking symptoms:')
test_symptoms = ['toothache_severe', 'toothache', 'jaw_pain']
for symptom in test_symptoms:
    if symptom in feature_columns:
        test_input = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
        test_input[symptom] = 1
        prediction = model.predict(test_input)[0]
        probability = model.predict_proba(test_input)[0].max()
        print(f'{symptom} -> {prediction} ({probability:.3f})')
    else:
        print(f'{symptom} -> NOT IN MODEL')
