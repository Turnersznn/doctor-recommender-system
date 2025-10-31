import joblib
import pandas as pd

# Load the model
model = joblib.load("content_model_specialist.pkl")

# Define the informative symptoms used in training
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

# Load the data to get the exact feature columns
df = pd.read_excel("Specialist.xlsx")
cols = [col for col in df.columns if not col.lower().startswith('unnamed')]
df = df[cols]
feature_columns = [col for col in informative_symptoms if col in df.columns]

print(f"Using {len(feature_columns)} features: {feature_columns[:5]}...")

# Test different symptom combinations
test_cases = [
    {"itching": 1, " skin_rash": 1, "cough": 0, " headache": 0},
    {" headache": 1, " dizziness": 1, "itching": 0, " skin_rash": 0},
    {" chest_pain": 1, " breathlessness": 1, "itching": 0, " skin_rash": 0},
    {" abdominal_pain": 1, " nausea": 1, "itching": 0, " skin_rash": 0},
    {" joint_pain": 1, " swelling_joints": 1, "itching": 0, " skin_rash": 0},
    {" fatigue": 1, " weight_loss": 1, "itching": 0, " skin_rash": 0},
    {" blurred_and_distorted_vision": 1, "itching": 0, " skin_rash": 0},
    {" cough": 1, " breathlessness": 1, "itching": 0, " skin_rash": 0},
]

print("\nTesting model predictions:")
for i, symptoms in enumerate(test_cases, 1):
    # Create input data with all features
    input_data = {col: symptoms.get(col, 0) for col in feature_columns}
    X = pd.DataFrame([input_data])
    
    # Predict
    prediction = model.predict(X)[0]
    print(f"Test {i}: {symptoms} → {prediction}")

print("\nModel feature importance:")
# Get feature importance if available
if hasattr(model, 'feature_importances_'):
    feature_importance = list(zip(feature_columns, model.feature_importances_))
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    print("Top 10 most important features:")
    for feature, importance in feature_importance[:10]:
        print(f"  {feature}: {importance:.4f}") 