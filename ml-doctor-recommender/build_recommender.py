import pandas as pd
import numpy as np

print("=== BUILDING DOCTOR RECOMMENDER SYSTEM ===\n")

# Step 1: Load the main dataset (symptoms to doctor mapping)
print("Loading main dataset...")
main_data = pd.read_excel('Specialist.xlsx')
print(f"✓ Loaded {main_data.shape[0]} records with {main_data.shape[1]} columns")

# Step 2: Clean up the data
print("\nCleaning data...")
# Remove the unnamed column
main_data = main_data.drop('Unnamed: 0', axis=1)

# The last column is the target (doctor specialist)
target_column = main_data.columns[-1]  # Should be 'Disease' but actually contains doctor names
symptom_columns = main_data.columns[:-1]  # All symptom columns

print(f"✓ Found {len(symptom_columns)} symptoms")
print(f"✓ Target column: {target_column}")

# Step 3: Let's see what doctor specialists we have
print(f"\nDoctor specialists in our data:")
specialists = main_data[target_column].unique()
for i, specialist in enumerate(specialists, 1):
    count = (main_data[target_column] == specialist).sum()
    print(f"{i}. {specialist}: {count} cases")

print(f"\n✓ Total unique specialists: {len(specialists)}")

# Step 4: Build the recommendation function
def recommend_doctor(user_symptoms):
    """
    Recommend a doctor based on user symptoms
    user_symptoms: list of symptoms (e.g., ['itching', 'skin_rash'])
    """
    print(f"\n=== ANALYZING SYMPTOMS: {user_symptoms} ===")
    
    # Create a user symptom vector (0s and 1s)
    user_vector = []
    for symptom in symptom_columns:
        # Clean symptom name (remove extra spaces)
        clean_symptom = symptom.strip()
        if clean_symptom in user_symptoms:
            user_vector.append(1)
        else:
            user_vector.append(0)
    
    user_vector = np.array(user_vector)
    print(f"✓ Created user symptom vector with {sum(user_vector)} active symptoms")
    
    # Calculate similarity with all cases in our dataset
    similarities = []
    for index, row in main_data.iterrows():
        # Get symptom vector for this case
        case_vector = np.array(row[symptom_columns])
        
        # Calculate similarity (we'll use simple matching for now)
        # Count how many symptoms match
        matching_symptoms = np.sum(user_vector * case_vector)
        total_user_symptoms = np.sum(user_vector)
        
        # Avoid division by zero
        if total_user_symptoms > 0:
            similarity = matching_symptoms / total_user_symptoms
        else:
            similarity = 0
            
        similarities.append({
            'similarity': similarity,
            'specialist': row[target_column],
            'matching_symptoms': matching_symptoms
        })
    
    # Convert to DataFrame for easier analysis
    similarity_df = pd.DataFrame(similarities)
    
    # Group by specialist and get average similarity
    specialist_scores = similarity_df.groupby('specialist').agg({
        'similarity': 'mean',
        'matching_symptoms': 'mean'
    }).round(3)
    
    # Sort by similarity score
    specialist_scores = specialist_scores.sort_values('similarity', ascending=False)
    
    print(f"\n=== TOP DOCTOR RECOMMENDATIONS ===")
    for i, (specialist, scores) in enumerate(specialist_scores.head(5).iterrows(), 1):
        print(f"{i}. {specialist}")
        print(f"   Match Score: {scores['similarity']:.3f}")
        print(f"   Avg Matching Symptoms: {scores['matching_symptoms']:.1f}")
        print()
    
    return specialist_scores.head(5)

# Step 5: Test the recommender with some example symptoms
print("\n" + "="*60)
print("TESTING THE RECOMMENDER SYSTEM")
print("="*60)

# Test 1: Skin problems
test_symptoms_1 = ['itching', 'skin_rash']
recommend_doctor(test_symptoms_1)

# Test 2: Stomach problems  
test_symptoms_2 = ['stomach_pain', 'vomiting', 'nausea']
recommend_doctor(test_symptoms_2)

# Test 3: Heart problems
test_symptoms_3 = ['chest_pain', 'fast_heart_rate', 'palpitations']
recommend_doctor(test_symptoms_3)