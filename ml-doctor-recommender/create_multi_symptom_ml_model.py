#!/usr/bin/env python3
"""
Create a Multi-Symptom ML Model for Disease Prediction and Specialist Recommendation

This demonstrates the STRENGTH of ML by:
1. Learning complex symptom patterns from real medical data
2. Handling multiple symptoms simultaneously 
3. Discovering hidden relationships between symptoms and diseases
4. Providing probabilistic predictions with confidence scores
5. Generalizing to new symptom combinations not seen in training
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import pickle
from collections import defaultdict

def load_and_prepare_data():
    """Load the original dataset and prepare it for multi-symptom ML training"""
    print("🔄 Loading original medical dataset...")
    
    # Load the original dataset with disease-symptom combinations
    df = pd.read_csv('Original_Dataset.csv', encoding='latin-1')
    print(f"✅ Loaded {len(df)} disease-symptom records")
    
    # Load disease-to-specialist mapping
    mapping_df = pd.read_csv('Doctor_Versus_Disease.csv', names=['Disease', 'Specialist'], encoding='latin-1')
    disease_to_specialist = dict(zip(mapping_df['Disease'].str.strip(), mapping_df['Specialist'].str.strip()))
    print(f"✅ Loaded {len(disease_to_specialist)} disease-specialist mappings")
    
    return df, disease_to_specialist

def create_multi_symptom_training_data(df, disease_to_specialist):
    """Convert the original data into multi-symptom ML training format"""
    print("🔄 Creating multi-symptom training data...")
    
    # Get all unique symptoms from the dataset
    all_symptoms = set()
    for _, row in df.iterrows():
        for col in ['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4', 'Symptom_5', 
                   'Symptom_6', 'Symptom_7', 'Symptom_8', 'Symptom_9', 'Symptom_10',
                   'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14', 'Symptom_15',
                   'Symptom_16', 'Symptom_17']:
            symptom = str(row[col]).strip()
            if symptom and symptom != 'nan' and symptom != '':
                # Clean symptom names
                symptom = symptom.lower().replace(' ', '_').replace(',', '').strip()
                all_symptoms.add(symptom)
    
    all_symptoms = sorted(list(all_symptoms))
    print(f"✅ Found {len(all_symptoms)} unique symptoms")
    
    # Create training data with one-hot encoding for symptoms
    training_data = []
    
    for _, row in df.iterrows():
        disease = row['Disease'].strip()
        
        # Get specialist for this disease
        specialist = disease_to_specialist.get(disease, 'General Practitioner')
        
        # Create symptom vector
        symptom_vector = {symptom: 0 for symptom in all_symptoms}
        
        # Mark present symptoms as 1
        for col in ['Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4', 'Symptom_5', 
                   'Symptom_6', 'Symptom_7', 'Symptom_8', 'Symptom_9', 'Symptom_10',
                   'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14', 'Symptom_15',
                   'Symptom_16', 'Symptom_17']:
            symptom = str(row[col]).strip()
            if symptom and symptom != 'nan' and symptom != '':
                symptom = symptom.lower().replace(' ', '_').replace(',', '').strip()
                if symptom in symptom_vector:
                    symptom_vector[symptom] = 1
        
        # Add to training data
        training_record = symptom_vector.copy()
        training_record['disease'] = disease
        training_record['specialist'] = specialist
        training_data.append(training_record)
    
    # Convert to DataFrame
    training_df = pd.DataFrame(training_data)
    print(f"✅ Created {len(training_df)} training records")
    print(f"✅ Diseases: {training_df['disease'].nunique()}")
    print(f"✅ Specialists: {training_df['specialist'].nunique()}")
    
    return training_df, all_symptoms

def augment_training_data(training_df, all_symptoms):
    """Augment training data with realistic multi-symptom combinations"""
    print("🔄 Augmenting training data with multi-symptom combinations...")
    
    augmented_data = []
    
    # Group by disease to create realistic combinations
    for disease, group in training_df.groupby('disease'):
        specialist = group['specialist'].iloc[0]
        
        # Get all symptoms for this disease
        disease_symptoms = []
        for _, row in group.iterrows():
            symptoms = [col for col in all_symptoms if row[col] == 1]
            disease_symptoms.extend(symptoms)
        
        # Get unique symptoms for this disease
        unique_symptoms = list(set(disease_symptoms))
        
        if len(unique_symptoms) >= 2:
            # Create combinations of 2-4 symptoms
            for combo_size in [2, 3, 4]:
                if len(unique_symptoms) >= combo_size:
                    # Create multiple random combinations
                    for _ in range(min(10, len(unique_symptoms))):
                        selected_symptoms = np.random.choice(unique_symptoms, 
                                                           size=min(combo_size, len(unique_symptoms)), 
                                                           replace=False)
                        
                        # Create training record
                        record = {symptom: 0 for symptom in all_symptoms}
                        for symptom in selected_symptoms:
                            record[symptom] = 1
                        record['disease'] = disease
                        record['specialist'] = specialist
                        augmented_data.append(record)
    
    # Add augmented data to original
    augmented_df = pd.DataFrame(augmented_data)
    combined_df = pd.concat([training_df, augmented_df], ignore_index=True)
    
    print(f"✅ Added {len(augmented_data)} augmented records")
    print(f"✅ Total training data: {len(combined_df)} records")
    
    return combined_df

def train_multi_symptom_models(training_df, all_symptoms):
    """Train multiple ML models for multi-symptom prediction"""
    print("🔄 Training multi-symptom ML models...")
    
    # Prepare features and targets
    X = training_df[all_symptoms]
    y_disease = training_df['disease']
    y_specialist = training_df['specialist']
    
    print(f"✅ Features shape: {X.shape}")
    print(f"✅ Unique diseases: {len(y_disease.unique())}")
    print(f"✅ Unique specialists: {len(y_specialist.unique())}")
    
    # Split data
    X_train, X_test, y_disease_train, y_disease_test, y_specialist_train, y_specialist_test = train_test_split(
        X, y_disease, y_specialist, test_size=0.2, random_state=42, stratify=y_specialist
    )
    
    # Train Disease Prediction Model (Random Forest)
    print("🔄 Training Disease Prediction Model...")
    disease_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    disease_model.fit(X_train, y_disease_train)
    
    # Train Specialist Prediction Model (Gradient Boosting)
    print("🔄 Training Specialist Prediction Model...")
    specialist_model = GradientBoostingClassifier(
        n_estimators=150,
        max_depth=8,
        learning_rate=0.1,
        random_state=42
    )
    specialist_model.fit(X_train, y_specialist_train)
    
    # Evaluate models
    print("\n📊 Model Evaluation:")
    
    # Disease model evaluation
    disease_pred = disease_model.predict(X_test)
    disease_accuracy = accuracy_score(y_disease_test, disease_pred)
    print(f"✅ Disease Model Accuracy: {disease_accuracy:.3f}")
    
    # Specialist model evaluation
    specialist_pred = specialist_model.predict(X_test)
    specialist_accuracy = accuracy_score(y_specialist_test, specialist_pred)
    print(f"✅ Specialist Model Accuracy: {specialist_accuracy:.3f}")
    
    # Cross-validation scores
    disease_cv_scores = cross_val_score(disease_model, X, y_disease, cv=5)
    specialist_cv_scores = cross_val_score(specialist_model, X, y_specialist, cv=5)
    
    print(f"✅ Disease Model CV Score: {disease_cv_scores.mean():.3f} (+/- {disease_cv_scores.std() * 2:.3f})")
    print(f"✅ Specialist Model CV Score: {specialist_cv_scores.mean():.3f} (+/- {specialist_cv_scores.std() * 2:.3f})")
    
    return disease_model, specialist_model

def save_models_and_features(disease_model, specialist_model, all_symptoms):
    """Save the trained models and feature columns"""
    print("🔄 Saving models and features...")
    
    # Save models
    joblib.dump(disease_model, 'multi_symptom_disease_model.pkl')
    joblib.dump(specialist_model, 'multi_symptom_specialist_model.pkl')
    
    # Save feature columns
    with open('multi_symptom_features.pkl', 'wb') as f:
        pickle.dump(all_symptoms, f)
    
    print("✅ Saved multi_symptom_disease_model.pkl")
    print("✅ Saved multi_symptom_specialist_model.pkl") 
    print("✅ Saved multi_symptom_features.pkl")

def main():
    """Main function to create the multi-symptom ML model"""
    print("🚀 Creating Multi-Symptom ML Model - Demonstrating ML Strength!")
    print("=" * 70)
    
    # Load data
    df, disease_to_specialist = load_and_prepare_data()
    
    # Create training data
    training_df, all_symptoms = create_multi_symptom_training_data(df, disease_to_specialist)
    
    # Augment with multi-symptom combinations
    augmented_df = augment_training_data(training_df, all_symptoms)
    
    # Train models
    disease_model, specialist_model = train_multi_symptom_models(augmented_df, all_symptoms)
    
    # Save models
    save_models_and_features(disease_model, specialist_model, all_symptoms)
    
    print("\n🎉 Multi-Symptom ML Model Creation Complete!")
    print("This ML model can now:")
    print("  ✅ Learn complex symptom patterns")
    print("  ✅ Handle multiple symptoms simultaneously")
    print("  ✅ Predict diseases with confidence scores")
    print("  ✅ Recommend specialists based on learned patterns")
    print("  ✅ Generalize to new symptom combinations")

if __name__ == "__main__":
    main()
