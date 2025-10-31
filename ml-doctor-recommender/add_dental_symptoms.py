#!/usr/bin/env python3
"""
Add dental/tooth symptoms to the ML model
"""

import pandas as pd
import numpy as np
import joblib
import pickle

def add_dental_symptoms_to_model():
    print("🦷 Adding dental symptoms to ML model...")
    
    # Load existing model and features
    try:
        model = joblib.load('content_model_HIGH_ACCURACY.pkl')
        with open('feature_columns_HIGH_ACCURACY.pkl', 'rb') as f:
            existing_features = pickle.load(f)
        print(f"✅ Loaded existing model with {len(existing_features)} features")
    except Exception as e:
        print(f"❌ Error loading existing model: {e}")
        return
    
    # Define dental symptoms and their specialist mappings
    DENTAL_SYMPTOMS = {
        # Basic dental symptoms
        'tooth_pain': 'Dentist',
        'toothache': 'Dentist',
        'tooth_sensitivity': 'Dentist',
        'dental_pain': 'Dentist',
        'gum_pain': 'Dentist',
        'jaw_pain': 'Dentist',
        
        # Gum-related symptoms
        'bleeding_gums': 'Dentist',
        'swollen_gums': 'Dentist',
        'gum_swelling': 'Dentist',
        'gum_bleeding': 'Dentist',
        'gum_inflammation': 'Dentist',
        
        # Oral health symptoms
        'bad_breath': 'Dentist',
        'mouth_sores': 'Dentist',
        'oral_pain': 'Dentist',
        'mouth_pain': 'Dentist',
        'tongue_pain': 'Dentist',
        'lip_pain': 'Dentist',
        
        # Dental structure issues
        'broken_tooth': 'Dentist',
        'chipped_tooth': 'Dentist',
        'loose_tooth': 'Dentist',
        'missing_tooth': 'Dentist',
        'crooked_teeth': 'Orthodontist',
        
        # Advanced dental issues
        'wisdom_tooth_pain': 'Oral Surgeon',
        'jaw_clicking': 'Oral Surgeon',
        'jaw_locking': 'Oral Surgeon',
        'tmj_pain': 'Oral Surgeon',
        
        # Orthodontic symptoms
        'teeth_alignment': 'Orthodontist',
        'bite_problems': 'Orthodontist',
        'overbite': 'Orthodontist',
        'underbite': 'Orthodontist'
    }
    
    # Add dental symptoms to existing features
    all_features = list(existing_features) + list(DENTAL_SYMPTOMS.keys())
    all_features = sorted(list(set(all_features)))  # Remove duplicates and sort
    
    print(f"📝 Added {len(DENTAL_SYMPTOMS)} dental symptoms")
    print(f"📝 Total features now: {len(all_features)}")
    
    # Create training data with dental symptoms
    print("🏗️ Creating training data with dental symptoms...")
    
    # Load existing training data structure
    original_df = pd.read_csv('Original_Dataset.csv', encoding='latin-1')
    doctor_disease_df = pd.read_csv('Doctor_Versus_Disease.csv', names=['Disease', 'Specialist'], encoding='latin-1')
    
    # Create comprehensive training data
    training_data = []
    
    # 1. Add existing medical symptoms (high weight)
    EXISTING_SYMPTOM_PRIORITY = {
        # Joint/Bone symptoms
        'joint_pain': 'Rheumatologists',
        'muscle_pain': 'Rheumatologists', 
        'back_pain': 'Rheumatologists',
        'neck_pain': 'Rheumatologists',
        'stiffness': 'Rheumatologists',
        
        # Respiratory symptoms
        'cough': 'Pulmonologist',
        'shortness_of_breath': 'Pulmonologist',
        'breathing_difficulty': 'Pulmonologist',
        'chest_congestion': 'Pulmonologist',
        'wheezing': 'Pulmonologist',
        
        # Heart symptoms
        'chest_pain': 'Cardiologist',
        'heart_palpitations': 'Cardiologist',
        'irregular_heartbeat': 'Cardiologist',
        'chest_tightness': 'Cardiologist',
        
        # Mental health
        'depression': 'Psychiatrist',
        'anxiety': 'Psychiatrist',
        'mood_swings': 'Psychiatrist',
        'panic_attacks': 'Psychiatrist',
        'insomnia': 'Psychiatrist',
        
        # Skin symptoms
        'skin_rash': 'Dermatologist',
        'itching': 'Dermatologist',
        'acne': 'Dermatologist',
        'rash': 'Dermatologist',
        
        # Digestive symptoms
        'abdominal_pain': 'Gastroenterologist',
        'nausea': 'Gastroenterologist',
        'vomiting': 'Gastroenterologist',
        'diarrhea': 'Gastroenterologist',
        'stomach_pain': 'Gastroenterologist',
        
        # Neurological symptoms
        'headache': 'Neurologist',
        'dizziness': 'Neurologist',
        'seizures': 'Neurologist',
        'memory_loss': 'Neurologist',
        'confusion': 'Neurologist',
        
        # ENT symptoms
        'sore_throat': 'Otolaryngologist',
        'ear_pain': 'Otolaryngologist',
        'hearing_loss': 'Otolaryngologist',
        'nasal_congestion': 'Otolaryngologist',
        'throat_irritation': 'Otolaryngologist',
        'runny_nose': 'Otolaryngologist',
        
        # General symptoms
        'fever': 'Internal Medcine',
        'fatigue': 'Internal Medcine',
        'weakness': 'Internal Medcine',
        'weight_loss': 'Internal Medcine'
    }
    
    # Combine existing and dental symptoms
    ALL_SYMPTOM_PRIORITY = {**EXISTING_SYMPTOM_PRIORITY, **DENTAL_SYMPTOMS}
    
    # Add priority symptom mappings with VERY HIGH weight
    for symptom, specialist in ALL_SYMPTOM_PRIORITY.items():
        for _ in range(200):  # Very high weight
            feature_vector = {s: 0 for s in all_features}
            feature_vector[symptom] = 1
            feature_vector['specialist'] = specialist
            training_data.append(feature_vector)
    
    # Add original dataset mappings (lower weight)
    for _, row in original_df.iterrows():
        disease = row['Disease']
        
        # Get specialist for this disease
        specialist_row = doctor_disease_df[doctor_disease_df['Disease'] == disease]
        if specialist_row.empty:
            continue
            
        specialist = specialist_row.iloc[0]['Specialist']
        
        # Create feature vector
        feature_vector = {symptom: 0 for symptom in all_features}
        
        # Set symptoms to 1
        for col in original_df.columns[1:]:
            if pd.notna(row[col]) and str(row[col]).strip():
                symptom = str(row[col]).strip().lower().replace(' ', '_')
                if symptom in feature_vector:
                    feature_vector[symptom] = 1
        
        feature_vector['specialist'] = specialist
        training_data.append(feature_vector)
    
    # Add multi-symptom combinations for dental
    dental_combinations = [
        (['tooth_pain', 'gum_swelling'], 'Dentist'),
        (['toothache', 'jaw_pain'], 'Dentist'),
        (['bleeding_gums', 'bad_breath'], 'Dentist'),
        (['wisdom_tooth_pain', 'jaw_clicking'], 'Oral Surgeon'),
        (['crooked_teeth', 'bite_problems'], 'Orthodontist'),
        (['broken_tooth', 'dental_pain'], 'Dentist')
    ]
    
    for symptoms, specialist in dental_combinations:
        for _ in range(50):  # 50 combinations each
            feature_vector = {s: 0 for s in all_features}
            for symptom in symptoms:
                if symptom in feature_vector:
                    feature_vector[symptom] = 1
            feature_vector['specialist'] = specialist
            training_data.append(feature_vector)
    
    # Convert to DataFrame and train model
    training_df = pd.DataFrame(training_data)
    
    print(f"✅ Created {len(training_df)} training samples")
    print(f"✅ Specialists: {training_df['specialist'].unique()}")
    
    # Train new model
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    
    X = training_df[all_features]
    y = training_df['specialist']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = GradientBoostingClassifier(
        n_estimators=300,
        learning_rate=0.1,
        max_depth=8,
        min_samples_split=10,
        min_samples_leaf=4,
        random_state=42
    )
    
    print("🤖 Training model with dental symptoms...")
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = (y_pred == y_test).mean()
    
    print(f"✅ Model trained with accuracy: {accuracy:.3f}")
    
    # Test dental symptoms
    print(f"\n🦷 Testing dental symptoms:")
    
    dental_test_cases = [
        ('tooth_pain', 'Dentist'),
        ('toothache', 'Dentist'),
        ('bleeding_gums', 'Dentist'),
        ('jaw_pain', 'Dentist'),
        ('wisdom_tooth_pain', 'Oral Surgeon'),
        ('crooked_teeth', 'Orthodontist'),
        ('bad_breath', 'Dentist'),
        ('broken_tooth', 'Dentist')
    ]
    
    correct = 0
    total = 0
    
    for symptom, expected in dental_test_cases:
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
            confidence_level = "HIGH" if probability > 0.7 else "MED" if probability > 0.5 else "LOW"
            print(f"{status} {symptom:<20} -> {prediction:<15} ({probability:.3f} {confidence_level}) [expected: {expected}]")
    
    dental_accuracy = correct / total if total > 0 else 0
    print(f"\n🦷 Dental Symptom Accuracy: {correct}/{total} = {dental_accuracy:.1%}")
    
    # Save updated model
    joblib.dump(model, 'content_model_WITH_DENTAL.pkl')
    with open('feature_columns_WITH_DENTAL.pkl', 'wb') as f:
        pickle.dump(all_features, f)
    
    print(f"\n💾 Saved model with dental symptoms as content_model_WITH_DENTAL.pkl")
    print(f"💾 Saved features as feature_columns_WITH_DENTAL.pkl")
    
    if dental_accuracy >= 0.9:
        print("🎉 EXCELLENT! Dental symptoms working perfectly!")
    else:
        print("⚠️ Dental symptoms need more work...")

if __name__ == "__main__":
    add_dental_symptoms_to_model()
