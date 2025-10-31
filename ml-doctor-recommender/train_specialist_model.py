import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load cleaned data
input_file = "Specialist_simple.xlsx"
df = pd.read_excel(input_file)

# Features and label
X = df.drop(columns=["Specialist"])
y = df["Specialist"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train RandomForest
clf = RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, "content_model_specialist_fixed.pkl")
print("✅ Model saved as content_model_specialist_fixed.pkl") 