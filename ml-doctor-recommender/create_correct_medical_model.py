#!/usr/bin/env python3
"""
Create a properly trained ML model with correct medical symptom-specialist mappings
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import pickle

# Correct medical symptom-to-specialist mappings
CORRECT_MEDICAL_MAPPINGS = {
    # Respiratory symptoms
    'cough': 'Pulmonology',
    'cough_severe': 'Pulmonology', 
    'shortness_of_breath': 'Pulmonology',
    'chest_pain': 'Cardiology',
    'wheezing': 'Pulmonology',
    'sore_throat': 'ENT',
    
    # Cardiovascular symptoms
    'heart_palpitations': 'Cardiology',
    'chest_tightness': 'Cardiology',
    'irregular_heartbeat': 'Cardiology',
    'high_blood_pressure': 'Cardiology',
    
    # Gastrointestinal symptoms
    'abdominal_pain': 'Gastroenterology',
    'nausea': 'Gastroenterology',
    'vomiting': 'Gastroenterology',
    'diarrhea': 'Gastroenterology',
    'constipation': 'Gastroenterology',
    'stomach_pain': 'Gastroenterology',
    
    # Neurological symptoms
    'headache': 'Neurology',
    'headache_severe': 'Neurology',
    'dizziness': 'Neurology',
    'seizures': 'Neurology',
    'memory_loss': 'Neurology',
    'confusion': 'Neurology',
    
    # Mental health symptoms
    'depression': 'Psychiatry',
    'anxiety': 'Psychiatry',
    'panic_attacks': 'Psychiatry',
    'mood_swings': 'Psychiatry',
    'insomnia': 'Psychiatry',
    
    # Dermatological symptoms
    'skin_rash': 'Dermatology',
    'skin_rash_severe': 'Dermatology',
    'itching': 'Dermatology',
    'itching_severe': 'Dermatology',
    'acne': 'Dermatology',
    'eczema': 'Dermatology',
    
    # Musculoskeletal symptoms
    'joint_pain': 'Rheumatology',
    'muscle_pain': 'Rheumatology',
    'back_pain': 'Orthopedics',
    'neck_pain': 'Orthopedics',
    'arthritis': 'Rheumatology',
    
    # Endocrine symptoms
    'fatigue': 'Endocrinology',
    'weight_loss': 'Endocrinology',
    'weight_gain': 'Endocrinology',
    'excessive_thirst': 'Endocrinology',
    'frequent_urination': 'Endocrinology',
    
    # Eye symptoms
    'blurred_vision': 'Ophthalmology',
    'eye_pain': 'Ophthalmology',
    'vision_loss': 'Ophthalmology',
    'double_vision': 'Ophthalmology',
    
    # ENT symptoms
    'ear_pain': 'ENT',
    'hearing_loss': 'ENT',
    'tinnitus': 'ENT',
    'nasal_congestion': 'ENT',
    
    # Urological symptoms
    'urinary_frequency': 'Urology',
    'painful_urination': 'Urology',
    'blood_in_urine': 'Urology',
    
    # General symptoms (Family Medicine)
    'fever': 'Family Medicine',
    'chills': 'Family Medicine',
    'sweating': 'Family Medicine',
    'general_weakness': 'Family Medicine'
}

def create_training_data():
    """Create comprehensive training data with correct medical mappings"""
    
    print("🏗️ Creating correct medical training data...")
    
    # Get all symptoms
    all_symptoms = list(CORRECT_MEDICAL_MAPPINGS.keys())
    
    # Create training data
    training_data = []
    
    # Single symptom cases (high confidence)
    for symptom, specialist in CORRECT_MEDICAL_MAPPINGS.items():
        # Create multiple variations for each symptom
        for _ in range(50):  # 50 samples per symptom
            row = {sym: 0 for sym in all_symptoms}
            row[symptom] = 1
            row['specialist'] = specialist
            training_data.append(row)
    
    # Multi-symptom cases (related symptoms)
    symptom_groups = {
        'Pulmonology': ['cough', 'cough_severe', 'shortness_of_breath', 'wheezing'],
        'Cardiology': ['chest_pain', 'heart_palpitations', 'chest_tightness', 'irregular_heartbeat'],
        'Gastroenterology': ['abdominal_pain', 'nausea', 'vomiting', 'diarrhea', 'stomach_pain'],
        'Neurology': ['headache', 'headache_severe', 'dizziness', 'confusion'],
        'Psychiatry': ['depression', 'anxiety', 'panic_attacks', 'mood_swings', 'insomnia'],
        'Dermatology': ['skin_rash', 'skin_rash_severe', 'itching', 'itching_severe'],
        'Rheumatology': ['joint_pain', 'muscle_pain', 'arthritis'],
        'Endocrinology': ['fatigue', 'weight_loss', 'weight_gain', 'excessive_thirst'],
        'ENT': ['sore_throat', 'ear_pain', 'hearing_loss', 'nasal_congestion']
    }
    
    # Create multi-symptom combinations
    for specialist, symptoms in symptom_groups.items():
        for _ in range(30):  # 30 combinations per specialist
            row = {sym: 0 for sym in all_symptoms}
            # Select 2-3 related symptoms
            selected_symptoms = np.random.choice(symptoms, size=min(len(symptoms), np.random.randint(2, 4)), replace=False)
            for symptom in selected_symptoms:
                row[symptom] = 1
            row['specialist'] = specialist
            training_data.append(row)
    
    # Convert to DataFrame
    df = pd.DataFrame(training_data)
    
    print(f"✅ Created {len(df)} training samples")
    print(f"✅ Specialists: {df['specialist'].unique()}")
    print(f"✅ Symptoms: {len(all_symptoms)}")
    
    return df, all_symptoms

def train_model():
    """Train the ML model with correct data"""
    
    print("🤖 Training new ML model...")
    
    # Create training data
    df, feature_columns = create_training_data()
    
    # Prepare features and target
    X = df[feature_columns]
    y = df['specialist']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    # Test model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Model trained with accuracy: {accuracy:.3f}")
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Test specific cases
    print("\n🧪 Testing specific cases:")
    test_cases = [
        (['cough'], 'Pulmonology'),
        (['depression'], 'Psychiatry'),
        (['chest_pain'], 'Cardiology'),
        (['skin_rash'], 'Dermatology'),
        (['headache'], 'Neurology'),
        (['abdominal_pain'], 'Gastroenterology')
    ]
    
    for symptoms, expected in test_cases:
        test_input = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
        for symptom in symptoms:
            if symptom in feature_columns:
                test_input[symptom] = 1
        
        prediction = model.predict(test_input)[0]
        probability = model.predict_proba(test_input)[0].max()
        
        status = "✅" if prediction == expected else "❌"
        print(f"{status} {symptoms} -> {prediction} (confidence: {probability:.3f}) [expected: {expected}]")
    
    return model, feature_columns

def save_model():
    """Train and save the corrected model"""
    
    print("💾 Creating and saving corrected ML model...")
    
    # Train model
    model, feature_columns = train_model()
    
    # Save model
    joblib.dump(model, 'content_model_corrected.pkl')
    print("✅ Saved model as content_model_corrected.pkl")
    
    # Save feature columns
    with open('feature_columns_corrected.pkl', 'wb') as f:
        pickle.dump(feature_columns, f)
    print("✅ Saved feature columns as feature_columns_corrected.pkl")
    
    print("\n🎯 Model is ready! Update content_api.py to use the new model.")

if __name__ == "__main__":
    save_model()
