import requests
import json

# Test the multi-symptom API
def test_multi_symptom_api():
    url = "http://127.0.0.1:8003/predict"
    
    # Test case 1: Respiratory symptoms
    test_symptoms_1 = {
        "symptoms": {
            "cough": True,
            "fever": True,
            "shortness_of_breath": True
        }
    }
    
    # Test case 2: Cardiac symptoms
    test_symptoms_2 = {
        "symptoms": {
            "chest_pain": True,
            "shortness_of_breath": True,
            "fatigue": True
        }
    }
    
    # Test case 3: Neurological symptoms
    test_symptoms_3 = {
        "symptoms": {
            "headache": True,
            "sensitivity_to_light": True,
            "nausea": True
        }
    }
    
    test_cases = [
        ("Respiratory symptoms", test_symptoms_1),
        ("Cardiac symptoms", test_symptoms_2),
        ("Neurological symptoms", test_symptoms_3)
    ]
    
    for test_name, test_data in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {test_name}")
        print(f"{'='*60}")
        print(f"Input: {test_data}")
        
        try:
            response = requests.post(url, json=test_data, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"Primary Specialist: {result.get('predicted_specialist')}")
                print(f"Confidence: {result.get('confidence')}")
                print(f"Number of diagnoses: {len(result.get('diagnoses', []))}")
                
                for i, diagnosis in enumerate(result.get('diagnoses', [])[:2], 1):
                    print(f"  {i}. {diagnosis.get('disease')} -> {diagnosis.get('specialist')} (confidence: {diagnosis.get('confidence'):.2f})")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: Could not connect to {url}")
            print("Make sure the multi-symptom API is running on port 8003")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_multi_symptom_api()
