#!/usr/bin/env python3
"""
Fix the ML model completely with proper symptom prioritization
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import pickle

def create_fixed_model():
    print("🔧 Creating completely fixed ML model...")
    
    # Load existing data
    original_df = pd.read_csv('Original_Dataset.csv', encoding='latin-1')
    doctor_disease_df = pd.read_csv('Doctor_Versus_Disease.csv', names=['Disease', 'Specialist'], encoding='latin-1')
    
    # Create symptom-specialist priority mapping
    SYMPTOM_PRIORITY = {
        # Joint/Bone symptoms - ALWAYS Rheumatology first
        'joint_pain': 'Rheumatologists',
        'muscle_pain': 'Rheumatologists', 
        'back_pain': 'Rheumatologists',
        'neck_pain': 'Rheumatologists',
        'stiffness': 'Rheumatologists',
        
        # Respiratory symptoms - ALWAYS Pulmonology
        'cough': 'Pulmonologist',
        'shortness_of_breath': 'Pulmonologist',
        'breathing_difficulty': 'Pulmonologist',
        'chest_congestion': 'Pulmonologist',
        
        # Heart symptoms - ALWAYS Cardiology
        'chest_pain': 'Cardiologist',
        'heart_palpitations': 'Cardiologist',
        'irregular_heartbeat': 'Cardiologist',
        
        # Mental health - ALWAYS Psychiatry
        'depression': 'Psychiatrist',
        'anxiety': 'Psychiatrist',
        'mood_swings': 'Psychiatrist',
        'panic_attacks': 'Psychiatrist',
        
        # Skin symptoms - ALWAYS Dermatology
        'skin_rash': 'Dermatologist',
        'itching': 'Dermatologist',
        'acne': 'Dermatologist',
        
        # Digestive symptoms - Gastroenterology
        'abdominal_pain': 'Gastroenterologist',
        'nausea': 'Gastroenterologist',
        'vomiting': 'Gastroenterologist',
        'diarrhea': 'Gastroenterologist',
        
        # Neurological symptoms
        'headache': 'Neurologist',
        'dizziness': 'Neurologist',
        'seizures': 'Neurologist',
        'memory_loss': 'Neurologist'
    }
    
    # Get all symptoms from dataset
    all_symptoms = set()
    for _, row in original_df.iterrows():
        for col in original_df.columns[1:]:
            if pd.notna(row[col]) and str(row[col]).strip():
                symptom = str(row[col]).strip().lower().replace(' ', '_')
                all_symptoms.add(symptom)
    
    all_symptoms = sorted(list(all_symptoms))
    print(f"📝 Found {len(all_symptoms)} unique symptoms")
    
    # Create training data with priority overrides
    training_data = []
    
    # First, add priority symptom mappings (high weight)
    for symptom, specialist in SYMPTOM_PRIORITY.items():
        if symptom in all_symptoms:
            for _ in range(100):  # High weight for priority mappings
                feature_vector = {s: 0 for s in all_symptoms}
                feature_vector[symptom] = 1
                feature_vector['specialist'] = specialist
                training_data.append(feature_vector)
    
    # Then add original dataset mappings (lower weight)
    for _, row in original_df.iterrows():
        disease = row['Disease']
        
        # Get specialist for this disease
        specialist_row = doctor_disease_df[doctor_disease_df['Disease'] == disease]
        if specialist_row.empty:
            continue
            
        specialist = specialist_row.iloc[0]['Specialist']
        
        # Create feature vector
        feature_vector = {symptom: 0 for symptom in all_symptoms}
        
        # Set symptoms to 1
        for col in original_df.columns[1:]:
            if pd.notna(row[col]) and str(row[col]).strip():
                symptom = str(row[col]).strip().lower().replace(' ', '_')
                if symptom in feature_vector:
                    feature_vector[symptom] = 1
        
        feature_vector['specialist'] = specialist
        training_data.append(feature_vector)
    
    # Convert to DataFrame
    training_df = pd.DataFrame(training_data)
    
    print(f"✅ Created {len(training_df)} training samples")
    print(f"✅ Specialists: {training_df['specialist'].unique()}")
    
    # Train model
    X = training_df[all_symptoms]
    y = training_df['specialist']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = (y_pred == y_test).mean()
    
    print(f"\n✅ Model trained with accuracy: {accuracy:.3f}")
    
    # Test critical cases
    print(f"\n🧪 Testing critical cases:")
    
    test_cases = [
        ('joint_pain', 'Rheumatologists'),
        ('cough', 'Pulmonologist'), 
        ('chest_pain', 'Cardiologist'),
        ('depression', 'Psychiatrist'),
        ('skin_rash', 'Dermatologist'),
        ('headache', 'Neurologist'),
        ('abdominal_pain', 'Gastroenterologist')
    ]
    
    for symptom, expected in test_cases:
        if symptom in all_symptoms:
            test_input = pd.DataFrame([[0] * len(all_symptoms)], columns=all_symptoms)
            test_input[symptom] = 1
            prediction = model.predict(test_input)[0]
            probability = model.predict_proba(test_input)[0].max()
            
            status = "✅" if prediction == expected else "❌"
            print(f"{status} {symptom} -> {prediction} (confidence: {probability:.3f}) [expected: {expected}]")
    
    # Save model
    joblib.dump(model, 'content_model_FIXED.pkl')
    with open('feature_columns_FIXED.pkl', 'wb') as f:
        pickle.dump(all_symptoms, f)
    
    print(f"\n💾 Saved FIXED model as content_model_FIXED.pkl")
    print(f"💾 Saved FIXED features as feature_columns_FIXED.pkl")

if __name__ == "__main__":
    create_fixed_model()
