#!/usr/bin/env python3
"""
Quick add dental symptoms to existing model
"""

import pandas as pd
import numpy as np
import joblib
import pickle
from sklearn.ensemble import RandomForestClassifier

def quick_add_dental():
    print("🦷 Quick adding dental symptoms...")
    
    # Load existing features
    with open('feature_columns_HIGH_ACCURACY.pkl', 'rb') as f:
        existing_features = pickle.load(f)
    
    # Define dental and eye symptoms
    dental_symptoms = [
        'tooth_pain', 'toothache', 'tooth_sensitivity', 'dental_pain',
        'gum_pain', 'jaw_pain', 'bleeding_gums', 'swollen_gums',
        'bad_breath', 'mouth_sores', 'broken_tooth', 'wisdom_tooth_pain'
    ]

    eye_symptoms = [
        'eye_pain', 'double_vision', 'vision_loss', 'eye_redness',
        'eye_discharge', 'dry_eyes', 'light_sensitivity', 'floaters', 'flashing_lights'
    ]

    new_symptoms = dental_symptoms + eye_symptoms
    
    # Combine features
    all_features = sorted(list(set(existing_features + new_symptoms)))

    print(f"📝 Added {len(dental_symptoms)} dental symptoms")
    print(f"📝 Added {len(eye_symptoms)} eye symptoms")
    print(f"📝 Total features: {len(all_features)}")
    
    # Create simple training data
    training_data = []
    
    # Existing high-priority symptoms
    priority_symptoms = {
        'joint_pain': 'Rheumatologists',
        'neck_pain': 'Rheumatologists',
        'cough': 'Pulmonologist',
        'chest_pain': 'Cardiologist',
        'depression': 'Psychiatrist',
        'skin_rash': 'Dermatologist',
        'headache': 'Neurologist',
        'abdominal_pain': 'Gastroenterologist',
        'throat_irritation': 'Otolaryngologist',
        'runny_nose': 'Otolaryngologist',
        
        # Dental symptoms
        'tooth_pain': 'Dentist',
        'toothache': 'Dentist',
        'tooth_sensitivity': 'Dentist',
        'dental_pain': 'Dentist',
        'gum_pain': 'Dentist',
        'jaw_pain': 'Dentist',
        'bleeding_gums': 'Dentist',
        'swollen_gums': 'Dentist',
        'bad_breath': 'Dentist',
        'mouth_sores': 'Dentist',
        'broken_tooth': 'Dentist',
        'wisdom_tooth_pain': 'Dentist',

        # Eye symptoms
        'eye_pain': 'Ophthalmologist',
        'double_vision': 'Ophthalmologist',
        'vision_loss': 'Ophthalmologist',
        'eye_redness': 'Ophthalmologist',
        'eye_discharge': 'Ophthalmologist',
        'dry_eyes': 'Ophthalmologist',
        'light_sensitivity': 'Ophthalmologist',
        'floaters': 'Ophthalmologist',
        'flashing_lights': 'Ophthalmologist'
    }
    
    # Add training samples
    for symptom, specialist in priority_symptoms.items():
        for _ in range(100):  # 100 samples per symptom
            feature_vector = {s: 0 for s in all_features}
            feature_vector[symptom] = 1
            feature_vector['specialist'] = specialist
            training_data.append(feature_vector)
    
    # Convert to DataFrame
    training_df = pd.DataFrame(training_data)
    
    print(f"✅ Created {len(training_df)} training samples")
    
    # Train simple model
    X = training_df[all_features]
    y = training_df['specialist']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    print("✅ Model trained")
    
    # Test dental symptoms
    print("\n🦷 Testing dental symptoms:")

    for symptom in dental_symptoms:
        if symptom in all_features:
            test_input = pd.DataFrame([[0] * len(all_features)], columns=all_features)
            test_input[symptom] = 1
            prediction = model.predict(test_input)[0]
            probability = model.predict_proba(test_input)[0].max()

            status = "✅" if prediction == 'Dentist' else "❌"
            print(f"{status} {symptom:<20} -> {prediction} ({probability:.3f})")

    # Test eye symptoms
    print("\n👁️ Testing eye symptoms:")

    for symptom in eye_symptoms:
        if symptom in all_features:
            test_input = pd.DataFrame([[0] * len(all_features)], columns=all_features)
            test_input[symptom] = 1
            prediction = model.predict(test_input)[0]
            probability = model.predict_proba(test_input)[0].max()

            status = "✅" if prediction == 'Ophthalmologist' else "❌"
            print(f"{status} {symptom:<20} -> {prediction} ({probability:.3f})")
    
    # Save model
    joblib.dump(model, 'content_model_WITH_DENTAL_AND_EYE.pkl')
    with open('feature_columns_WITH_DENTAL_AND_EYE.pkl', 'wb') as f:
        pickle.dump(all_features, f)

    print(f"\n💾 Saved model with dental and eye symptoms")

if __name__ == "__main__":
    quick_add_dental()
