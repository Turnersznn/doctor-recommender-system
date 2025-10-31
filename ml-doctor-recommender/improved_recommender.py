import pandas as pd
import numpy as np
from collections import Counter

print("=== IMPROVED DOCTOR RECOMMENDER SYSTEM ===\n")

# Load and clean data
print("Loading and cleaning data...")
main_data = pd.read_excel('Specialist.xlsx')
main_data = main_data.drop('Unnamed: 0', axis=1)

target_column = main_data.columns[-1]
symptom_columns = main_data.columns[:-1]

# Clean up specialist names (fix data quality issues)
def clean_specialist_name(specialist):
    """Clean and standardize specialist names"""
    # Remove common data issues
    specialist = str(specialist).strip()
    
    # Fix known issues in your data
    if specialist == "Dermatologists":
        return "Dermatologist"
    elif specialist == "Cardiologist ":  # with trailing space
        return "Cardiologist"
    elif specialist == "Internal Medcine":
        return "Internal Medicine"
    elif specialist == "Common Cold":
        return "General Practitioner"  # More appropriate
    elif specialist == "Osteoarthristis":
        return "Rheumatologist"  # More appropriate for arthritis
    else:
        return specialist

# Apply cleaning
main_data[target_column] = main_data[target_column].apply(clean_specialist_name)

print(f"✓ Cleaned data: {main_data.shape[0]} records with {len(symptom_columns)} symptoms")

# Show cleaned specialists
specialists = main_data[target_column].unique()
print(f"✓ Clean specialist list ({len(specialists)} types):")
for specialist in sorted(specialists):
    count = (main_data[target_column] == specialist).sum()
    print(f"  • {specialist}: {count} cases")

def recommend_doctor_improved(user_symptoms, top_n=5):
    """
    Improved recommendation function with better scoring
    """
    print(f"\n=== ANALYZING SYMPTOMS: {user_symptoms} ===")
    
    # Clean user symptoms (remove spaces, lowercase)
    clean_user_symptoms = []
    for symptom in user_symptoms:
        # Try to find matching symptom in our columns
        symptom_clean = symptom.lower().strip().replace(' ', '_')
        
        # Find best match in symptom columns
        best_match = None
        for col in symptom_columns:
            col_clean = col.lower().strip().replace(' ', '_')
            if symptom_clean in col_clean or col_clean in symptom_clean:
                best_match = col
                break
        
        if best_match:
            clean_user_symptoms.append(best_match)
        else:
            print(f"⚠️  Symptom '{symptom}' not found in database")
    
    if not clean_user_symptoms:
        print("❌ No matching symptoms found!")
        return None
    
    print(f"✓ Matched symptoms: {clean_user_symptoms}")
    
    # Create user vector
    user_vector = np.zeros(len(symptom_columns))
    for i, symptom in enumerate(symptom_columns):
        if symptom in clean_user_symptoms:
            user_vector[i] = 1
    
    print(f"✓ Active symptoms: {int(sum(user_vector))}/{len(symptom_columns)}")
    
    # Calculate recommendations using multiple scoring methods
    specialist_scores = {}
    
    for specialist in specialists:
        specialist_data = main_data[main_data[target_column] == specialist]
        
        scores = []
        matching_cases = 0
        
        for index, row in specialist_data.iterrows():
            case_vector = np.array(row[symptom_columns])
            
            # Method 1: Jaccard similarity (intersection/union)
            intersection = np.sum(user_vector * case_vector)
            union = np.sum((user_vector + case_vector) > 0)
            jaccard = intersection / union if union > 0 else 0
            
            # Method 2: Cosine similarity
            dot_product = np.dot(user_vector, case_vector)
            norm_user = np.linalg.norm(user_vector)
            norm_case = np.linalg.norm(case_vector)
            cosine = dot_product / (norm_user * norm_case) if (norm_user * norm_case) > 0 else 0
            
            # Method 3: Simple matching (percentage of user symptoms matched)
            simple_match = intersection / sum(user_vector) if sum(user_vector) > 0 else 0
            
            # Combined score (weighted average)
            combined_score = (jaccard * 0.3 + cosine * 0.3 + simple_match * 0.4)
            
            if combined_score > 0:
                scores.append(combined_score)
                matching_cases += 1
        
        if scores:
            avg_score = np.mean(scores)
            max_score = np.max(scores)
            specialist_scores[specialist] = {
                'avg_score': avg_score,
                'max_score': max_score,
                'matching_cases': matching_cases,
                'total_cases': len(specialist_data)
            }
    
    # Sort by average score
    sorted_specialists = sorted(specialist_scores.items(), 
                              key=lambda x: x[1]['avg_score'], 
                              reverse=True)
    
    print(f"\n=== TOP {top_n} DOCTOR RECOMMENDATIONS ===")
    results = []
    
    for i, (specialist, scores) in enumerate(sorted_specialists[:top_n], 1):
        confidence = scores['avg_score'] * 100
        match_rate = (scores['matching_cases'] / scores['total_cases']) * 100
        
        print(f"{i}. {specialist}")
        print(f"   Confidence: {confidence:.1f}%")
        print(f"   Cases with similar symptoms: {scores['matching_cases']}/{scores['total_cases']} ({match_rate:.1f}%)")
        print(f"   Best match score: {scores['max_score']:.3f}")
        print()
        
        results.append({
            'specialist': specialist,
            'confidence': confidence,
            'matching_cases': scores['matching_cases'],
            'total_cases': scores['total_cases']
        })
    
    return results

def interactive_recommender():
    """Interactive function for testing"""
    print("\n" + "="*60)
    print("🏥 INTERACTIVE DOCTOR RECOMMENDER")
    print("="*60)
    
    # Show available symptoms
    print("Available symptoms (first 20):")
    for i, symptom in enumerate(list(symptom_columns)[:20], 1):
        clean_name = symptom.strip().replace('_', ' ')
        print(f"{i:2d}. {clean_name}")
    print("    ... and many more!")
    
    print("\nEnter your symptoms separated by commas:")
    print("Example: itching, skin rash, fever")
    
    # For demo, let's test with predefined cases
    test_cases = [
        {
            'name': 'Skin Issues',
            'symptoms': ['itching', 'skin_rash', 'red_spots_over_body']
        },
        {
            'name': 'Digestive Problems', 
            'symptoms': ['stomach_pain', 'vomiting', 'nausea', 'abdominal_pain']
        },
        {
            'name': 'Heart Problems',
            'symptoms': ['chest_pain', 'fast_heart_rate', 'palpitations', 'breathlessness']
        },
        {
            'name': 'Joint Pain',
            'symptoms': ['joint_pain', 'knee_pain', 'hip_joint_pain', 'movement_stiffness']
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'='*50}")
        print(f"TEST CASE: {test_case['name']}")
        print(f"SYMPTOMS: {', '.join(test_case['symptoms'])}")
        recommend_doctor_improved(test_case['symptoms'])

# Run the interactive recommender
if __name__ == "__main__":
    interactive_recommender()