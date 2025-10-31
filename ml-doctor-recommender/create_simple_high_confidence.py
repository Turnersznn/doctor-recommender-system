#!/usr/bin/env python3
"""
Create simple high confidence model
"""

import pandas as pd
import numpy as np
import joblib
import pickle
from sklearn.tree import DecisionTreeClassifier

def create_simple_high_confidence():
    print("⚡ Creating SIMPLE HIGH CONFIDENCE model...")
    
    # Load existing features
    with open('feature_columns_WITH_DENTAL_AND_EYE.pkl', 'rb') as f:
        all_features = pickle.load(f)
    
    # Key symptoms only
    KEY_MAPPINGS = {
        'joint_pain': 'Rheumatologists',
        'neck_pain': 'Rheumatologists',
        'back_pain': 'Rheumatologists',
        'cough': 'Pulmonologist',
        'chest_pain': 'Cardiologist',
        'depression': 'Psychiatrist',
        'anxiety': 'Psychiatrist',
        'skin_rash': 'Dermatologist',
        'itching': 'Dermatologist',
        'abdominal_pain': 'Gastroenterologist',
        'stomach_pain': 'Gastroenterologist',
        'nausea': 'Gastroenterologist',
        'vomiting': 'Gastroenterologist',
        'headache': 'Neurologist',
        'dizziness': 'Neurologist',
        'throat_irritation': 'Otolaryngologist',
        'runny_nose': 'Otolaryngologist',
        'sore_throat': 'Otolaryngologist',
        'toothache': 'Dentist',
        'tooth_pain': 'Dentist',
        'jaw_pain': 'Dentist',
        'eye_pain': 'Ophthalmologist',
        'vision_loss': 'Ophthalmologist',
        'blurred_and_distorted_vision': 'Ophthalmologist',
        'fever': 'Internal Medcine',
        'fatigue': 'Internal Medcine'
    }
    
    print(f"📝 Key mappings: {len(KEY_MAPPINGS)}")
    
    # Create simple training data
    training_data = []
    
    # Add key mappings with high weight
    for symptom, specialist in KEY_MAPPINGS.items():
        if symptom in all_features:
            for _ in range(500):  # 500 samples per key symptom
                feature_vector = {s: 0 for s in all_features}
                feature_vector[symptom] = 1
                feature_vector['specialist'] = specialist
                training_data.append(feature_vector)
    
    # Convert to DataFrame
    training_df = pd.DataFrame(training_data)
    
    print(f"✅ Created {len(training_df)} training samples")
    
    # Train simple decision tree for high confidence
    X = training_df[all_features]
    y = training_df['specialist']
    
    model = DecisionTreeClassifier(
        max_depth=None,
        min_samples_split=2,
        min_samples_leaf=1,
        random_state=42
    )
    
    print("🤖 Training simple model...")
    model.fit(X, y)
    
    print(f"✅ Model trained")
    
    # Test key mappings
    print(f"\n🧪 Testing key mappings:")
    
    perfect_count = 0
    total_count = 0
    
    for symptom, expected in KEY_MAPPINGS.items():
        if symptom in all_features:
            test_input = pd.DataFrame([[0] * len(all_features)], columns=all_features)
            test_input[symptom] = 1
            prediction = model.predict(test_input)[0]
            probability = model.predict_proba(test_input)[0].max()
            
            is_correct = prediction == expected
            if is_correct:
                perfect_count += 1
            total_count += 1
            
            status = "✅" if is_correct else "❌"
            confidence_level = "PERFECT" if probability > 0.99 else "ULTRA" if probability > 0.95 else "HIGH" if probability > 0.8 else "MED"
            
            print(f"{status} {symptom:<25} -> {prediction:<20} ({probability:.3f} {confidence_level})")
    
    final_accuracy = perfect_count / total_count if total_count > 0 else 0
    print(f"\n📊 Accuracy: {perfect_count}/{total_count} = {final_accuracy:.1%}")
    
    # Save model
    joblib.dump(model, 'content_model_SIMPLE_HIGH_CONFIDENCE.pkl')
    with open('feature_columns_SIMPLE_HIGH_CONFIDENCE.pkl', 'wb') as f:
        pickle.dump(all_features, f)
    
    print(f"\n💾 Saved SIMPLE HIGH CONFIDENCE model")

if __name__ == "__main__":
    create_simple_high_confidence()
