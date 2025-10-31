#!/usr/bin/env python3
"""
Direct test of the multi-symptom mapper without starting the API server
"""

import sys
import os
sys.path.append('ml-doctor-recommender')

# Change to current directory and import
os.chdir('ml-doctor-recommender')
from multi_symptom_mapper import get_multi_symptom_recommendations
from content_api import disease_to_specialist_mapping

def test_multi_symptom_direct():
    print("Testing Multi-Symptom Mapper Directly")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Respiratory Symptoms",
            "symptoms": ["cough", "fever", "shortness_of_breath"]
        },
        {
            "name": "Cardiac Symptoms", 
            "symptoms": ["chest_pain", "shortness_of_breath", "fatigue"]
        },
        {
            "name": "Neurological Symptoms",
            "symptoms": ["headache", "sensitivity_to_light", "nausea"]
        },
        {
            "name": "GI Symptoms",
            "symptoms": ["stomach_pain", "nausea", "vomiting"]
        },
        {
            "name": "Joint Symptoms",
            "symptoms": ["joint_pain", "swelling_joints", "stiffness"]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case['name']}")
        print(f"Symptoms: {test_case['symptoms']}")
        print("-" * 40)
        
        try:
            results = get_multi_symptom_recommendations(
                test_case['symptoms'], 
                disease_to_specialist_mapping
            )
            
            if results:
                print(f"✅ Found {len(results)} recommendations:")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. Disease: {result['disease']}")
                    print(f"     Specialist: {result['specialist']}")
                    print(f"     Confidence: {result['confidence']:.2f}")
                    print(f"     Matching symptoms: {result['matching_symptoms']}")
                    if i < len(results):
                        print()
            else:
                print("❌ No recommendations found")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_multi_symptom_direct()
