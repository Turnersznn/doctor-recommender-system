#!/usr/bin/env python3
"""
Test the ML Multi-Symptom Model directly
"""

import joblib
import pickle
import pandas as pd
import numpy as np

def test_ml_model():
    print("🔍 Testing ML Multi-Symptom Model")
    print("=" * 50)
    
    try:
        # Load models
        print("🔄 Loading ML models...")
        disease_model = joblib.load('multi_symptom_disease_model.pkl')
        specialist_model = joblib.load('multi_symptom_specialist_model.pkl')
        
        with open('multi_symptom_features.pkl', 'rb') as f:
            feature_columns = pickle.load(f)
            
        print(f"✅ Disease model loaded: {len(disease_model.classes_)} diseases")
        print(f"✅ Specialist model loaded: {len(specialist_model.classes_)} specialists")
        print(f"✅ Feature columns loaded: {len(feature_columns)}")
        
        # Test cases
        test_cases = [
            {
                "name": "Skin Issues",
                "symptoms": ["itching", "skin_rash"]
            },
            {
                "name": "Respiratory Issues", 
                "symptoms": ["cough", "breathlessness"]
            },
            {
                "name": "Heart Issues",
                "symptoms": ["chest_pain", "palpitations"]
            },
            {
                "name": "Digestive Issues",
                "symptoms": ["nausea", "vomiting", "abdominal_pain"]
            }
        ]
        
        for test_case in test_cases:
            print(f"\n🎯 Testing: {test_case['name']}")
            print(f"Symptoms: {test_case['symptoms']}")
            print("-" * 40)
            
            # Prepare input
            input_data = pd.DataFrame([[0] * len(feature_columns)], columns=feature_columns)
            
            for symptom in test_case['symptoms']:
                clean_symptom = symptom.lower().replace(' ', '_').replace(',', '').strip()
                if clean_symptom in feature_columns:
                    input_data[clean_symptom] = 1
                    print(f"✅ Mapped: {symptom} -> {clean_symptom}")
                else:
                    print(f"⚠️ Not found: {symptom}")
            
            # Get predictions
            disease_probs = disease_model.predict_proba(input_data)[0]
            disease_classes = disease_model.classes_
            
            specialist_probs = specialist_model.predict_proba(input_data)[0]
            specialist_classes = specialist_model.classes_
            
            # Top disease predictions
            top_disease_indices = disease_probs.argsort()[-3:][::-1]
            print("\n🏥 Top Disease Predictions:")
            for i, idx in enumerate(top_disease_indices, 1):
                if disease_probs[idx] > 0.01:
                    print(f"  {i}. {disease_classes[idx]}: {disease_probs[idx]:.3f}")
            
            # Top specialist predictions
            top_specialist_indices = specialist_probs.argsort()[-3:][::-1]
            print("\n👨‍⚕️ Top Specialist Predictions:")
            for i, idx in enumerate(top_specialist_indices, 1):
                if specialist_probs[idx] > 0.01:
                    print(f"  {i}. {specialist_classes[idx]}: {specialist_probs[idx]:.3f}")
        
        print("\n🎉 ML Model Test Complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing ML model: {e}")
        return False

if __name__ == "__main__":
    test_ml_model()
