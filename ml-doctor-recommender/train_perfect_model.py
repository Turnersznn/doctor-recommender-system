import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load the perfect training data
print("Loading perfect training data...")
df = pd.read_excel("Specialist_perfect.xlsx")

# Prepare features and target
X = df.drop('Specialist', axis=1)
y = df['Specialist']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Create a RandomForest model with optimal parameters
clf = RandomForestClassifier(
    n_estimators=300,  # More trees for better accuracy
    max_depth=15,      # Allow deeper trees
    min_samples_split=3,
    min_samples_leaf=1,
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
test_symptoms = ['itching', 'headache', 'nausea', 'cough', 'watering_from_eyes', 'chest_pain', 'depression', 'back_pain']
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
            'chest_pain': 'Cardiologist',
            'depression': 'Neurologist',
            'back_pain': 'Rheumatologists'
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