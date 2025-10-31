#!/usr/bin/env python3
"""
Analyze existing datasets to understand the data structure
"""

import pandas as pd
import numpy as np

def analyze_datasets():
    print("🔍 Analyzing existing datasets...")
    
    # Load datasets
    try:
        original_df = pd.read_csv('Original_Dataset.csv', encoding='latin-1')
        doctor_disease_df = pd.read_csv('Doctor_Versus_Disease.csv', names=['Disease', 'Specialist'], encoding='latin-1')
        
        print(f"\n📊 Original Dataset: {original_df.shape}")
        print(f"📊 Doctor-Disease Mapping: {doctor_disease_df.shape}")
        
        # Check unique diseases
        print(f"\n🏥 Diseases in original dataset: {original_df['Disease'].nunique()}")
        print(f"🏥 Diseases in doctor mapping: {doctor_disease_df['Disease'].nunique()}")
        
        # Check specialists
        print(f"\n👨‍⚕️ Available specialists:")
        specialists = doctor_disease_df['Specialist'].unique()
        for specialist in specialists:
            count = doctor_disease_df[doctor_disease_df['Specialist'] == specialist].shape[0]
            print(f"  - {specialist}: {count} diseases")
        
        # Check respiratory diseases
        print(f"\n🫁 Respiratory-related diseases:")
        respiratory_diseases = doctor_disease_df[
            doctor_disease_df['Disease'].str.contains('Asthma|Pneumonia|Tuberculosis', case=False, na=False)
        ]
        print(respiratory_diseases)
        
        # Check symptoms in original dataset
        print(f"\n🔍 Sample symptoms from original dataset:")
        sample_row = original_df.iloc[0]
        symptoms = []
        for col in original_df.columns[1:]:  # Skip Disease column
            if pd.notna(sample_row[col]) and sample_row[col].strip():
                symptoms.append(sample_row[col].strip())
        print(f"Sample symptoms: {symptoms}")
        
        # Look for cough-related diseases
        print(f"\n🔍 Looking for cough-related diseases...")
        cough_rows = original_df[
            original_df.apply(lambda row: 'cough' in str(row).lower(), axis=1)
        ]
        if not cough_rows.empty:
            print(f"Found {len(cough_rows)} rows with cough symptoms:")
            print(cough_rows['Disease'].unique())
        else:
            print("No cough symptoms found in dataset")
            
        # Look for depression-related diseases
        print(f"\n🔍 Looking for depression-related diseases...")
        depression_rows = original_df[
            original_df.apply(lambda row: 'depression' in str(row).lower(), axis=1)
        ]
        if not depression_rows.empty:
            print(f"Found {len(depression_rows)} rows with depression symptoms:")
            print(depression_rows['Disease'].unique())
        else:
            print("No depression symptoms found in dataset")
            
        return original_df, doctor_disease_df
        
    except Exception as e:
        print(f"❌ Error loading datasets: {e}")
        return None, None

def create_proper_model_from_existing_data():
    """Create a proper ML model using the existing datasets"""
    
    print("\n🤖 Creating ML model from existing data...")
    
    original_df, doctor_disease_df = analyze_datasets()
    
    if original_df is None:
        return
    
    # Create symptom-disease-specialist mapping
    print("\n🔗 Creating symptom-disease-specialist mapping...")
    
    # Get all unique symptoms
    all_symptoms = set()
    for _, row in original_df.iterrows():
        for col in original_df.columns[1:]:  # Skip Disease column
            if pd.notna(row[col]) and str(row[col]).strip():
                symptom = str(row[col]).strip().lower().replace(' ', '_')
                all_symptoms.add(symptom)
    
    all_symptoms = sorted(list(all_symptoms))
    print(f"📝 Found {len(all_symptoms)} unique symptoms")
    
    # Create training data
    training_data = []
    
    for _, row in original_df.iterrows():
        disease = row['Disease']
        
        # Get specialist for this disease
        specialist_row = doctor_disease_df[doctor_disease_df['Disease'] == disease]
        if specialist_row.empty:
            continue
            
        specialist = specialist_row.iloc[0]['Specialist']
        
        # Create feature vector
        feature_vector = {symptom: 0 for symptom in all_symptoms}
        
        # Set symptoms to 1
        for col in original_df.columns[1:]:
            if pd.notna(row[col]) and str(row[col]).strip():
                symptom = str(row[col]).strip().lower().replace(' ', '_')
                if symptom in feature_vector:
                    feature_vector[symptom] = 1
        
        feature_vector['specialist'] = specialist
        training_data.append(feature_vector)
    
    # Convert to DataFrame
    training_df = pd.DataFrame(training_data)
    
    print(f"✅ Created {len(training_df)} training samples")
    print(f"✅ Specialists: {training_df['specialist'].unique()}")
    
    # Train model
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report
    import joblib
    import pickle
    
    X = training_df[all_symptoms]
    y = training_df['specialist']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = (y_pred == y_test).mean()
    
    print(f"\n✅ Model trained with accuracy: {accuracy:.3f}")
    
    # Test specific cases
    print(f"\n🧪 Testing model predictions...")
    
    # Test if we have respiratory symptoms
    respiratory_symptoms = ['cough', 'breathing_difficulty', 'chest_pain']
    for symptom in respiratory_symptoms:
        if symptom in all_symptoms:
            test_input = pd.DataFrame([[0] * len(all_symptoms)], columns=all_symptoms)
            test_input[symptom] = 1
            prediction = model.predict(test_input)[0]
            probability = model.predict_proba(test_input)[0].max()
            print(f"  {symptom} -> {prediction} (confidence: {probability:.3f})")
    
    # Save model
    joblib.dump(model, 'content_model_from_existing_data.pkl')
    with open('feature_columns_from_existing_data.pkl', 'wb') as f:
        pickle.dump(all_symptoms, f)
    
    print(f"\n💾 Saved model as content_model_from_existing_data.pkl")
    print(f"💾 Saved features as feature_columns_from_existing_data.pkl")

if __name__ == "__main__":
    create_proper_model_from_existing_data()
