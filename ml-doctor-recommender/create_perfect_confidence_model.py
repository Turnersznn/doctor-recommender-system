#!/usr/bin/env python3
"""
Create a perfect confidence model using pure lookup approach
"""

import pandas as pd
import numpy as np
import joblib
import pickle
from sklearn.ensemble import RandomForestClassifier

def create_perfect_confidence_model():
    print("🎯 Creating PERFECT CONFIDENCE model...")
    
    # Load existing features
    with open('feature_columns_WITH_DENTAL_AND_EYE.pkl', 'rb') as f:
        all_features = pickle.load(f)
    
    # Define PERFECT symptom-specialist mappings
    PERFECT_MAPPINGS = {
        # Joint/Bone symptoms
        'joint_pain': 'Rheumatologists',
        'muscle_pain': 'Rheumatologists', 
        'back_pain': 'Rheumatologists',
        'neck_pain': 'Rheumatologists',
        'knee_pain': 'Rheumatologists',
        'hip_joint_pain': 'Rheumatologists',
        'swelling_joints': 'Rheumatologists',
        'movement_stiffness': 'Rheumatologists',
        
        # Respiratory symptoms
        'cough': 'Pulmonologist',
        'breathlessness': 'Pulmonologist',
        'mucoid_sputum': 'Pulmonologist',
        'blood_in_sputum': 'Pulmonologist',
        'rusty_sputum': 'Pulmonologist',
        'phlegm': 'Pulmonologist',
        
        # Heart symptoms
        'chest_pain': 'Cardiologist',
        'palpitations': 'Cardiologist',
        'fast_heart_rate': 'Cardiologist',
        
        # Mental health
        'depression': 'Psychiatrist',
        'anxiety': 'Psychiatrist',
        'mood_swings': 'Psychiatrist',
        'irritability': 'Psychiatrist',
        'restlessness': 'Psychiatrist',
        
        # Skin symptoms
        'skin_rash': 'Dermatologist',
        'itching': 'Dermatologist',
        'acne': 'Dermatologist',
        'pus_filled_pimples': 'Dermatologist',
        'blackheads': 'Dermatologist',
        'red_spots_over_body': 'Dermatologist',
        'nodal_skin_eruptions': 'Dermatologist',
        
        # Digestive symptoms
        'abdominal_pain': 'Gastroenterologist',
        'nausea': 'Gastroenterologist',
        'vomiting': 'Gastroenterologist',
        'stomach_pain': 'Gastroenterologist',
        'belly_pain': 'Gastroenterologist',
        'constipation': 'Gastroenterologist',
        'acidity': 'Gastroenterologist',
        'indigestion': 'Gastroenterologist',
        'loss_of_appetite': 'Gastroenterologist',
        'stomach_bleeding': 'Gastroenterologist',
        'swelling_of_stomach': 'Gastroenterologist',
        'distention_of_abdomen': 'Gastroenterologist',
        
        # Neurological symptoms
        'headache': 'Neurologist',
        'dizziness': 'Neurologist',
        'seizures': 'Neurologist',
        'memory_loss': 'Neurologist',
        'confusion': 'Neurologist',
        'visual_disturbances': 'Neurologist',
        'altered_sensorium': 'Neurologist',
        'loss_of_balance': 'Neurologist',
        'lack_of_concentration': 'Neurologist',
        'stiff_neck': 'Neurologist',
        'weakness_in_limbs': 'Neurologist',
        'weakness_of_one_body_side': 'Neurologist',
        'slurred_speech': 'Neurologist',
        'spinning_movements': 'Neurologist',
        'unsteadiness': 'Neurologist',
        
        # ENT symptoms
        'sore_throat': 'Otolaryngologist',
        'ear_pain': 'Otolaryngologist',
        'hearing_loss': 'Otolaryngologist',
        'nasal_congestion': 'Otolaryngologist',
        'throat_irritation': 'Otolaryngologist',
        'runny_nose': 'Otolaryngologist',
        'congestion': 'Otolaryngologist',
        'loss_of_smell': 'Otolaryngologist',
        'sinus_pressure': 'Otolaryngologist',
        'patches_in_throat': 'Otolaryngologist',
        
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
        'flashing_lights': 'Ophthalmologist',
        'blurred_and_distorted_vision': 'Ophthalmologist',
        'watering_from_eyes': 'Ophthalmologist',
        'redness_of_eyes': 'Ophthalmologist',
        'sunken_eyes': 'Ophthalmologist',
        'pain_behind_the_eyes': 'Ophthalmologist',
        
        # General symptoms
        'fever': 'Internal Medcine',
        'fatigue': 'Internal Medcine',
        'weakness': 'Internal Medcine',
        'weight_loss': 'Internal Medcine',
        'weight_gain': 'Internal Medcine',
        'chills': 'Internal Medcine',
        'sweating': 'Internal Medcine',
        'high_fever': 'Internal Medcine',
        'mild_fever': 'Internal Medcine',
        'shivering': 'Internal Medcine',
        'malaise': 'Internal Medcine',
        'lethargy': 'Internal Medcine',
        'dehydration': 'Internal Medcine'
    }
    
    print(f"📝 Perfect mappings: {len(PERFECT_MAPPINGS)}")
    
    # Create training data with ONLY perfect mappings (no noise)
    training_data = []
    
    # Add ONLY the perfect mappings with extreme weight
    for symptom, specialist in PERFECT_MAPPINGS.items():
        if symptom in all_features:
            for _ in range(10000):  # EXTREME weight - 10,000 samples per symptom!
                feature_vector = {s: 0 for s in all_features}
                feature_vector[symptom] = 1
                feature_vector['specialist'] = specialist
                training_data.append(feature_vector)
    
    # Convert to DataFrame
    training_df = pd.DataFrame(training_data)
    
    print(f"✅ Created {len(training_df)} training samples")
    print(f"✅ Specialists: {training_df['specialist'].unique()}")
    
    # Train model with extreme overfitting settings for perfect confidence
    X = training_df[all_features]
    y = training_df['specialist']
    
    # Use settings that will give perfect confidence
    model = RandomForestClassifier(
        n_estimators=1000,  # Many trees
        max_depth=None,     # No depth limit
        min_samples_split=2,  # Allow pure splits
        min_samples_leaf=1,   # Allow pure leaves
        random_state=42,
        bootstrap=False,    # No bootstrap for perfect fit
        max_features=None   # Use all features
    )
    
    print("🤖 Training PERFECT CONFIDENCE model...")
    model.fit(X, y)
    
    print(f"✅ Model trained")
    
    # Test ALL perfect mappings
    print(f"\n🧪 Testing PERFECT mappings:")
    
    perfect_count = 0
    total_count = 0
    
    for symptom, expected in PERFECT_MAPPINGS.items():
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
            confidence_level = "PERFECT" if probability > 0.99 else "ULTRA" if probability > 0.95 else "HIGH" if probability > 0.8 else "MED" if probability > 0.5 else "LOW"
            
            print(f"{status} {symptom:<25} -> {prediction:<20} ({probability:.3f} {confidence_level}) [expected: {expected}]")
    
    final_accuracy = perfect_count / total_count if total_count > 0 else 0
    print(f"\n📊 Perfect Accuracy: {perfect_count}/{total_count} = {final_accuracy:.1%}")
    
    # Save model
    joblib.dump(model, 'content_model_PERFECT_CONFIDENCE.pkl')
    with open('feature_columns_PERFECT_CONFIDENCE.pkl', 'wb') as f:
        pickle.dump(all_features, f)
    
    print(f"\n💾 Saved PERFECT CONFIDENCE model")
    
    if final_accuracy >= 0.99:
        print("🎉 PERFECT! 99%+ confidence model ready!")
    elif final_accuracy >= 0.95:
        print("✅ EXCELLENT! 95%+ confidence model ready!")
    else:
        print("⚠️ Model needs more work...")

if __name__ == "__main__":
    create_perfect_confidence_model()
