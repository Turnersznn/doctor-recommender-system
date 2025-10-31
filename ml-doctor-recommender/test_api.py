import requests
import json

# Test the ML API
def test_ml_api():
    url = "http://127.0.0.1:8000/predict"
    
    test_symptoms = {
        "symptoms": {
            "chest_pain": True,
            "headache": True,
            "fatigue": True
        }
    }
    
    try:
        print("Testing ML API...")
        print(f"URL: {url}")
        print(f"Payload: {json.dumps(test_symptoms, indent=2)}")
        
        response = requests.post(url, json=test_symptoms, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ ML API is working!")
            print(f"Diagnoses found: {len(result.get('diagnoses', []))}")
            for i, diag in enumerate(result.get('diagnoses', [])[:3]):
                print(f"  {i+1}. {diag.get('disease')} - {diag.get('probability', 0)*100:.1f}% - {diag.get('specialist')}")
        else:
            print("❌ ML API returned error")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to ML API - make sure it's running on port 8000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_ml_api()
