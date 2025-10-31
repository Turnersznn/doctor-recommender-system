import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# === STEP 1: Load and Prepare Data ===
df = pd.read_excel("Specialist.xlsx")
df = df.drop(columns=["Unnamed: 0"], errors="ignore")
df.columns = df.columns.str.strip()  # Clean column names

print("Class balance before balancing:")
print(df['Disease'].value_counts())

# === STEP 2: Balance the Data ===
min_count = df['Disease'].value_counts().min()
classes = df['Disease'].unique()

balanced_df = pd.concat([
    resample(df[df['Disease'] == c], replace=False, n_samples=min_count, random_state=42)
    for c in classes
])

print("\nClass balance after balancing:")
print(balanced_df['Disease'].value_counts())

# === STEP 3: Feature/Label Split ===
X = balanced_df.iloc[:, :-1]
y = balanced_df.iloc[:, -1]

# === STEP 4: Train-Test Split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === STEP 5: Try Different Models ===
models = {
    'RandomForest': RandomForestClassifier(random_state=42),
    'DecisionTree': DecisionTreeClassifier(random_state=42),
    'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42)
}

best_model = None
best_f1 = 0

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"\n=== {name} Classification Report ===")
    report = classification_report(y_test, y_pred, output_dict=True)
    print(classification_report(y_test, y_pred))
    avg_f1 = report['weighted avg']['f1-score']
    if avg_f1 > best_f1:
        best_f1 = avg_f1
        best_model = model

# === STEP 6: Save the Best Model ===
joblib.dump(best_model, "content_model_balanced.pkl")
print(f"\n✅ Best model saved as 'content_model_balanced.pkl' (f1={best_f1:.3f})") 