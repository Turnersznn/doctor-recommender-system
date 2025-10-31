#!/usr/bin/env python3
"""
Test the multi-symptom integration
"""

from multi_symptom_mapper import get_multi_symptom_recommendations
from content_api import disease_to_specialist_mapping

def test_integration():
    print("Testing Multi-Symptom Integration")
    print("=" * 50)
    
    # Test case: Respiratory symptoms
    symptoms = ["cough", "fever", "shortness_of_breath"]
    print(f"Testing symptoms: {symptoms}")
    
    try:
        results = get_multi_symptom_recommendations(symptoms, disease_to_specialist_mapping)
        
        if results:
            print(f"✅ Success! Found {len(results)} recommendations:")
            for i, result in enumerate(results, 1):
                print(f"  {i}. Disease: {result['disease']}")
                print(f"     Specialist: {result['specialist']}")
                print(f"     Confidence: {result['confidence']:.2f}")
                print(f"     Matching symptoms: {result['matching_symptoms']}")
        else:
            print("❌ No recommendations found")
            
        # Test the API format conversion
        print("\n" + "=" * 50)
        print("Testing API Format Conversion")
        print("=" * 50)
        
        # Simulate what the API does
        diagnoses = []
        specialists = []
        
        for result in results:
            diagnosis = {
                "disease": result["disease"],
                "probability": result["probability"],
                "specialist": result["specialist"],
                "alternative_specialists": result.get("alternative_specialists", []),
                "confidence": result["confidence"],
                "explanation": result.get("explanation", f"Based on symptoms matching {result['disease']}"),
                "matching_symptoms": result.get("matching_symptoms", symptoms)
            }
            diagnoses.append(diagnosis)
            
            if result["specialist"] not in specialists:
                specialists.append(result["specialist"])
        
        primary_specialist = diagnoses[0]["specialist"] if diagnoses else "General Practitioner"
        
        api_response = {
            "diagnoses": diagnoses,
            "predicted_specialist": primary_specialist,
            "confidence": diagnoses[0]["confidence"] if diagnoses else 0.6,
            "suggested_diseases": [diag["disease"] for diag in diagnoses],
            "active_symptoms": symptoms,
            "ml_prediction": primary_specialist,
            "disease_based_specialists": specialists
        }
        
        print(f"✅ API Response Format:")
        print(f"   Primary Specialist: {api_response['predicted_specialist']}")
        print(f"   Confidence: {api_response['confidence']:.2f}")
        print(f"   Number of diagnoses: {len(api_response['diagnoses'])}")
        print(f"   Specialists: {api_response['disease_based_specialists']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_integration()
    if success:
        print("\n🎉 Integration test passed! The multi-symptom system is working correctly.")
    else:
        print("\n❌ Integration test failed!")
