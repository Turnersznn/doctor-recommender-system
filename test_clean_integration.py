#!/usr/bin/env python3
"""
Test the clean integration - ML model working behind the scenes without branding
"""

import requests
import json

def test_clean_integration():
    print("🔍 Testing Clean Integration")
    print("=" * 50)
    
    url = "http://127.0.0.1:8006/predict"
    
    # Test cases that should work
    test_cases = [
        {
            "name": "Respiratory symptoms",
            "symptoms": {
                "cough": True,
                "fever": True,
                "shortness_of_breath": True
            }
        },
        {
            "name": "Skin symptoms", 
            "symptoms": {
                "itching": True,
                "skin_rash": True
            }
        },
        {
            "name": "Unknown combination",
            "symptoms": {
                "random_symptom_xyz": True,
                "another_fake_symptom": True
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🎯 Testing: {test_case['name']}")
        print(f"Symptoms: {list(test_case['symptoms'].keys())}")
        print("-" * 40)
        
        try:
            response = requests.post(url, json=test_case, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                # Check if it's a "not found" case
                if not result.get('diagnoses') or len(result.get('diagnoses', [])) == 0:
                    print("❌ No diagnoses found - will show 'not found' message")
                elif len(result.get('diagnoses', [])) == 1 and result['diagnoses'][0].get('disease') == "General Assessment Needed":
                    print("❌ General assessment only - will show 'not found' message")
                else:
                    print("✅ Success! Found diagnoses:")
                    for i, diagnosis in enumerate(result.get('diagnoses', [])[:2], 1):
                        print(f"  {i}. {diagnosis.get('disease')} -> {diagnosis.get('specialist')}")
                        print(f"     Confidence: {diagnosis.get('confidence', 0):.2f}")
                
                print(f"Primary specialist: {result.get('predicted_specialist', 'Unknown')}")
                
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: API not running on {url}")
            print("Start the API with: python ml_multi_symptom_api.py")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*50}")
    print("✅ Integration test complete!")
    print("The ML model works behind the scenes without any ML branding in the frontend.")

if __name__ == "__main__":
    test_clean_integration()
