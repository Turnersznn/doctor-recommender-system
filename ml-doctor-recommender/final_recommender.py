import pandas as pd
import numpy as np
import json
from typing import List, Dict, Optional

class DoctorRecommender:
    """
    Enhanced Doctor Recommender System with:
    - Dynamic confidence thresholds
    - Expanded specialist mappings
    - Improved output formatting
    """
    
    def __init__(self, data_path: str = 'Specialist.xlsx'):
        self.data_path = data_path
        self.main_data = None
        self.symptom_columns = None
        self.specialists = None
        self.symptom_to_column_map = {}
        self.BASE_CONFIDENCE = 30  # Base minimum confidence percentage
        self.MIN_FALLBACK_CONFIDENCE = 20  # Minimum for cases with few matches
        
        # Enhanced symptom standardization
        self.symptom_mapping = {
            "fever": "high_fever",
            "stomachache": "stomach_pain",
            "throw up": "vomiting",
            "throwup": "vomiting",
            "belly pain": "stomach_pain",
            "bp": "blood_pressure",
            "heartburn": "acid_reflux"
        }
        
        self._load_data()
        self._prepare_data()
    
    def _load_data(self):
        """Load and clean the dataset"""
        print("Loading data...")
        self.main_data = pd.read_excel(self.data_path)
        
        if 'Unnamed: 0' in self.main_data.columns:
            self.main_data = self.main_data.drop('Unnamed: 0', axis=1)
        
        self.target_column = self.main_data.columns[-1]
        self.symptom_columns = self.main_data.columns[:-1]
        print(f"✓ Loaded {len(self.main_data)} records with {len(self.symptom_columns)} symptoms")
    
    def _clean_specialist_name(self, specialist: str) -> str:
        """Enhanced specialist name standardization"""
        specialist = str(specialist).strip()
        
        specialist_mapping = {
            "Dermatologists": "Dermatologist",
            "Cardiologist ": "Cardiologist",
            "Internal Medcine": "Internal Medicine",
            "Common Cold": "General Practitioner",
            "Osteoarthristis": "Rheumatologist",
            "Rheumatologists": "Rheumatologist",
            "Pulmonology": "Pulmonologist",
            "Gastro": "Gastroenterologist",
            "Orthopedist": "Rheumatologist",  # New mapping
            "Arthritis Specialist": "Rheumatologist",
            "ENT": "Otolaryngologist",
            "General Doctor": "General Practitioner"
        }
        
        return specialist_mapping.get(specialist, specialist)
    
    def _prepare_data(self):
        """Prepare data for recommendations"""
        self.main_data[self.target_column] = self.main_data[self.target_column].apply(
            self._clean_specialist_name
        )
        
        self.specialists = self.main_data[self.target_column].unique()
        
        for col in self.symptom_columns:
            clean_name = col.strip().lower().replace(' ', '_')
            self.symptom_to_column_map[clean_name] = col
            no_underscore = clean_name.replace('_', '')
            self.symptom_to_column_map[no_underscore] = col
        
        print(f"✓ Prepared data with {len(self.specialists)} specialist types")
    
    def _standardize_symptom(self, symptom: str) -> str:
        """Standardize symptom input with enhanced mappings"""
        symptom = symptom.strip().lower()
        return self.symptom_mapping.get(symptom, symptom)
    
    def _match_symptoms(self, user_symptoms: List[str]) -> List[str]:
        """Robust symptom matching with improved partial matching"""
        matched_symptoms = []
        
        for symptom in user_symptoms:
            clean_symptom = self._standardize_symptom(symptom)
            clean_symptom = clean_symptom.replace(' ', '_')
            
            # Exact match check
            if clean_symptom in self.symptom_to_column_map:
                matched_symptoms.append(self.symptom_to_column_map[clean_symptom])
                continue
            
            # Enhanced partial matching
            best_match = None
            best_score = 0
            
            for db_symptom, db_column in self.symptom_to_column_map.items():
                if clean_symptom in db_symptom or db_symptom in clean_symptom:
                    score = len(set(clean_symptom) & set(db_symptom)) / len(set(clean_symptom) | set(db_symptom))
                    if score > best_score:
                        best_score = score
                        best_match = db_column
            
            if best_match and best_score > 0.4:  # Slightly more lenient threshold
                matched_symptoms.append(best_match)
        
        return list(set(matched_symptoms))
    
    def _calculate_similarity(self, user_vector: np.ndarray, case_vector: np.ndarray) -> float:
        """Enhanced similarity calculation"""
        intersection = np.sum(user_vector * case_vector)
        union = np.sum((user_vector + case_vector) > 0)
        jaccard = intersection / union if union > 0 else 0
        
        dot_product = np.dot(user_vector, case_vector)
        norm_user = np.linalg.norm(user_vector)
        norm_case = np.linalg.norm(case_vector)
        cosine = dot_product / (norm_user * norm_case) if (norm_user * norm_case) > 0 else 0
        
        simple_match = intersection / np.sum(user_vector) if np.sum(user_vector) > 0 else 0
        
        # Weighted combination favoring simple match
        return jaccard * 0.2 + cosine * 0.2 + simple_match * 0.6
    
    def recommend(self, symptoms: List[str], top_n: int = 5) -> Dict:
        """Enhanced recommendation with dynamic confidence"""
        if not symptoms:
            return {"error": "No symptoms provided"}
        
        matched_symptoms = self._match_symptoms(symptoms)
        
        if not matched_symptoms:
            return {
                "error": "No matching symptoms found",
                "available_symptoms": list(self.symptom_to_column_map.keys())[:20]
            }
        
        # Create symptom vector
        user_vector = np.zeros(len(self.symptom_columns))
        for i, symptom in enumerate(self.symptom_columns):
            if symptom in matched_symptoms:
                user_vector[i] = 1
        
        # Calculate scores
        specialist_scores = {}
        for specialist in self.specialists:
            specialist_data = self.main_data[self.main_data[self.target_column] == specialist]
            
            similarities = []
            for _, row in specialist_data.iterrows():
                case_vector = np.array(row[self.symptom_columns])
                similarity = self._calculate_similarity(user_vector, case_vector)
                if similarity > 0:
                    similarities.append(similarity)
            
            if similarities:
                confidence = np.mean(similarities) * 100
                specialist_scores[specialist] = {
                    'confidence': confidence,
                    'matching_cases': len(similarities),
                    'total_cases': len(specialist_data),
                    'max_score': np.max(similarities)
                }
        
        # Dynamic confidence threshold
        if len(specialist_scores) < 3:
            threshold = max(self.MIN_FALLBACK_CONFIDENCE, 
                          self.BASE_CONFIDENCE - 10)
        else:
            threshold = self.BASE_CONFIDENCE
        
        # Filter and sort
        recommendations = []
        seen_specialists = set()
        
        for specialist, scores in sorted(
            specialist_scores.items(),
            key=lambda x: x[1]['confidence'],
            reverse=True
        ):
            if (scores['confidence'] >= threshold and 
                specialist not in seen_specialists):
                recommendations.append({
                    'specialist': specialist,
                    'confidence': round(scores['confidence'], 1),
                    'matching_cases': scores['matching_cases'],
                    'total_cases': scores['total_cases'],
                    'match_percentage': round((scores['matching_cases'] / scores['total_cases']) * 100, 1),
                    'max_similarity': round(scores['max_score'], 3),
                    'confidence_level': (
                        "High" if scores['confidence'] >= self.BASE_CONFIDENCE 
                        else "Moderate"
                    )
                })
                seen_specialists.add(specialist)
                if len(recommendations) >= top_n:
                    break
        
        return {
            'input_symptoms': symptoms,
            'matched_symptoms': [s.strip() for s in matched_symptoms],
            'total_active_symptoms': int(np.sum(user_vector)),
            'recommendations': recommendations,
            'status': 'success',
            'system_metrics': {
                'confidence_threshold': threshold,
                'total_specialists_considered': len(specialist_scores)
            }
        }
    
    def get_available_symptoms(self) -> List[str]:
        """Get list of available symptoms"""
        return [col.strip().replace('_', ' ') for col in self.symptom_columns]
    
    def get_specialist_info(self) -> Dict:
        """Get information about available specialists"""
        specialist_info = {}
        for specialist in self.specialists:
            count = (self.main_data[self.target_column] == specialist).sum()
            specialist_info[specialist] = {
                'count': count,
                'common_symptoms': list(
                    self.main_data[self.main_data[self.target_column] == specialist]
                    .iloc[:, :-1]
                    .sum()
                    .sort_values(ascending=False)
                    .head(3)
                    .index
                )
            }
        return specialist_info

def test_recommender():
    """Enhanced test function with better formatting"""
    print("=== TESTING DOCTOR RECOMMENDER SYSTEM ===")
    print(f"{'='*50}\n")
    
    recommender = DoctorRecommender()
    
    test_cases = [
        {
            'name': 'Skin Problems',
            'symptoms': ['itching', 'skin rash', 'red spots']
        },
        {
            'name': 'Heart Issues',
            'symptoms': ['chest pain', 'palpitations', 'breathlessness']
        },
        {
            'name': 'Digestive Problems',
            'symptoms': ['stomach pain', 'vomiting', 'nausea']
        },
        {
            'name': 'Joint Pain',
            'symptoms': ['joint pain', 'knee pain', 'stiffness']
        },
        {
            'name': 'Complex Case',
            'symptoms': ['fever', 'cough', 'fatigue', 'headache']
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_case['name']}")
        print(f"SYMPTOMS: {', '.join(test_case['symptoms'])}")
        print('-'*50)
        
        result = recommender.recommend(test_case['symptoms'])
        
        if result['status'] == 'success':
            print(f"✓ Matched {len(result['matched_symptoms'])} symptoms")
            print(f"✓ Found {len(result['recommendations'])} recommendations")
            print(f"System used confidence threshold: {result['system_metrics']['confidence_threshold']}%")
            
            for i, rec in enumerate(result['recommendations'], 1):
                stars = '★' * int(rec['confidence']/20)
                print(f"\n{i}. {rec['specialist']} {stars}")
                print(f"   Confidence: {rec['confidence']}% ({rec['confidence_level']})")
                print(f"   Experience: {rec['matching_cases']} similar cases")
                print(f"   Success Rate: {rec['match_percentage']}%")
        else:
            print(f"❌ Error: {result['error']}")
            if 'available_symptoms' in result:
                print("Similar symptoms in system:", 
                     ', '.join(result['available_symptoms'][:5]))

def recommend_doctor_api(symptoms: List[str]) -> str:
    """Enhanced API function with better error handling"""
    recommender = DoctorRecommender()
    try:
        result = recommender.recommend(symptoms)
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e),
            "available_symptoms": recommender.get_available_symptoms()[:10]
        }, indent=2)

if __name__ == "__main__":
    test_recommender()
    
    print("\n" + "="*60)
    print("API DEMONSTRATION")
    print("="*60)
    
    print("\nCase 1: Common cold symptoms")
    print(recommend_doctor_api(['fever', 'cough', 'sore throat']))
    
    print("\nCase 2: Joint issues")
    print(recommend_doctor_api(['joint pain', 'swelling', 'redness']))
    
    print("\nCase 3: Invalid symptoms")
    print(recommend_doctor_api(['not_a_real_symptom']))