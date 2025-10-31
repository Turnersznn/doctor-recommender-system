import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import numpy as np

# Load the training data
df = pd.read_excel("Specialist_clean_clinical.xlsx")

# Features and label
X = df.drop(columns=["Specialist"])
y = df["Specialist"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train a simpler model with fewer estimators and more regularization
clf = RandomForestClassifier(
    n_estimators=100,  # Reduced from 200
    random_state=42, 
    class_weight="balanced",
    max_depth=10,  # Limit depth to prevent overfitting
    min_samples_split=5,  # Require more samples to split
    min_samples_leaf=2  # Require more samples in leaves
)

clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
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
        if symptom == 'itching' and prediction != 'Dermatologist':
            print(f"  ⚠️  {symptom} should predict Dermatologist but predicts {prediction}")
        elif symptom == 'headache' and prediction != 'Neurologist':
            print(f"  ⚠️  {symptom} should predict Neurologist but predicts {prediction}")
        elif symptom == 'nausea' and prediction != 'Gastroenterologist':
            print(f"  ⚠️  {symptom} should predict Gastroenterologist but predicts {prediction}")
        elif symptom == 'cough' and prediction != 'Pulmonologist':
            print(f"  ⚠️  {symptom} should predict Pulmonologist but predicts {prediction}")
        elif symptom == 'watering_from_eyes' and prediction != 'Ophthalmologist':
            print(f"  ⚠️  {symptom} should predict Ophthalmologist but predicts {prediction}")
        elif symptom == 'chest_pain' and prediction != 'Cardiologist':
            print(f"  ⚠️  {symptom} should predict Cardiologist but predicts {prediction}")

# Save the new model
joblib.dump(clf, "content_model_specialist_fixed.pkl")
print("\n✅ Model saved as content_model_specialist_fixed.pkl") 