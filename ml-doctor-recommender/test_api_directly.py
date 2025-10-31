#!/usr/bin/env python3
"""
Test the ML API directly to verify dental symptoms work
"""

import requests
import json

def test_ml_api():
    print("🧪 Testing ML API directly...")
    
    # Test cases
    test_cases = [
        {
            "name": "Dental symptoms with severity",
            "symptoms": {
                "toothache_severe": True,
                "toothache": True,
                "jaw_pain": True,
                "followupanswers": {"symptom_duration": "days"}
            },
            "expected_specialist": "Dentistry"
        },
        {
            "name": "Simple toothache",
            "symptoms": {
                "toothache": True,
                "followupanswers": {}
            },
            "expected_specialist": "Dentistry"
        },
        {
            "name": "Joint pain",
            "symptoms": {
                "joint_pain": True,
                "neck_pain": True,
                "followupanswers": {}
            },
            "expected_specialist": "Rheumatology"
        },
        {
            "name": "Eye symptoms",
            "symptoms": {
                "eye_pain": True,
                "vision_loss": True,
                "followupanswers": {}
            },
            "expected_specialist": "Ophthalmology"
        }
    ]
    
    api_url = "http://127.0.0.1:8001/predict"
    
    for test_case in test_cases:
        print(f"\n🔍 Testing: {test_case['name']}")
        print(f"Symptoms: {test_case['symptoms']}")
        
        try:
            response = requests.post(api_url, json=test_case['symptoms'], timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract key information
                predicted_specialist = result.get('predicted_specialist', 'Unknown')
                confidence = result.get('confidence', 0)
                suggested_diseases = result.get('suggested_diseases', [])
                
                print(f"✅ Response received")
                print(f"   Predicted specialist: {predicted_specialist}")
                print(f"   Confidence: {confidence:.3f}")
                print(f"   Top disease: {suggested_diseases[0] if suggested_diseases else 'None'}")
                
                # Check if prediction is correct
                if test_case['expected_specialist'].lower() in predicted_specialist.lower():
                    print(f"✅ CORRECT: Expected {test_case['expected_specialist']}, got {predicted_specialist}")
                else:
                    print(f"❌ WRONG: Expected {test_case['expected_specialist']}, got {predicted_specialist}")
                    
                # Check confidence
                if confidence > 0.8:
                    print(f"✅ HIGH CONFIDENCE: {confidence:.1%}")
                elif confidence > 0.5:
                    print(f"⚠️ MEDIUM CONFIDENCE: {confidence:.1%}")
                else:
                    print(f"❌ LOW CONFIDENCE: {confidence:.1%}")
                    
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ CONNECTION ERROR: ML API not running on {api_url}")
            print("   Start the ML API with: uvicorn content_api:app --host 127.0.0.1 --port 8001")
            break
        except requests.exceptions.Timeout:
            print(f"❌ TIMEOUT: ML API took too long to respond")
        except Exception as e:
            print(f"❌ ERROR: {e}")
    
    print(f"\n🎯 Test completed!")

if __name__ == "__main__":
    test_ml_api()
