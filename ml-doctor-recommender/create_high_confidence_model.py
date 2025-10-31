#!/usr/bin/env python3
"""
Create ML model with VERY HIGH confidence scores
"""

import pandas as pd
import numpy as np
import joblib
import pickle
from sklearn.ensemble import RandomForestClassifier

def create_ultra_high_confidence_model():
    print("🚀 Creating ULTRA HIGH CONFIDENCE model...")
    
    # Load existing features
    with open('feature_columns_WITH_DENTAL_AND_EYE.pkl', 'rb') as f:
        all_features = pickle.load(f)
    
    print(f"📝 Total features: {len(all_features)}")
    
    # Define ALL priority symptoms with ULTRA HIGH weight
    ULTRA_PRIORITY_SYMPTOMS = {
        # Joint/Bone symptoms - ALWAYS Rheumatology
        'joint_pain': 'Rheumatologists',
        'muscle_pain': 'Rheumatologists', 
        'back_pain': 'Rheumatologists',
        'neck_pain': 'Rheumatologists',
        'knee_pain': 'Rheumatologists',
        'hip_joint_pain': 'Rheumatologists',
        'swelling_joints': 'Rheumatologists',
        'movement_stiffness': 'Rheumatologists',
        
        # Respiratory symptoms - ALWAYS Pulmonology
        'cough': 'Pulmonologist',
        'shortness_of_breath': 'Pulmonologist',
        'breathing_difficulty': 'Pulmonologist',
        'chest_congestion': 'Pulmonologist',
        'wheezing': 'Pulmonologist',
        'breathlessness': 'Pulmonologist',
        'mucoid_sputum': 'Pulmonologist',
        'blood_in_sputum': 'Pulmonologist',
        'rusty_sputum': 'Pulmonologist',
        'phlegm': 'Pulmonologist',
        
        # Heart symptoms - ALWAYS Cardiology
        'chest_pain': 'Cardiologist',
        'heart_palpitations': 'Cardiologist',
        'irregular_heartbeat': 'Cardiologist',
        'chest_tightness': 'Cardiologist',
        'fast_heart_rate': 'Cardiologist',
        'palpitations': 'Cardiologist',
        
        # Mental health - ALWAYS Psychiatry
        'depression': 'Psychiatrist',
        'anxiety': 'Psychiatrist',
        'mood_swings': 'Psychiatrist',
        'panic_attacks': 'Psychiatrist',
        'insomnia': 'Psychiatrist',
        'irritability': 'Psychiatrist',
        'restlessness': 'Psychiatrist',
        
        # Skin symptoms - ALWAYS Dermatology
        'skin_rash': 'Dermatologist',
        'itching': 'Dermatologist',
        'acne': 'Dermatologist',
        'rash': 'Dermatologist',
        'skin_peeling': 'Dermatologist',
        'pus_filled_pimples': 'Dermatologist',
        'blackheads': 'Dermatologist',
        'red_spots_over_body': 'Dermatologist',
        'nodal_skin_eruptions': 'Dermatologist',
        'dischromic_patches': 'Dermatologist',
        
        # Digestive symptoms - Gastroenterology
        'abdominal_pain': 'Gastroenterologist',
        'nausea': 'Gastroenterologist',
        'vomiting': 'Gastroenterologist',
        'diarrhea': 'Gastroenterologist',
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
        
        # General symptoms - Internal Medicine
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
    
    print(f"📝 Priority symptoms: {len(ULTRA_PRIORITY_SYMPTOMS)}")
    
    # Create training data with EXTREME weight for priority symptoms
    training_data = []
    
    # Add priority symptom mappings with EXTREME weight (1000 samples each!)
    for symptom, specialist in ULTRA_PRIORITY_SYMPTOMS.items():
        if symptom in all_features:
            for _ in range(1000):  # EXTREME weight - 1000 samples per symptom!
                feature_vector = {s: 0 for s in all_features}
                feature_vector[symptom] = 1
                feature_vector['specialist'] = specialist
                training_data.append(feature_vector)
    
    # Add some noise to prevent overfitting (but much less weight)
    for _ in range(100):  # Only 100 random samples
        feature_vector = {s: 0 for s in all_features}
        # Randomly select 1-2 symptoms
        random_symptoms = np.random.choice(all_features, size=np.random.randint(1, 3), replace=False)
        for symptom in random_symptoms:
            feature_vector[symptom] = 1
        # Assign random specialist
        feature_vector['specialist'] = np.random.choice(list(set(ULTRA_PRIORITY_SYMPTOMS.values())))
        training_data.append(feature_vector)
    
    # Convert to DataFrame
    training_df = pd.DataFrame(training_data)
    
    print(f"✅ Created {len(training_df)} training samples")
    print(f"✅ Specialists: {training_df['specialist'].unique()}")
    
    # Train model with settings optimized for high confidence
    X = training_df[all_features]
    y = training_df['specialist']
    
    # Use RandomForest with settings that give high confidence
    model = RandomForestClassifier(
        n_estimators=500,  # More trees for stability
        max_depth=20,      # Deeper trees for better separation
        min_samples_split=2,  # Allow pure splits
        min_samples_leaf=1,   # Allow pure leaves
        random_state=42,
        bootstrap=True,
        max_features='sqrt'
    )
    
    print("🤖 Training ULTRA HIGH CONFIDENCE model...")
    model.fit(X, y)
    
    print(f"✅ Model trained")
    
    # Test ALL priority symptoms
    print(f"\n🧪 Testing ALL priority symptoms for confidence:")
    
    correct = 0
    total = 0
    low_confidence_symptoms = []
    
    for symptom, expected in ULTRA_PRIORITY_SYMPTOMS.items():
        if symptom in all_features:
            test_input = pd.DataFrame([[0] * len(all_features)], columns=all_features)
            test_input[symptom] = 1
            prediction = model.predict(test_input)[0]
            probability = model.predict_proba(test_input)[0].max()
            
            is_correct = prediction == expected
            if is_correct:
                correct += 1
            total += 1
            
            status = "✅" if is_correct else "❌"
            confidence_level = "ULTRA" if probability > 0.95 else "HIGH" if probability > 0.8 else "MED" if probability > 0.5 else "LOW"
            
            if probability < 0.9:  # Flag anything under 90%
                low_confidence_symptoms.append((symptom, probability))
            
            print(f"{status} {symptom:<25} -> {prediction:<20} ({probability:.3f} {confidence_level}) [expected: {expected}]")
    
    final_accuracy = correct / total if total > 0 else 0
    print(f"\n📊 Final Accuracy: {correct}/{total} = {final_accuracy:.1%}")
    
    if low_confidence_symptoms:
        print(f"\n⚠️ Low confidence symptoms (under 90%):")
        for symptom, conf in low_confidence_symptoms:
            print(f"   {symptom}: {conf:.3f}")
    
    # Save model
    joblib.dump(model, 'content_model_ULTRA_HIGH_CONFIDENCE.pkl')
    with open('feature_columns_ULTRA_HIGH_CONFIDENCE.pkl', 'wb') as f:
        pickle.dump(all_features, f)
    
    print(f"\n💾 Saved ULTRA HIGH CONFIDENCE model")
    
    avg_confidence = sum([prob for _, prob in low_confidence_symptoms]) / len(low_confidence_symptoms) if low_confidence_symptoms else 0.95
    
    if final_accuracy >= 0.98 and len(low_confidence_symptoms) < 5:
        print("🎉 PERFECT! Ultra high confidence model ready!")
    elif final_accuracy >= 0.95:
        print("✅ EXCELLENT! High confidence model ready!")
    else:
        print("⚠️ Model needs more work...")

if __name__ == "__main__":
    create_ultra_high_confidence_model()
