import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Create a much better training dataset
def create_better_training_data():
    # Define clear symptom-specialist mappings
    mappings = {
        'Dermatologist': ['itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic _patches', 'pus_filled_pimples', 'blackheads', 'scurring', 'blister'],
        'Neurologist': ['headache', 'dizziness', 'loss_of_balance', 'lack_of_concentration', 'stiff_neck', 'depression', 'irritability', 'neck_pain'],
        'Gastroenterologist': ['nausea', 'vomiting', 'abdominal_pain', 'stomach_pain', 'diarrhoea', 'constipation', 'indigestion', 'acidity'],
        'Pulmonologist': ['cough', 'breathlessness', 'phlegm', 'blood_in_sputum', 'rusty_sputum', 'mucoid_sputum'],
        'Cardiologist': ['chest_pain', 'fast_heart_rate', 'palpitations'],
        'Ophthalmologist': ['watering_from_eyes', 'yellowing_of_eyes', 'sunken_eyes', 'pain_behind_the_eyes', 'redness_of_eyes', 'blurred_and_distorted_vision', 'visual_disturbances'],
        'Endocrinologist': ['irregular_sugar_level', 'excessive_hunger', 'weight_loss', 'weight_gain', 'obesity', 'polyuria', 'enlarged_thyroid'],
        'Rheumatologists': ['joint_pain', 'swelling_joints', 'painful_walking', 'movement_stiffness', 'knee_pain', 'hip_joint_pain', 'back_pain'],
        'Allergist': ['continuous_sneezing', 'shivering', 'chills', 'runny_nose', 'congestion', 'throat_irritation'],
        'Gynecologist': ['burning_micturition', 'bladder_discomfort', 'foul_smell_of urine', 'continuous_feel_of_urine', 'abnormal_menstruation'],
        'Internal Medcine': ['fatigue', 'mild_fever', 'high_fever', 'sweating', 'loss_of_appetite', 'malaise', 'lethargy']
    }
    
    # Load original data to get all possible symptoms
    df_original = pd.read_excel("Specialist_cleaned.xlsx")
    all_symptoms = [col for col in df_original.columns if col != 'Specialist']
    
    training_rows = []
    
    # Create training data with multiple symptoms per specialist
    for specialist, symptoms in mappings.items():
        # Create 100 rows per specialist for better training
        for i in range(100):
            row = {symptom: 0 for symptom in all_symptoms}
            row['Specialist'] = specialist
            
            # Add 1-3 symptoms from this specialist's list
            num_symptoms = np.random.randint(1, 4)
            available_symptoms = [s for s in symptoms if s in all_symptoms]
            
            if available_symptoms:
                selected_symptoms = np.random.choice(available_symptoms, min(num_symptoms, len(available_symptoms)), replace=False)
                for symptom in selected_symptoms:
                    row[symptom] = 1
            
            training_rows.append(row)
    
    return pd.DataFrame(training_rows)

# Create better training data
print("Creating better training data...")
df = create_better_training_data()

# Prepare features and target
X = df.drop('Specialist', axis=1)
y = df['Specialist']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Create a better RandomForest model with different parameters
clf = RandomForestClassifier(
    n_estimators=200,  # More trees
    max_depth=10,      # Limit depth to prevent overfitting
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    class_weight='balanced'  # Handle class imbalance
)

# Train the model
print("Training the model...")
clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
print("\nModel Performance:")
print(classification_report(y_test, y_pred))

# Test specific symptoms
print("\nTesting specific symptoms:")
test_symptoms = ['itching', 'headache', 'nausea', 'cough', 'watering_from_eyes', 'chest_pain']
feature_columns = X.columns.tolist()

for symptom in test_symptoms:
    if symptom in feature_columns:
        # Create input with just this symptom
        input_data = np.zeros((1, len(feature_columns)))
        symptom_index = feature_columns.index(symptom)
        input_data[0, symptom_index] = 1
        
        prediction = clf.predict(input_data)[0]
        print(f"{symptom}: {prediction}")
        
        # Check if prediction makes sense
        expected = {
            'itching': 'Dermatologist',
            'headache': 'Neurologist',
            'nausea': 'Gastroenterologist',
            'cough': 'Pulmonologist',
            'watering_from_eyes': 'Ophthalmologist',
            'chest_pain': 'Cardiologist'
        }
        
        if symptom in expected and prediction != expected[symptom]:
            print(f"  ⚠️  {symptom} should predict {expected[symptom]} but predicts {prediction}")

# Save the model
joblib.dump(clf, 'content_model_specialist_fixed.pkl')
print(f"\n✅ Model saved as content_model_specialist_fixed.pkl")

# Also save the feature columns for the API
import pickle
with open('feature_columns.pkl', 'wb') as f:
    pickle.dump(feature_columns, f)
print("✅ Feature columns saved") 