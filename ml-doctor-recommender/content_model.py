import pandas as pd
from sklearn.model_selection import train_test_split

# === STEP 1: Load and Prepare Data ===

# 1. Load Excel file
df = pd.read_excel("Specialist.xlsx")

# 2. Drop unwanted column (like index)
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

# 3. Separate features (X) and label (y)
X = df.iloc[:, :-1]  # All columns except last = symptoms
y = df.iloc[:, -1]   # Last column = specialist

# 4. Train-test split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("✅ Data loaded and split successfully")
print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# === STEP 2: Train the Model ===

model = RandomForestClassifier()
model.fit(X_train, y_train)

print("\n✅ Model trained successfully!")

# === STEP 3: Evaluate on Test Set ===

y_pred = model.predict(X_test)

print("\n=== CLASSIFICATION REPORT ===")
print(classification_report(y_test, y_pred))

import joblib

joblib.dump(model, "content_model.pkl")
print("\n✅ Trained model saved as 'content_model.pkl'")
