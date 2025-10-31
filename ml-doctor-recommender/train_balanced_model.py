import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.utils import resample
import joblib

# Load the data
df = pd.read_excel("Specialist_with_specialist.xlsx")
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

# Prepare features and target
X = df.iloc[:, :-2]  # All columns except last two (Disease, Specialist)
y = df['Specialist']

print("Original data distribution:")
print(y.value_counts())

# Balance the dataset by downsampling the majority classes
balanced_dfs = []
target_count = 100  # Target 100 samples per specialist

for specialist in y.unique():
    specialist_data = df[y == specialist]
    if len(specialist_data) > target_count:
        # Downsample if we have too many
        balanced_data = resample(specialist_data, 
                               n_samples=target_count, 
                               random_state=42, 
                               replace=False)
    else:
        # Keep all if we have fewer than target
        balanced_data = specialist_data
    
    balanced_dfs.append(balanced_data)

# Combine all balanced data
balanced_df = pd.concat(balanced_dfs, ignore_index=True)
X_balanced = balanced_df.iloc[:, :-2]
y_balanced = balanced_df['Specialist']

print("\nBalanced data distribution:")
print(y_balanced.value_counts())

# Split the balanced data
X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=0.2, random_state=42, stratify=y_balanced)

# Train the model
model = RandomForestClassifier(random_state=42, n_estimators=100)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the balanced model
joblib.dump(model, "content_model_specialist.pkl")
print("✅ Balanced model saved as content_model_specialist.pkl")

# Test some predictions
test_cases = [
    {"itching": 1, "skin_rash": 0, "fever": 0},
    {"headache": 1, "dizziness": 0, "fever": 0},
    {"chest_pain": 1, "shortness_of_breath": 0, "fever": 0},
    {"stomach_pain": 1, "nausea": 0, "fever": 0},
    {"joint_pain": 1, "swelling_joints": 0, "fever": 0},
    {"depression": 1, "anxiety": 0, "fever": 0},
    {"blurred_and_distorted_vision": 1, "fever": 0},
    {"sore_throat": 1, "cough": 0, "fever": 0},
]

print("\nTest predictions:")
for i, symptoms in enumerate(test_cases, 1):
    input_data = {col: symptoms.get(col, 0) for col in X_train.columns}
    X_test_case = pd.DataFrame([input_data])
    prediction = model.predict(X_test_case)[0]
    print(f"Test {i}: {symptoms} → {prediction}") 