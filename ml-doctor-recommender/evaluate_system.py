import requests
import json
from sklearn.metrics import precision_score, recall_score, accuracy_score, classification_report

# Realistic test cases with challenging scenarios
TEST_CASES = [
    # Perfect matches (should work)
    {"symptoms": {"fever": True, "chills": True, "headache": True, "muscle_aches": True}, "expected": "Malaria"},
    {"symptoms": {"diarrhoea": True, "vomiting": True, "dehydration": True}, "expected": "Cholera"},
    
    # Ambiguous cases (fever could be many things)
    {"symptoms": {"fever": True, "headache": True}, "expected": "Malaria"},  # Could be many diseases
    {"symptoms": {"cough": True, "fever": True}, "expected": "Common Cold"},  # Could be pneumonia
    {"symptoms": {"chest_pain": True}, "expected": "Heart Condition"},  # Very vague
    
    # Incomplete symptom sets
    {"symptoms": {"joint_pain": True}, "expected": "Joint Inflammation"},  # Missing swelling
    {"symptoms": {"headache": True}, "expected": "Head Pain"},  # Very generic
    {"symptoms": {"eye_pain": True}, "expected": "Eye Strain"},  # Missing other symptoms
    
    # Overlapping symptoms (could match multiple diseases)
    {"symptoms": {"nausea": True, "vomiting": True}, "expected": "Stomach Upset"},  # Could be many GI issues
    {"symptoms": {"skin_rash": True, "itching": True}, "expected": "Skin Irritation"},  # Could be eczema
    
    # Edge cases with uncommon combinations
    {"symptoms": {"fatigue": True, "weight_loss": True}, "expected": None},  # No clear mapping
    {"symptoms": {"dizziness": True, "anxiety": True}, "expected": None},  # Unclear
    
    # Mixed symptoms from different systems
    {"symptoms": {"chest_pain": True, "headache": True, "nausea": True}, "expected": None},  # Confusing mix
    {"symptoms": {"fever": True, "joint_pain": True, "skin_rash": True}, "expected": "Dengue Fever"},  # Should work
    
    # Single symptom cases (should be challenging)
    {"symptoms": {"toothache": True}, "expected": None},  # Too vague
    {"symptoms": {"back_pain": True}, "expected": "Back Strain"},  # Generic
    
    # British vs American spelling issues
    {"symptoms": {"diarrhoea": True, "fever": True}, "expected": "Typhoid Fever"},  # Should handle spelling
    
    # Complex multi-system cases
    {"symptoms": {"fever": True, "cough": True, "chest_pain": True, "fatigue": True}, "expected": "Pneumonia"},  # Multiple matches possible
]

def get_prediction(symptoms):
    """Get prediction from ML API"""
    try:
        response = requests.post('http://127.0.0.1:8002/predict', 
                               json={"symptoms": symptoms}, 
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('diagnoses') and len(data['diagnoses']) > 0:
                return data['diagnoses'][0]['disease']
        return None
    except Exception as e:
        print(f"Error getting prediction: {e}")
        return None

def evaluate_system():
    """Evaluate the system performance"""
    y_true = []
    y_pred = []
    
    print("Evaluating system performance...")
    print("-" * 50)
    
    for i, test_case in enumerate(TEST_CASES):
        symptoms = test_case["symptoms"]
        expected = test_case["expected"]
        
        prediction = get_prediction(symptoms)
        
        y_true.append(expected if expected else "Unknown")
        y_pred.append(prediction if prediction else "Unknown")
        
        status = "PASS" if prediction == expected else "FAIL"
        expected_str = expected or 'None'
        prediction_str = prediction or 'None'
        print(f"{i+1:2d}. {status} Expected: {expected_str:20} | Got: {prediction_str:20}")
    
    print("-" * 50)
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    
    # For precision and recall, we need to handle multi-class
    unique_labels = list(set(y_true + y_pred))
    precision = precision_score(y_true, y_pred, labels=unique_labels, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, labels=unique_labels, average='weighted', zero_division=0)
    
    print(f"RESULTS:")
    print(f"Accuracy:  {accuracy:.3f} ({accuracy*100:.1f}%)")
    print(f"Precision: {precision:.3f} ({precision*100:.1f}%)")
    print(f"Recall:    {recall:.3f} ({recall*100:.1f}%)")
    
    # Detailed classification report
    print("\nDetailed Classification Report:")
    print(classification_report(y_true, y_pred, zero_division=0))
    
    return accuracy, precision, recall

if __name__ == "__main__":
    evaluate_system()