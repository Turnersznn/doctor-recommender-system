import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.utils import resample
import joblib

# Load the data
df = pd.read_excel("Specialist.xlsx")
cols = [col for col in df.columns if not col.lower().startswith('unnamed')]
df = df[cols]

# Use symptoms that actually exist in the data and are informative
informative_symptoms = [
    'itching', ' skin_rash', 'cough', ' loss_of_appetite', ' sweating', 
    ' joint_pain', ' chills', ' nausea', ' diarrhoea', ' malaise',
    ' abdominal_pain', ' weight_loss', ' lethargy', ' breathlessness', 
    ' dizziness', ' loss_of_balance', ' muscle_pain', ' mild_fever',
    ' swelled_lymph_nodes', ' phlegm', ' continuous_sneezing', ' stomach_pain',
    ' acidity', ' yellowish_skin', ' yellowing_of_eyes', ' burning_micturition',
    ' indigestion', ' blurred_and_distorted_vision', ' obesity', ' excessive_hunger',
    ' family_history', ' stiff_neck', ' depression', ' irritability', ' back_pain',
    ' neck_pain', ' dark_urine', ' red_spots_over_body', ' constipation',
    ' fast_heart_rate', ' muscle_weakness', ' swelling_joints', ' painful_walking'
]

# Filter to only use informative symptoms + Disease column
feature_cols = [col for col in informative_symptoms if col in df.columns]
df_filtered = df[feature_cols + ['Disease']]

print(f"Using {len(feature_cols)} informative symptoms")
print("Original distribution:")
print(df_filtered['Disease'].value_counts())

# Balance the dataset by downsampling majority classes
balanced_dfs = []
target_count = 100  # Target 100 samples per specialist

for specialist in df_filtered['Disease'].unique():
    specialist_data = df_filtered[df_filtered['Disease'] == specialist]
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
X = balanced_df[feature_cols]
y = balanced_df['Disease']

print("\nBalanced distribution:")
print(y.value_counts())

# Split the balanced data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

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
    {"itching": 1, " skin_rash": 0, "fever": 0},
    {" headache": 1, " dizziness": 0, "fever": 0},
    {" chest_pain": 1, " breathlessness": 0, "fever": 0},
    {" abdominal_pain": 1, " nausea": 0, "fever": 0},
    {" joint_pain": 1, " swelling_joints": 0, "fever": 0},
    {" fatigue": 1, " weight_loss": 0, "fever": 0},
    {" blurred_and_distorted_vision": 1, "fever": 0},
    {" cough": 1, " breathlessness": 0, "fever": 0},
]

print("\nTest predictions:")
for i, symptoms in enumerate(test_cases, 1):
    input_data = {col: symptoms.get(col, 0) for col in feature_cols}
    X_test_case = pd.DataFrame([input_data])
    prediction = model.predict(X_test_case)[0]
    print(f"Test {i}: {symptoms} → {prediction}") 