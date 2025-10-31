#!/usr/bin/env python3
import pandas as pd
import joblib
import pickle

# Load model
model = joblib.load('content_model_HIGH_ACCURACY.pkl')
with open('feature_columns_HIGH_ACCURACY.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

# Test throat_irritation + runny_nose
test_input = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
test_input['throat_irritation'] = 1
test_input['runny_nose'] = 1

# Get predictions
proba = model.predict_proba(test_input)[0]
classes = model.classes_

# Show top 10 predictions
top_indices = proba.argsort()[-10:][::-1]
print('Top 10 predictions for throat_irritation + runny_nose:')
for i in top_indices:
    print(f'{classes[i]}: {proba[i]:.6f}')

print('\nExpected: ENT/Otolaryngologist should be #1')
print('Actual: First prediction is:', classes[top_indices[0]])
