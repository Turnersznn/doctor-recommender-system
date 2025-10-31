#!/usr/bin/env python3
"""
Test all symptoms to verify the model is working correctly
"""

import pandas as pd
import joblib
import pickle

def test_all_symptoms():
    print("🧪 Testing ALL symptoms to verify model correctness...")
    
    # Load the FIXED model
    try:
        model = joblib.load("content_model_FIXED.pkl")
        with open('feature_columns_FIXED.pkl', 'rb') as f:
            feature_columns = pickle.load(f)
        print(f"✅ Loaded FIXED model with {len(feature_columns)} features")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Test critical symptoms that should have obvious mappings
    critical_tests = [
        # Respiratory
        ('cough', 'Pulmonologist'),
        ('shortness_of_breath', 'Pulmonologist'),
        ('breathing_difficulty', 'Pulmonologist'),
        
        # Cardiovascular  
        ('chest_pain', 'Cardiologist'),
        ('heart_palpitations', 'Cardiologist'),
        
        # Joint/Musculoskeletal
        ('joint_pain', 'Rheumatologists'),
        ('muscle_pain', 'Rheumatologists'),
        ('back_pain', 'Rheumatologists'),
        
        # Mental Health
        ('depression', 'Psychiatrist'),
        ('anxiety', 'Psychiatrist'),
        ('mood_swings', 'Psychiatrist'),
        
        # Skin
        ('skin_rash', 'Dermatologist'),
        ('itching', 'Dermatologist'),
        ('acne', 'Dermatologist'),
        
        # Digestive
        ('abdominal_pain', 'Gastroenterologist'),
        ('nausea', 'Gastroenterologist'),
        ('vomiting', 'Gastroenterologist'),
        ('diarrhea', 'Gastroenterologist'),
        
        # Neurological
        ('headache', 'Neurologist'),
        ('dizziness', 'Neurologist'),
        ('seizures', 'Neurologist'),
        
        # General
        ('fever', 'Internal Medcine'),
        ('fatigue', 'Internal Medcine')
    ]
    
    print(f"\n🔍 Testing {len(critical_tests)} critical symptoms:")
    print("=" * 80)
    
    correct_predictions = 0
    total_predictions = 0
    
    for symptom, expected in critical_tests:
        if symptom in feature_columns:
            # Create test input
            test_input = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
            test_input[symptom] = 1
            
            # Get prediction
            prediction = model.predict(test_input)[0]
            probabilities = model.predict_proba(test_input)[0]
            confidence = probabilities.max()
            
            # Check if correct
            is_correct = prediction == expected
            if is_correct:
                correct_predictions += 1
            total_predictions += 1
            
            # Status indicator
            status = "✅" if is_correct else "❌"
            confidence_level = "HIGH" if confidence > 0.5 else "MED" if confidence > 0.3 else "LOW"
            
            print(f"{status} {symptom:<20} -> {prediction:<20} ({confidence:.3f} {confidence_level}) [expected: {expected}]")
            
            # Show top 3 predictions for failed cases
            if not is_correct:
                top_classes = model.classes_
                top_probs = probabilities
                top_indices = top_probs.argsort()[-3:][::-1]
                print(f"    Top 3: {[(top_classes[i], top_probs[i]) for i in top_indices]}")
        else:
            print(f"⚠️  {symptom:<20} -> NOT FOUND in feature columns")
    
    print("=" * 80)
    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
    print(f"📊 Overall Accuracy: {correct_predictions}/{total_predictions} = {accuracy:.1%}")
    
    if accuracy < 0.8:
        print("❌ Model accuracy is too low! Need to fix more symptoms.")
    elif accuracy < 0.9:
        print("⚠️  Model accuracy is okay but could be better.")
    else:
        print("✅ Model accuracy is excellent!")
    
    # Test some common symptom combinations
    print(f"\n🔍 Testing symptom combinations:")
    print("=" * 50)
    
    combinations = [
        (['cough', 'fever'], 'Should be Pulmonologist'),
        (['chest_pain', 'shortness_of_breath'], 'Should be Cardiologist'),
        (['joint_pain', 'muscle_pain'], 'Should be Rheumatologists'),
        (['headache', 'dizziness'], 'Should be Neurologist'),
        (['skin_rash', 'itching'], 'Should be Dermatologist'),
        (['depression', 'anxiety'], 'Should be Psychiatrist')
    ]
    
    for symptoms, expected_note in combinations:
        # Check if all symptoms exist
        if all(symptom in feature_columns for symptom in symptoms):
            test_input = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
            for symptom in symptoms:
                test_input[symptom] = 1
            
            prediction = model.predict(test_input)[0]
            confidence = model.predict_proba(test_input)[0].max()
            
            print(f"🔗 {' + '.join(symptoms)} -> {prediction} ({confidence:.3f}) [{expected_note}]")
    
    print(f"\n🎯 Model is ready for testing!" if accuracy >= 0.8 else "🚨 Model needs more fixes!")

if __name__ == "__main__":
    test_all_symptoms()
